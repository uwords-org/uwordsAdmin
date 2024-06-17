# Uwords Admin API


Чтобы сделать миграцию к БД, нужно прописать в контейнере docker следующую команду
```shell
alembic -c src/alembic.ini revision --autogenerate -m "комментарий для миграции"
```

Применить миграции
```shell
alembic -c src/alembic.ini upgrade head
```
