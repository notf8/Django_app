from csv import DictReader
from io import TextIOWrapper
from shopapp.models import Order, Product


def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)
    product_pk = [product.pk for product in Product.objects.all()]
    orders = [
        Order(**row, user_id=1)
        for row in reader
    ]
    instance = Order.objects.bulk_create(orders)
    for order in instance:
        order.products.set(product_pk)

    return instance
