from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.keyboards import inline_keyboards as ikb
from app.database.requests import add_platform_db, add_game_db

admin = Router()


class AdminPanel(StatesGroup):
    # add
    add = State()
    # add - platform
    add_platform = State()
    # add - game
    add_game = State()
    add_game_platform = State()
    add_game_name = State()
    add_game_price = State()
    add_game_region = State()
    add_game_condition = State()
    add_game_desc = State()
    add_game_photo = State()
    add_game_amount = State()


@admin.message(Command('admin'))
async def admin_panel(message: Message):
    await message.answer(
        text='<b>Памятка: Админ-команды</b>\n\n'
             '/add - Добавить данные\n\n'
             '/change - Изменить данные\n\n'
             '/del - Удалить данные\n\n'
             '/price - Прайс-лист\n\n'
             '/post - Рассылка\n\n'
             '/ban - Забанить пользователя\n\n'
             '/set - Настройки')


# ADD - Выбор категории
@admin.message(F.text == '/add')
async def add(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.add)
    await message.answer(
        text='Выберите категорию',
        reply_markup=await ikb.categories())


# ADD - Добавление платформы
@admin.callback_query(AdminPanel.add, F.data=='platform')
async def add_platform(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminPanel.add_platform)
    await call.message.answer(text='Напишите название платформы:')


# ADD - platform - Получено название платформы и сохранение в БД
@admin.message(AdminPanel.add_platform)
async def add_platform_confirm(message: Message, state: FSMContext):
    result = await add_platform_db(message.text)
    if result:
        await message.answer(text=f'Платформа "{message.text}" Добавлена!')
    else:
        await message.answer(text='Ошибка! Попробуйте снова')
    await state.clear()


# ADD - Добавление игры
@admin.callback_query(AdminPanel.add, F.data=='game')
async def add_game(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminPanel.add_game)
    await call.message.answer(
        text='Выберите платформу:',
        reply_markup=await ikb.platforms())


# ADD - game - выбрана платформа
@admin.callback_query(AdminPanel.add_game, F.data.startswith('platform_'))
async def add_game_platform(call: CallbackQuery, state:FSMContext):
    await state.set_state(AdminPanel.add_game_platform)
    platform_id = call.data.split('_')[1]
    await state.update_data(platform_id=platform_id)
    await call.message.answer(text='Напишите название игры:')


# ADD - game - получено наименование
@admin.message(AdminPanel.add_game_platform)
async def add_game_name(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.add_game_name)
    await state.update_data(name=message.text)
    await message.answer(text='Напишите стоимость игры:')


# ADD - game - Получена стоимость
@admin.message(AdminPanel.add_game_name)
async def add_game_price(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.add_game_price)
    await state.update_data(price=message.text)
    await message.answer(text='Напишите регион:')


# ADD - game - Получен регион
@admin.message(AdminPanel.add_game_price)
async def add_game_region(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.add_game_region)
    await state.update_data(region=message.text)
    await message.answer(text='Напишите состояние игры:')


 # ADD - game - Получено состояние игры
@admin.message(AdminPanel.add_game_region)
async def add_game_condition(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.add_game_condition)
    await state.update_data(condition=message.text)
    await message.answer(text='Напишите описание игры:')


 # ADD - game - Получено описание игры
@admin.message(AdminPanel.add_game_condition)
async def add_game_desc(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.add_game_desc)
    await state.update_data(desc=message.text)
    await message.answer(text='Добавьте фотографию игры:')


 # ADD - game - Получена фотография
@admin.message(F.photo, AdminPanel.add_game_desc)
async def add_game_photo(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.add_game_photo)
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer(text='Напишите количество:')


 # ADD - game - Получено количество
@admin.message(AdminPanel.add_game_photo)
async def add_game_amount(message: Message, state: FSMContext):
    await state.set_state(AdminPanel.add_game_amount)
    await state.update_data(amount=message.text)
    await message.answer(
        text='Добавить в продажу?',
        reply_markup=await ikb.confirm())


 # ADD - game - Получена отметка для продажи и сохранение в БД
@admin.callback_query(AdminPanel.add_game_amount)
async def add_game_sale(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    result = await add_game_db(
        data['name'], data['platform_id'], data['region'], data['price'], data['condition'],
        data['desc'], data['photo'], int(data['amount']), data['for_sale'])
    if result:
        await call.message.answer('Игра добавлена')
    else:
        await call.message.answer('Ошибка! Попробуйте снова')
    await state.clear()