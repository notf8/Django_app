from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def product_preview_directory(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(null=False, blank=True, verbose_name=_("Description"))
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=_("Price"))
    discount = models.SmallIntegerField(default=0, verbose_name=_("Discount"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("Created by"))
    archived = models.BooleanField(default=False, verbose_name=_("Archived"))
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory, verbose_name=_("Preview"))

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.name!r})"

    def get_absolute_url(self):
        return reverse("shopapp:product_details", kwargs={"pk": self.pk})


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name=_("Product"))
    image = models.ImageField(upload_to=product_images_directory_path, verbose_name=_("Image"))
    description = models.CharField(max_length=200, null=False, blank=True, verbose_name=_("Description"))


class Order(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    delivery_address = models.TextField(null=True, blank=True, verbose_name=_("Delivery address"))
    promocode = models.CharField(max_length=20, null=False, blank=True, verbose_name=_("Promocode"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("User"))
    products = models.ManyToManyField(Product, related_name="orders", verbose_name=_("Products"))
