from mongoengine import Document, StringField

from ..middlewares.db import Template


class Model(Document):
    meta = dict(
        collection="role",
        strict=False,
        indexes=["name"],
        ordering=["-name"],
    )
    name = StringField(index=True, required=True, unique=True)


from ..middlewares.db import Template


class Role(Template):
    def __init__(self):
        super().__init__(Model)
