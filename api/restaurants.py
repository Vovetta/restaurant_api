from random import randint
from typing import List

from fastapi import APIRouter
from tortoise.functions import Max

from app.models import RestaurantIn, RestaurantOut, RestaurantModel

restaurants_router = APIRouter(
    prefix='/restaurants'
)


@restaurants_router.get('/', response_model=List[RestaurantOut])
async def list_restaurants(limit: int = 10, offset: int = 0) -> List[RestaurantOut]:
    """
    List all restaurants from database

    :param limit: limit of records to loading
    :param offset: pagination parameter to start loading records from that point
    :return: list of restaurants
    """
    return await RestaurantModel.filter().limit(limit).offset(offset)


@restaurants_router.post('/', response_model=RestaurantOut)
async def create_restaurant(data: RestaurantIn) -> RestaurantOut:
    """
    Creates a restaurant from user input data

    :param data: new restaurant data
    :return: new restaurant
    """
    return await RestaurantModel.create(**data.dict(exclude_unset=True))


@restaurants_router.get('/random', response_model=RestaurantOut)
async def random_restaurant() -> RestaurantOut:
    """
    Random choice of a restaurant

    :return: random restaurant
    """
    row = await RestaurantModel.filter().annotate(max_id=Max('id')).first()
    random_index = randint(0, getattr(row, 'max_id', 0) or 0)
    return await RestaurantModel.filter(id__gte=random_index).first()


@restaurants_router.get('/search', response_model=RestaurantOut)
async def get_restaurant_by_name(name: str) -> RestaurantOut:
    """
    Get a restaurant by name

    :param name: name of a restaurant
    :return: restaurant
    :raises DoesNotExist: restaurant doesn't found in database
    """
    return await RestaurantModel.get(name=name)


@restaurants_router.get('/{restaurant_id:int}', response_model=RestaurantOut)
async def get_restaurant(restaurant_id: int) -> RestaurantOut:
    """
    Get a restaurant by id

    :param restaurant_id: id of a restaurant
    :return: restaurant
    :raises DoesNotExist: restaurant doesn't found in database
    """
    return await RestaurantModel.get(id=restaurant_id)


@restaurants_router.put('/{restaurant_id:int}', response_model=RestaurantOut)
async def update_restaurant(restaurant_id: int, data: RestaurantIn) -> RestaurantOut:
    """
    Update a restaurant by id

    :param restaurant_id: id of a restaurant
    :param data: restaurant data for update
    :return: updated restaurant
    :raises DoesNotExist: restaurant doesn't found in database
    """
    restaurant = await RestaurantModel.get(id=restaurant_id)
    await restaurant.update_from_dict(data.dict(exclude_unset=True)).save()
    return restaurant


@restaurants_router.delete('/{restaurant_id:int}', response_model=RestaurantOut)
async def delete_restaurant(restaurant_id: int) -> RestaurantOut:
    """
    Delete a restaurant by id

    :param restaurant_id: id of a restaurant
    :return: deleted restaurant
    :raises DoesNotExist: restaurant doesn't found in database
    """
    restaurant = await RestaurantModel.get(id=restaurant_id)
    await restaurant.delete()
    return restaurant
