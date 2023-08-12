from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.keyboards import inline_keyboards as ikb
from app.database.requests import get_platform_by_id_db, get_game_by_id_db

router = Router()


class Main(StatesGroup):
    catalog = State()
    platform = State()
    game = State()
    region = State()
    condition = State()
    product = State()


# /start
@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer(
        text=f'Добро пожаловать, {message.from_user.first_name}',
        reply_markup=await ikb.main())


# Выбран каталог - выбираем платформу
@router.callback_query(F.data == 'catalog')
async def catalog(call: CallbackQuery, state: FSMContext):
    await state.set_state(Main.catalog)
    await call.message.edit_text(
        text='Выберите платформу',
        reply_markup=await ikb.catalog())


# Выбрана платформа - выбираем игру
@router.callback_query(Main.catalog, F.data.startswith('platform_'))
async def platform(call: CallbackQuery, state: FSMContext):
    platform_id = call.data.split('_')[1]
    platform = await get_platform_by_id_db(platform_id)
    await state.set_state(Main.game)
    await state.update_data(platform_id=platform.id, platform_name=platform.name)
    await call.message.edit_text(
        text=f'Вы выбрали {platform.name}\nВыберите игру',
        reply_markup=await ikb.games(platform.id))


# Выбрана игра - выбираем регион
@router.callback_query(Main.game, F.data.startswith('game_'))
async def game(call: CallbackQuery, state: FSMContext):
    game_name = call.data.split('_')[1]
    await state.set_state(Main.region)
    await state.update_data(game_name=game_name)
    data = await state.get_data()
    platform_id = data['platform_id']
    await call.message.edit_text(
        text=f'Вы выбрали игру: {game_name}\nВыберите регион',
        reply_markup=await ikb.regions(game_name, platform_id))


# Выбран регион - выбираем игру по состоянию
@router.callback_query(Main.region, F.data.startswith('region_'))
async def region(call: CallbackQuery, state: FSMContext):
    region = call.data.split('_')[1]
    await state.set_state(Main.condition)
    await state.update_data(region=region)
    data = await state.get_data()
    game_name = data['game_name']
    platform_id = data['platform_id']
    await call.message.edit_text(
        text=f'Вы выбрали регион: {region}\nВыберите игру по состоянию',
        reply_markup=await ikb.conditions(region, game_name, platform_id))


# Выбрана игра по состонию - получаем карточку товара
@router.callback_query(Main.condition, F.data.startswith('game_'))
async def condition(call: CallbackQuery, state: FSMContext):
    game_id = call.data.split('_')[1]
    await state.set_state(Main.product)
    game = await get_game_by_id_db(game_id)
    platform = await get_platform_by_id_db(game.platform_id)
    await call.message.edit_text(
        text=f'Платформа - {platform.name}\n'
             f'Игра - {game.name}\n'
             f'Стоимость - {game.price}\n'
             f'Регион - {game.region}\n'
             f'Состояние - {game.condition}\n\n'
             f'Описание - {game.desc}\n\n')
