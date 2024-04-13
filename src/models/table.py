from datetime import datetime

from mongoengine import Document, IntField, ReferenceField, StringField

from ..middlewares.db import Template
from .restaurant import Model as Restaurant


class Model(Document):
    meta = dict(
        collection="table",
        strict=False,
    )
    number = StringField(required=True)
    restaurant = ReferenceField(Restaurant, required=True)


from ..middlewares.db import Template


class Table(Template):
    def __init__(self):
        super().__init__(Model)
