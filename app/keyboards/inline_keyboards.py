from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import (get_platforms_db, get_games_by_platform_db, get_regions_db,
                                   get_games_condition_db)


# Главное меню
async def main():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Каталог", callback_data="catalog"))
    kb.add(InlineKeyboardButton(text="Поиск", callback_data="find"))
    kb.add(InlineKeyboardButton(text="Контакты", callback_data="contacts"))
    kb.adjust(1)
    return kb.as_markup()


# Подтверждение
async def confirm():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Да', callback_data='True'))
    kb.add(InlineKeyboardButton(text='Нет', callback_data='False'))
    kb.adjust(1)
    return kb.as_markup()


# Все платформы
async def platforms():
    kb = InlineKeyboardBuilder()
    all_platforms = await get_platforms_db()
    for platform in all_platforms:
        kb.row(InlineKeyboardButton(
            text=platform.name,
            callback_data=f'platform_{platform.id}')
        )
    kb.adjust(1)
    return kb.as_markup()


# Каталог - все платформы у которых есть игры с отметкой в продажу
async def catalog():
    kb = InlineKeyboardBuilder()
    all_platforms = await get_platforms_db()
    for platform in all_platforms:
        games = await get_games_by_platform_db(platform.id)
        if games:
            kb.row(InlineKeyboardButton(
                text=platform.name,
                callback_data=f'platform_{platform.id}')
            )
    kb.adjust(2)
    return kb.as_markup()


# Игры - все по выбранной платформе (одно имя игры - одна кнопка) с отметкой в продажу
async def games(platform_id):
    kb = InlineKeyboardBuilder()
    games = await get_games_by_platform_db(platform_id)
    games_list = []
    for game in games:
        if game.name not in games_list:
            games_list.append(game.name)
    for game in games_list:
        kb.row(InlineKeyboardButton(
            text=game,
            callback_data=f'game_{game}')
        )
    kb.adjust(1)
    return kb.as_markup()


# Регионы - по названию игры и выбранной платформе (одно имя региона - одна кнопка)
async def regions(game_name, platform_id):
    kb = InlineKeyboardBuilder()
    regions = await get_regions_db(game_name, platform_id)
    regions_list = []
    for region in regions:
        if region not in regions_list:
            regions_list.append(region)
    for region in regions_list:
        kb.row(InlineKeyboardButton(
            text=region,
            callback_data=f'region_{region}')
        )
    kb.adjust(1)
    return kb.as_markup()


# игры по состоянию
async def conditions(region, game_name, platform_id):
    kb = InlineKeyboardBuilder()
    games = await get_games_condition_db(region, game_name, platform_id)
    for game in games:
        kb.row(InlineKeyboardButton(
            text=f'{game.name} ({game.condition}) - {game.price} руб. ',
            callback_data=f'game_{game.id}')
        )
    kb.adjust(1)
    return kb.as_markup()


# Карточка товара



# Админ-панель
async def categories():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Платформа", callback_data="platform"))
    kb.add(InlineKeyboardButton(text="Игра", callback_data="game"))
    kb.adjust(1)
    return kb.as_markup()