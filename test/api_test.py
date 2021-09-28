from asyncio import gather
from collections import Generator

from fastapi.testclient import TestClient
from pytest import fixture

from app.models import RestaurantModel
from config import Sqlite

Sqlite.database = ':memory:'


@fixture(scope='module')
def client() -> Generator:
    from app.service import service

    with TestClient(service) as client:
        client.task.get_loop().run_until_complete(
            gather(
                RestaurantModel.create(name='First'),
                RestaurantModel.create(name='Second'),
                RestaurantModel.create(name='Third')
            )
        )
        yield client


def test_list_restaurants(client: TestClient):
    # Successful `list` operation
    response = client.get('/restaurants')
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'name': 'First'},
        {'id': 2, 'name': 'Second'},
        {'id': 3, 'name': 'Third'}
    ]


def test_get_restaurant(client: TestClient):
    # Successful `get` operation
    response = client.get('/restaurants/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'First'}

    # Successful `get` operation
    response = client.get('/restaurants/4')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Object does not exist'}


def test_create_restaurant(client: TestClient):
    # Successful `create` operation
    response = client.post('/restaurants/', json={'name': 'Fourth'})
    assert response.status_code == 200
    assert response.json() == {'id': 4, 'name': 'Fourth'}

    # Unsuccessful `create` operation
    response = client.post('/restaurants/', json={'name': 'First'})
    assert response.status_code == 422


def test_update_restaurant(client: TestClient):
    # Successful `update` operation
    response = client.put('/restaurants/1', json={'name': 'Updated First'})
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'Updated First'}


def test_delete_restaurant(client: TestClient):
    # Successful `delete` operation
    response = client.delete('/restaurants/2')
    assert response.status_code == 200
    assert response.json() == {'id': 2, 'name': 'Second'}

    # Unsuccessful `delete` operation
    response = client.get('/restaurants/2')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Object does not exist'}


def test_search_restaurant(client: TestClient):
    # Successful `search by name` operation
    response = client.get('/restaurants/search?name=Third')
    assert response.status_code == 200
    assert response.json() == {'id': 3, 'name': 'Third'}

    # Unsuccessful `search by name` operation
    response = client.get('/restaurants/search?name=Zero')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Object does not exist'}
