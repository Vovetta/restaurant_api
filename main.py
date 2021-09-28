from asyncio import run

from hypercorn.asyncio import serve, Config

from app.service import service
from config import Service


def create_config() -> Config:
    config = Config()
    config.bind = f'{Service.host}:{Service.port}'
    config.accesslog = '-'
    config.errorlog = '-'

    return config


if __name__ == '__main__':
    run(serve(service, config=create_config()))
