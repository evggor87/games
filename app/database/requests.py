from sqlalchemy import select
from app.database.models import Platform, Game
from app.database.models import async_session


# Запрос всех платформ
async def get_platforms_db():
    async with async_session() as session:
        platforms = (await session.scalars(select(Platform).order_by(Platform.name))).all()
    return platforms


# Запрос платформы по ID платформы
async def get_platform_by_id_db(platform_id):
    async with async_session() as session:
        platform = await session.scalar(select(Platform).where(Platform.id==platform_id))
    return platform


# Запрос всех игр по ID платформы с отметкой для продажи
async def get_games_by_platform_db(platform_id):
    async with async_session() as session:
        games = (await session.scalars(select(Game).where(Game.platform_id==platform_id, Game.for_sale==True))).all()
    return games


# Запрос регионов по имени игры и с отметкой для продажи
async def get_regions_db(game_name, platform_id):
    async with async_session() as session:
        regions = (await session.scalars(select(Game.region).where(Game.name==game_name, Game.platform_id==platform_id, Game.for_sale==1))).all()
    return regions

# Запрос игр по состоянию и с отметкой для продажи
async def get_games_condition_db(region, game_name, platform_id):
    async with async_session() as session:
        games = (await session.scalars(select(Game).where(Game.region==region, Game.name==game_name, Game.platform_id==platform_id, Game.for_sale==1))).all()
    return games


# Запрос игры по id игры
async def get_game_by_id_db(game_id):
    async with async_session() as session:
        game = await session.scalar(select(Game).where(Game.id==game_id))
    return game



# Админ

# Добавление платформы
async def add_platform_db(name):
    async with async_session() as session:
        try:
            session.add(Platform(name=name))
            await session.commit()
            return True
        except:
            return False


# Добавление игры
async def add_game_db(name, platform_id, region, price, condition, desc, photo, for_sale):
    async with async_session() as session:
        try:
            session.add(Game(name=name, platform_id=platform_id, region=region, price=price,
                            sealed=condition, desc=desc, photos=photo, for_sale=for_sale))
            await session.commit()
            return True
        except:
            return False







# async def delete_platform(platform_id):
#     platform = await session.scalar(select(Platform).where(Platform.id==platform_id))
#     await session.delete(platform)
#     await session.commit()





# async def get_games(platform_id):
#     games = (await session.scalars(select(Game).where(Game.platform_id==platform_id))).all()
#     return games


# async def get_regions(game_name):
#     regions = (await session.scalars(select(Game.region_id).where(Game.name==game_name))).all()
#     return regions
