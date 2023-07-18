from sqlalchemy import ForeignKey, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from app.config import SQLALCHEMY_URL, SQLALCHEMY_ECHO


engine = create_engine(url=SQLALCHEMY_URL, echo=SQLALCHEMY_ECHO)
Session = sessionmaker(engine)
session = Session()

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int]
    name: Mapped[str] = mapped_column(String(32))


class Platform(Base):
    __tablename__ = 'platforms'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))


class Console(Base):
    __tablename__ = 'consoles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    platform_id: Mapped[int] = mapped_column(ForeignKey('platforms.id'))


class Region(Base):
    __tablename__ = 'regions'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    console_id: Mapped[int] = mapped_column(ForeignKey('consoles.id'))


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



async def create_base():
    Base.metadata.create_all(bind=engine)