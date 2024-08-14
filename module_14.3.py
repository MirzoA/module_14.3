from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Информация'),
         KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Купить')]
    ], resize_keyboard=True)
buy_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Клей для пенополистирола ZM-01', callback_data='product_buying1')],
        [InlineKeyboardButton(text='Клей для плитки ZM-51', callback_data='product_buying2')],
        [InlineKeyboardButton(text='Клей для блоков ZM-22', callback_data='product_buying3')],
        [InlineKeyboardButton(text='Штукатурка гладкая цементно-известковая ZM-41', callback_data='product_buying4')],
    ]
)
calclulate_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
         InlineKeyboardButton(text='Формула расчёта', callback_data='formula')]
    ]
)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    images = [
        'Клей для пенополистирола ZM-01.png',
        'Клей для плитки ZM-51.png',
        'Клей для блоков ZM-22.png',
        'Штукатурка гладкая цементно-известковая ZM-41.png',
    ]
    texts = [
        'Клей для пенополистирола ZM-01, Цена 417 ₽/шт',
        'Клей для плитки ZM-51, Цена 353 ₽/шт',
        'Клей для блоков ZM-22, Цена 384 ₽/шт',
        'Штукатурка гладкая цементно-известковая ZM-41, Цена 395 ₽/шт'
    ]
    for i, t in zip(images, texts):
        with open(i, 'rb') as img:
            await message.answer_photo(img, t)
    await message.answer("Выберите продукт для покупки:", reply_markup=buy_menu)

@dp.callback_query_handler(text="product_buying1")
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели Клей для пенополистирола ZM-01')
    await call.answer()

@dp.callback_query_handler(text="product_buying2")
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели Клей для плитки ZM-51')
    await call.answer()

@dp.callback_query_handler(text="product_buying3")
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели Клей для блоков ZM-22')
    await call.answer()

@dp.callback_query_handler(text="product_buying4")
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели Штукатурка гладкая цементно-известковая ZM-41')
    await call.answer()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=calclulate_menu)


@dp.message_handler(commands=['start'])
async def start_message(message):
    print("Бот запущен")
    await message.answer(f"Привет!, {message.from_user.username}.  Я бот помогающий твоему здоровью.",
                         reply_markup=start_menu)

@dp.message_handler()
async def all_message(message):
    print('Мы получили новое сообщение')
    await message.answer('Введите команду /start, чтобы начать общение.')

@dp.callback_query_handler(text='formula')
async def set_formul(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer("Введите свой рост в сантиметрах:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer("Введите свой вес в килограммах:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = int(data['weight']) * 10 + int(data['growth']) * 6.25 - int(data['age']) * 5 + 5
    await message.answer(f"Ваша норма калорий: {calories}")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)