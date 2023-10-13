from csv import DictWriter
from timeit import default_timer
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.decorators import action
from .models import Product, Order, ProductImage, User
from .forms import ProductForm
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, OrderSerializer
from django.contrib.syndication.views import Feed


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        links = [
            {"title": "Products", "address": "products/"},
            {"title": "Orders", "address": "orders/"},
        ]
        context = {
            "time_running": default_timer(),
            "links": links
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = [
        "delivery_address",
        "promocode",
        "created_at",
        "user",
        "products",
    ]
    ordering_fields = [
        "user",
        "created_at",
    ]

    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = "orders-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "delivery_address",
            "promocode",
            "created_at",
            "user_id",
            "products",
        ]
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for order in queryset:
            writer.writerow({
                field: getattr(order, field)
                for field in fields
            })
        return response


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = "products"
    queryset = (
        Product.objects.filter(archived=False)
        .filter(created_at__isnull=False)
        .order_by("-created_at")
    )


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by_id = self.request.user.id
        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = "shopapp.change_product"
    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    form_class = ProductForm
    template_name_suffix = "_update_form"

    def test_func(self):
        return self.request.user.id == self.get_object().created_by_id or self.request.user.is_superuser

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductsDataExportView(View):
    def get(self, requets: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})


class LatestProductsFeed(Feed):
    title = "Shop products (latest)"
    description = "Updates on changes and addition products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return (
            Product.objects
            .select_related("created_by")
            .prefetch_related("images")
            .filter(created_at__isnull=False)
            .order_by("-created_at")[:5]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]


class OrdersListView(ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderCreateView(CreateView):
    model = Order
    fields = "user", "products", "promocode", "delivery_address"
    success_url = reverse_lazy("shopapp:orders_list")


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    model = Order
    fields = "user", "products", "promocode", "delivery_address"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrderDataExportView(View, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.id,
                "products": [product.id for product in order.products.all()]
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})


class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = "shopapp/user_orders.html"

    def get_queryset(self, owner=None, **kwargs):
        self.owner = get_object_or_404(User, pk=self.kwargs['user_id'])
        return Order.objects.select_related('user').prefetch_related('products').filter(user_id=self.owner)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


class OrderCacheExportView(View, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest, **kwargs) -> JsonResponse:
        user_id = get_object_or_404(User, pk=self.kwargs['user_id'])
        print(user_id)
        cache_key = user_id
        orders_data = cache.get(cache_key)
        orders = Order.objects.filter(user_id=user_id).order_by("pk")
        if orders_data is None:
            orders_data = [
                {
                    "pk": order.pk,
                    "address": order.delivery_address,
                    "promocode": order.promocode,
                    "user": order.user.id,
                    "products": [product.id for product in order.products.all()]
                }
                for order in orders
            ]
            cache.set(cache_key, orders_data, 3000)
        return JsonResponse({"orders": orders_data})
