from mongoengine import DecimalField, Document, ReferenceField

from .menu_item import Model as MenuItem


class Model(Document):
    meta = dict(
        collection="order_item",
        strict=False,
    )
    menu_item = ReferenceField(MenuItem, required=True)
    quantity = DecimalField(required=True, precision=2)


from ..middlewares.db import Template


class OrderItem(Template):
    def __init__(self):
        super().__init__(Model)
