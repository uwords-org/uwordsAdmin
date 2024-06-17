import abc
from sqlalchemy import insert, select, delete, update
from src.database.db_config import async_session_maker


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    async def add_one(self, data: dict):
        raise NotImplemented()

    @abc.abstractmethod
    async def get_one(self, filters):
        raise NotImplemented()

    @abc.abstractmethod
    async def delete_one(self, id):
        raise NotImplemented()

    @abc.abstractmethod
    async def mark_as_delete(self, id):
        raise NotImplemented()

    @abc.abstractmethod
    async def get_all_by_filter(self, filters, limit, order):
        raise NotImplemented()

    @abc.abstractmethod
    async def get_all(self, limit):
        raise NotImplemented


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(data)
            await session.execute(stmt)
            await session.commit()

    async def delete_one(self, id):
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == id)
            await session.execute(stmt)
            await session.commit()

    async def get_one(self, filters):
        async with async_session_maker() as session:
            stmt = select(self.model).filter(filters)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def mark_as_delete(self, id):
        async with async_session_maker() as session:
            stmt = update(self.model).where(self.model.id == id).value(is_delete=True)
            await session.execute(stmt)
            await session.commit()

    async def get_all_by_filter(self, filters, limit, order):
        async with async_session_maker() as session:
            if limit > 0:
                stmt = select(self.model).filter(*filters).order_by(order).limit(limit)
            if limit == 0:
                stmt = select(self.model).filter(*filters).order_by(order)
            res = await session.execute(stmt)
            res = [row[0] for row in res.all()]
            return res

    async def get_all(self, limit):
        async with async_session_maker() as session:
            stmt = select(self.model).limit(limit)
            res = await session.execute(stmt)
            res = [row[0] for row in res.all()]
            return res