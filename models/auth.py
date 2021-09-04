from models import model
from db import DB


class CRUDBase:
    @staticmethod
    async def execute(query, *args, **kwargs):
        async with DB() as db:
            result = await db.execute(query, *args, **kwargs)
        return result


class Auth(CRUDBase):
    def __init__(self, user_id):
        self.user_id = user_id

    async def get(self):
        q = model.auth.select().where(self.user_id == model.auth.c.id)
        result = await self.execute(q)
        return await result.fetchone()

    async def set(self, **kwargs):
        q = model.auth.update(None).where(
            self.user_id == model.auth.c.id
        ).values(**kwargs)
        await self.execute(q)
        return self

    async def delete(self):
        q = model.auth.delete(None).where(self.user_id == model.auth.c.id)
        await self.execute(q)
        return self

    @classmethod
    async def create(cls, user_id):
        q = model.auth.insert(None).values(id=user_id)
        guild = cls(user_id)
        await cls.execute(q)
        return guild

    @staticmethod
    async def get_all(cls):
        q = model.auth.select()
        results = await cls.execute(q)
        return await results.fetchall()