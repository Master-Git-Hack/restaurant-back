from mongoengine import DecimalField, Document, ListField, ReferenceField, StringField

from .restaurant import Model as Restaurant


class Model(Document):
    meta = dict(
        collection="inventory_item",
        strict=False,
        indexes=["name"],
        ordering=["-name"],
    )
    name = StringField(required=True)
    variations = ListField(StringField())
    quantity = DecimalField(required=True, precision=2)
    restaurant = ReferenceField(Restaurant, required=True)


from ..middlewares.db import Template


class InventoryItem(Template):
    def __init__(self):
        super().__init__(Model)
