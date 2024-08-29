import abc
from sqlalchemy.ext.asyncio import AsyncSession
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
    async def update_one(self, id, values):
        raise NotImplemented()

    @abc.abstractmethod
    async def get_all_by_filter(self, filters, limit, order):
        raise NotImplemented()

    @abc.abstractmethod
    async def get_all(self, limit):
        raise NotImplemented

    @abc.abstractmethod
    async def get_last(self, filters):
        raise NotImplemented


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            session: AsyncSession

            stmt = insert(self.model).values(data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()

    async def delete_one(self, id):
        async with async_session_maker() as session:
            session: AsyncSession

            stmt = delete(self.model).where(self.model.id == id)
            await session.execute(stmt)
            await session.commit()

    async def get_one(self, filters):
        async with async_session_maker() as session:
            session: AsyncSession

            stmt = select(self.model).where(*filters)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def mark_as_delete(self, id):
        async with async_session_maker() as session:
            session: AsyncSession

            stmt = update(self.model).where(self.model.id == id).values(is_delete=True)
            await session.execute(stmt)
            await session.commit()

    async def update_one(self, id, values):
        async with async_session_maker() as session:
            session: AsyncSession

            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(values)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()

    async def get_all_by_filter(self, filters, limit, order):
        async with async_session_maker() as session:
            session: AsyncSession

            if limit > 0:
                stmt = select(self.model).where(*filters).order_by(order).limit(limit)
            if limit == 0:
                stmt = select(self.model).where(*filters).order_by(order)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def get_all(self, limit):
        async with async_session_maker() as session:
            session: AsyncSession

            stmt = select(self.model).limit(limit)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def get_last(self, filters):
        async with async_session_maker() as session:
            session: AsyncSession

            if filters:
                stmt = (
                    select(self.model)
                    .where(*filters)
                    .order_by(self.model.id.desc())
                    .limit(1)
                )
            else:
                stmt = select(self.model).order_by(self.model.id.desc()).limit(1)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()
