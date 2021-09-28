from app.service import service
from asyncio import run
from hypercorn.asyncio import serve, Config
from config import Service


def create_config() -> Config:
    config = Config()
    config.bind = f'{Service.host}:{Service.port}'

    return config


if __name__ == '__main__':
    run(serve(service, config=create_config()))
