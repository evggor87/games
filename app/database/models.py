from typing import List
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


engine = create_async_engine("sqlite+aiosqlite:///db.sqlite3", echo=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(32))

    def __repr__(self):
        return f'id:{self.id}; tg_id:{self.tg_id}; name:{self.name}'


class Banned(Base):
    __tablename__ = 'banned'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

    def __repr__(self):
        return f'id:{self.id}; tg_id:{self.tg_id}'


class Platform(Base):
    __tablename__ = 'platforms'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))

    games: Mapped[List['Game']] = relationship(back_populates='platform', cascade='all, delete')

    def __repr__(self):
        return f'id:{self.id}; name:{self.name}'


class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    platform_id: Mapped[int] = mapped_column(ForeignKey('platforms.id', ondelete='CASCADE'))
    region: Mapped[str] = mapped_column(String(32))
    price: Mapped[int]
    condition: Mapped[str]
    desc: Mapped[str]
    photos: Mapped[str]
    amount: Mapped[int]
    for_sale: Mapped[bool]

    platform: Mapped[Platform] = relationship(back_populates='games')

    def __repr__(self):
        return f'id:{self.id}; name:{self.name}; platform_id:{self.platform_id}; region:{self.region}; price:{self.price}; sealed:{self.sealed}; for_sale:{self.for_sale}'


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
