from datetime import datetime

from mongoengine import (
    DateTimeField,
    DecimalField,
    Document,
    ListField,
    ReferenceField,
    StringField,
)

from .hostess import Model as Hostess
from .order_item import Model as OrderItem
from .table import Model as Table
from .waiter import Model as Waiter


class Model(Document):
    meta = dict(
        collection="order",
        strict=False,
    )
    table = ReferenceField(Table, required=True)
    waiter = ReferenceField(Waiter, required=True)
    hostess = ReferenceField(Hostess)
    items = ListField(ReferenceField(OrderItem))
    total_amount = DecimalField(required=True, precision=2)
    created_at = DateTimeField(required=True, default=datetime.now)
    payment_method = StringField(required=True)


from ..middlewares.db import Template


class Order(Template):
    def __init__(self):
        super().__init__(Model)
