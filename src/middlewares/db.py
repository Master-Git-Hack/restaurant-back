from typing import Any, Dict, List, Optional, Set, Tuple, Union

from marshmallow import post_dump
from marshmallow_mongoengine import ModelSchema
from mongoengine import connect, errors
from mongoengine.connection import disconnect
from mongoengine.queryset.base import BaseQuerySet

from .. import config, logger

# from ..utils.dictionaries import deep_merge

######################


def create_schema(
    model,
    schema_args: Optional[List[Tuple[str, Any]]] = None,
    **meta_kwargs: Optional[Dict[str, Any]],
) -> object:
    class Model: ...

    Model = model

    class Schema(ModelSchema):
        """Class for schema.
        Example:
            >>> Schema().dump(model)->dict
            >>> Schema().load(model)
            >>> Schema(many=True).dump(model)->list
            >>> Schema(many=True).load(model)
        Args:
            ModelSchema (class): class for schema.
        Attributes:
            Meta (class): class for schema.
        """

        @post_dump
        def remove_id(self, data, **kwargs):
            if "_id" in data:
                del data["_id"]
            if "id" in data:
                del data["id"]
            return data

        class Meta:
            model = Model
            load_instance = True
            include_relationships = True
            include_fk = True

    if schema_args is not None:
        for key, value in schema_args:
            setattr(Schema, key, value)

    for key, value in meta_kwargs.items():
        setattr(Schema.Meta, key, value)

    return Schema


class Template:
    model = None
    current = None
    schema = None

    def __init__(self, model, schema_args: Optional[List] = [], **schema_kwargs):
        self.model = model
        self.schema = create_schema(
            self.model, **schema_kwargs, schema_args=schema_args
        )
        self.__check_attr()
        connect(host=config.MONGO_URI)

    def __check_attr(self):
        if self.model is None:
            logger.debug("----------> Model is not defined:\n")
        if self.schema is None:
            self.schema = create_schema(model=self.model)
        return True

    def __enter__(self):
        if self.__check_attr():
            connect(host=config.MONGO_URI)
            return self

    def __exit__(self, exc_type, exc_value, traceback):
        disconnect()
        self.current = None

    def get(self, id, to_dict=False, **kwargs):
        self.__check_attr()
        try:
            self.current = self.model.objects(id=id).first()
        except Exception as e:
            logger.bind(payload=str(e)).debug(
                f"----------> Unexpected error:\n {str(e)}"
            )
            self.current = None
        if not self.current:
            return None
        if to_dict:
            return self.to_dict(**kwargs)
        return self.current

    def filter(self, to_dict=False, exclude=None, only=None, **kwargs):
        self.__check_attr()
        try:
            self.current = self.model.objects(**kwargs).first()

        except errors.NotUniqueError as e:
            logger.bind(payload=str(e)).debug(
                f"----------> Index conflict error:\n {str(e)}"
            )
            self.current = None
            # Handle the specific NotUniqueError for index conflicts
        except Exception as e:
            logger.bind(payload=str(e)).debug(
                f"----------> An unexpected error occurred:\n {str(e)}"
            )
            self.current = None
        if not self.current:
            return None
        if to_dict:
            return self.to_dict(exclude=exclude, only=only)
        return self.current

    def filter_group(self, to_list=False, exclude=None, only=None, **kwargs):
        self.__check_attr()
        try:
            self.current = self.model.objects(**kwargs)
        except Exception as e:
            logger.bind(payload=str(e)).debug(
                f"----------> Unexpected error:\n {str(e)}"
            )
            self.current = None
        if not self.current:
            return None
        if to_list:
            return self.to_list(exclude=exclude, only=only)
        return self.current

    def all(self, to_list=False, exclude=None, only=None):
        self.current = self.model.objects
        if not self.current:
            return None
        if to_list:
            return self.to_list(exclude=exclude, only=only)
        return self.current

    def create(self, to_dict=False, exclude=None, **kwargs):
        self.current = self.model(**kwargs)
        if not self.current:
            return None
        try:
            self.current.save()
        except Exception as e:
            logger.bind(payload=str(e)).debug(
                f"----------> Unexpected error at creation:\n {str(e)}"
            )
            self.current = None
        else:
            if to_dict:
                return self.to_dict(exclude=exclude)
            return self.current

    def update(self, id=None, to_dict=False, exclude=None, only=None, **kwargs):
        if id is not None:
            self.current = self.model.objects(id=id).first()
        if not self.current:
            return None
        for key, value in kwargs.items():
            setattr(self.current, key, value)
        try:
            self.current.save()
        except Exception as e:
            logger.bind(payload=str(e)).debug(
                f"----------> Unexpected error at updating:\n {str(e)}"
            )
            self.current = None
        else:
            if to_dict:
                self.to_dict(exclude=exclude, only=only)
            return self.current

    def delete(self, id=None):
        try:
            if id is not None:
                self.current = self.model.objects(id=id).first()
            if self.current is None:
                return None
            result = self.current.delete()
            if result:
                deleted = result[1]
                if deleted > 0:
                    self.current = None
                else:
                    return self.current

            return self.current
        except Exception as e:
            logger.bind(payload=str(e)).debug(
                f"----------> Unexpected error at deleting:\n {str(e)}"
            )
            return self.current

    def to_dict(
        self,
        data: Optional[object] = None,
        exclude: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict:
        self.__check_attr()
        if "many" in kwargs:
            kwargs.pop("many")
        if data is not None:
            self.current = data
        if self.current is None:
            return {}
        if exclude is not None:
            return self.schema(exclude=exclude, **kwargs).dump(self.current)
        return self.schema(**kwargs).dump(self.current)

    def to_list(
        self,
        data: Optional[object] = None,
        exclude: Optional[List[str]] = None,
        **kwargs,
    ) -> List:
        self.__check_attr()
        if data is not None:
            self.current = data
        if self.current is None:
            return []
        if exclude is not None:
            return self.schema(exclude=exclude, many=True, **kwargs).dump(self.current)
        return self.schema(many=True, **kwargs).dump(self.current)

    def flat(self, keys: Optional[Set | List] = None): ...
