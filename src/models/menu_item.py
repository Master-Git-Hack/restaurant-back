from mongoengine import DecimalField, Document, ListField, ReferenceField, StringField

from .restaurant import Model as Restaurant


class Model(Document):
    meta = dict(
        collection="menu_item",
        strict=False,
        indexes=["name"],
        ordering=["-name"],
    )
    name = StringField(required=True)
    description = StringField()
    variations = ListField(StringField())
    topings = ListField(StringField())
    price = DecimalField(required=True, precision=2)
    restaurant = ReferenceField(Restaurant, required=True)


from ..middlewares.db import Template


class MenuItem(Template):
    def __init__(self):
        super().__init__(Model)
