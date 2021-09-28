from tortoise import Model

from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields import IntField, CharField


class RestaurantModel(Model):
    id = IntField(pk=True)
    name = CharField(max_length=250, unique=True)


Restaurant = pydantic_model_creator(RestaurantModel, name='Restaurant')
