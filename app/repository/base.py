from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.database import async_session_maker


class BaseRepo:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_flush(cls, session, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def find_last_n(cls, limit: int = 10, **filter_by):
        """
        Получить последние N записей, отсортированных по created_at (по убыванию)

        Args:
            limit: количество записей для возврата
            filter_by: дополнительные фильтры
        """
        async with async_session_maker() as session:
            # Проверяем, есть ли у модели поле created_at
            if not hasattr(cls.model, "created_at"):
                raise HTTPException(
                    status_code=400,
                    detail=f"Model {cls.model.__name__} doesn't have created_at field",
                )

            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .order_by(desc(cls.model.created_at))
                .limit(limit)
            )

            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def update(cls, filter, values):
        async with async_session_maker() as session:
            async with session.begin():
                instance = await cls.find_one_or_none_flush(**filter, session=session)
                if not instance:
                    raise HTTPException(status_code=404, detail="not found")
                for var, value in values.items():
                    setattr(instance, var, value) if value else None

                session.add(instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return instance

    @classmethod
    async def delete(cls, p_id):
        async with async_session_maker() as session:
            async with session.begin():
                hero = await session.get(cls.model, p_id)
                if not hero:
                    raise HTTPException(status_code=404, detail="Hero not found")
                await session.delete(hero)
                return {"ok": True}
