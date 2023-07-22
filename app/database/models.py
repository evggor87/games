from datetime import datetime
from turtle import back
from sqlalchemy import ForeignKey, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from config import SQLALCHEMY_URL, SQLALCHEMY_ECHO

engine = create_engine(url=SQLALCHEMY_URL, echo=SQLALCHEMY_ECHO)
Session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int]
    name: Mapped[str] = mapped_column(String(32))

    orders: Mapped['Order'] = relationship(back_populates='user')


class Banned(Base):
    __tablename__ = 'banned'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int]


class Platform(Base):
    __tablename__ = 'platforms'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))

    consoles: Mapped['Console'] = relationship(back_populates='platform')


class Console(Base):
    __tablename__ = 'consoles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    platform_id: Mapped[int] = mapped_column(ForeignKey('platforms.id'))

    platform: Mapped['Platform'] = relationship(back_populates='consoles')
    regions: Mapped['Region'] = relationship(back_populates='console')
    games: Mapped['Game'] = relationship(back_populates='console')


class Region(Base):
    __tablename__ = 'regions'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    console_id: Mapped[int] = mapped_column(ForeignKey('consoles.id'))

    console: Mapped['Console'] = relationship(back_populates='regions')
    games: Mapped['Game'] = relationship(back_populates='region')


class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    region_id: Mapped[int] = mapped_column(ForeignKey('regions.id'))
    console_id: Mapped[int] = mapped_column(ForeignKey('consoles.id'))
    price: Mapped[int]
    sealed: Mapped[bool]
    for_sale: Mapped[bool]
    desc: Mapped[str]

    region: Mapped['Region'] = relationship(back_populates='games')
    console: Mapped['Console'] = relationship(back_populates='games')
    order: Mapped['Order'] = relationship(back_populates='game')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_num: Mapped[str] = mapped_column(String(12))
    date: Mapped[datetime]
    state: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    game_id: Mapped[int] = mapped_column(ForeignKey('games.id'))

    user: Mapped['User'] = relationship(back_populates='orders')
    game: Mapped['Game'] = relationship(back_populates='order')


async def create_base():
    Base.metadata.create_all(bind=engine)
