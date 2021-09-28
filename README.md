# Restaurant API test

Web application with restaurant API

## Starting service

- Install requirements
- Copy `config.yaml.example` -> `config.yaml` and fill params
- Test: `pytest` in project root directory
- Start: `python main.py`

## Service technologies

- Language: *Python 3.8*
- Framework: *FastApi*
- ORM: *Tortoise*
- Database: *SQLite*
- Tests: *PyTest*

## Future improvements

1. Improve and change a random system (now it's not really good)
2. Migrate from `SQLite` to `PostgresQL`
3. Add more logging, logging to file and rethink log format
4. Add dynamic loading of routers from api directory
5. Add migrations with `Aerich`
6. Dockerize a service
7. Add more tests
