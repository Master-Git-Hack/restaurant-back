from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmailField,
    ImageField,
    ReferenceField,
    StringField,
)

from ..middlewares.db import Template
from .role import Model as Role


class Model(Document):
    meta = dict(
        collection="user",
        strict=False,
        indexes=["username"],
        ordering=["-username"],
    )
    username = EmailField(
        index=True,
        unique=True,  # Hace que el campo sea único
        required=True,
        error_messages={
            "unique": "User already exists.",  # Mensaje de error para valores duplicados
        },
    )
    names = StringField(required=True)
    last_names = StringField(required=True)
    password = StringField(required=True)
    created_at = DateTimeField(required=True, default=datetime.now)
    enabled = BooleanField(required=True, default=True)
    password_change_needed = BooleanField(default=False)
    password_changed_date = DateTimeField()
    picture = ImageField()
    role = ReferenceField(Role, required=True)


class User(Template):
    def __init__(self):
        super().__init__(Model)
