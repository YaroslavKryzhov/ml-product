from pydantic import BaseModel
from humps import camelize


def to_camel(string):
    return camelize(string)


class CoreSchema(BaseModel):
    """
    Any common logic to be shared by all models goes here.
    """
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class IDModelMixin(BaseModel):
    id: int
