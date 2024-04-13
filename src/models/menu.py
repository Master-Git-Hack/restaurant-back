from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    ListField,
    ReferenceField,
    StringField,
)

from .menu_item import Model as MenuItem
from .restaurant import Model as Restaurant


class Model(Document):
    name = StringField(required=True)
    items = ListField(ReferenceField(MenuItem))
    restaurant = ReferenceField(Restaurant, required=True)
    created_at = DateTimeField(required=True, default=datetime.now)
    enabled = BooleanField(required=True, defaulf=True)
