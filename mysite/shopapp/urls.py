from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    ShopIndexView,
    ProductsListView,
    ProductDetailsView,
    OrdersListView,
    OrderDetailView,
    OrderCreateView,
    OrderDeleteView,
    OrderUpdateView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductsDataExportView,
    OrderDataExportView,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed,
    UserOrdersListView,
    OrderCacheExportView,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)


urlpatterns = [
    path("", ShopIndexView.as_view(), name="shop_index"),
    path("api/", include(routers.urls)),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/export/", ProductsDataExportView.as_view(), name="products-export"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/latest/feed/", LatestProductsFeed(), name="products-feed"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/export", OrderDataExportView.as_view(), name="orders-export"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/confirm-delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("orders/<int:pk>/confirm-update/", OrderUpdateView.as_view(), name="order_update"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user_orders"),
    path("users/<int:user_id>/orders/export", OrderCacheExportView.as_view(), name="orders-export-cached"),
]