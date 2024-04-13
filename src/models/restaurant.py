from datetime import datetime

from mongoengine import Document, StringField

from ..middlewares.db import Template


class Model(Document):
    meta = dict(
        collection="restaurant",
        strict=False,
        indexes=["name"],
        ordering=["-name"],
    )
    name = StringField(index=True, required=True)
    location = StringField(required=True)


from ..middlewares.db import Template


class Restaurant(Template):
    def __init__(self):
        super().__init__(Model)
