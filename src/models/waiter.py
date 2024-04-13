from mongoengine import Document, ReferenceField

from .restaurant import Model as Restaurant
from .user import Model as User


class Model(Document):
    meta = dict(
        collection="waiter",
        strict=False,
        indexes=["user"],
        ordering=["-user"],
    )
    user = ReferenceField(User, required=True)
    restaurant = ReferenceField(Restaurant, required=True)


from ..middlewares.db import Template


class Waiter(Template):
    def __init__(self):
        super().__init__(Model)
