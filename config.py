from inspect import getmembers, isclass
from sys import modules

from yaml import safe_load, YAMLError

from app.exceptions import ServiceException

CONFIG_FILE = 'config.yaml'


class Service:
    """Service configuration"""
    host: str
    port: int
    debug: bool


class Sqlite:
    """Sqlite database configuration"""
    database: str


def load_config() -> None:
    """Loads app config from YAML config file"""
    with open(CONFIG_FILE, 'r') as file:
        try:
            config = safe_load(file)
        except YAMLError as e:
            raise ServiceException(f'Check config file: {CONFIG_FILE}') from e

    classes = getmembers(modules[__name__], lambda member: isclass(member) and member.__module__ == __name__)
    for class_name, class_object in classes:
        for key, value in config[class_name].items():
            setattr(class_object, key, value)


load_config()
