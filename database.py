from aiogram import types, bot

from gino import Gino
from sqlalchemy import (Column, Integer, BigInteger, String, Sequence, TIMESTAMP, Boolean, JSON)
from sqlalchemy import sql
from gino.schema import GinoSchemaVisitor
from config import DB_USER, DB_PASS, HOST


db = Gino()


class User(db.Model):
    __tablename__ = "users"
    query: sql.Select

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(Integer)
    username = Column(String(50))
    full_name = Column(String(100))
    language = Column(String(2))


class Item(db.Model):
    __tablename__ = "items"
    query: sql.Select

    id = Column(Integer, Sequence("item_id_seq"), primary_key=True)
    name = Column(String(100))
    photo = Column(String(300))
    price = Column(BigInteger)
    category = Column(String(30))


class Purchase(db.Model):
    __tablename__ = "purchases"
    query: sql.Select

    id = Column(Integer, Sequence("purchase_id_seq"), primary_key=True)
    buyer = Column(Integer)
    item_id = Column(Integer)
    amount = Column(Integer)
    quantity = Column(Integer)
    purchase_time = Column(TIMESTAMP)
    shipping_address = Column(JSON)
    shipping_phone_number = Column(String(30))
    receiver = Column(String(100))
    text = Column(String(300))
    successful = Column(Boolean, default=False)


class DBCommands:
    async def get_user(self, user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def add_user(self) -> User:
        user = types.User.get_current()
        user_exists = await self.get_user(user.id)
        if user_exists:
            return user_exists
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name
        await new_user.create()
        return new_user

    async def set_language(self, language):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(language=language).apply()

    async def count_users(self):
        total = await db.func.count(User.user_id).gino.scalar()
        return total

    async def show_items(self, category):
        items = await Item.query.where(Item.category == category).gino.all()
        return items

    async def delete_item(self, item_id):
        deleted_item = await Item.delete.where(Item.id == item_id).gino.status()
        return deleted_item


async def create_db():
    await db.set_bind(f"postgresql://{DB_USER}:{DB_PASS}@{HOST}/gino")
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()
