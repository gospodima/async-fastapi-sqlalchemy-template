from copy import deepcopy
from typing import Any, Optional, TypeVar

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

AnyModel = TypeVar("AnyModel", bound=BaseModel)


def partial_model(model: type[AnyModel]) -> type[AnyModel]:
    """Decorator function used to modify a pydantic model's fields to all be optional.

    Taken from https://stackoverflow.com/a/76560886/19129261
    """

    def make_field_optional(
        field: FieldInfo, default: Any = None
    ) -> tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new

    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{  # type: ignore
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        },
    )
