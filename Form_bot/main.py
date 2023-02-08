from aiogram import Dispatcher, Bot, types, executor

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import TOKEN, main_panel, geneder_panel, admin_id, cancel_btn


storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage = storage)

class Form(StatesGroup):
    name = State()
    age = State()
    gender = State()

@dp.message_handler(commands = 'start')
async def welcome(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.username}, я бот для заполнения формы', reply_markup = main_panel)

@dp.message_handler(content_types = 'text')
async def text_filter(message: types.Message):
    if message.text == '📁заполнить форму📁':
        await bot.send_message(message.from_user.id, 'введите своё имя', reply_markup = cancel_btn)
        await Form.name.set()

#* name setting
# if your message is numeric or lenght of your message is under 2 symbols, then bot
# is gonna ask you to reenter your name
@dp.message_handler(state = Form.name)
async def set_name_func(message: types.Message, state: FSMContext):
    await state.update_data(username = message.from_user.username)
    await state.update_data(name = message.text)
    data = await state.get_data()

    if data['name'].isnumeric() or len(data['name']) < 2:
        await bot.send_message(message.from_user.id, 'введите своё имя')
    
    elif data['name'] == '📛отмена📛':
        await state.finish()
        await welcome(message)
    
    else:
        await bot.send_message(message.from_user.id, 'отлично, теперь введи возраст')
        await Form.next()

#* age setting
# if you are under 18, then you are declined
# if you sent message with letters, then bot is gonna ask you to reenter your age
@dp.message_handler(state = Form.age)
async def set_age(message: types.Message, state: FSMContext):
    await state.update_data(age = message.text)
    data = await state.get_data()

    if data['age'].isnumeric():
        await bot.send_message(message.from_user.id, 'отлично, теперь укажите свой гендер', reply_markup = geneder_panel)
        await Form.next()

    elif data['age'] == '📛отмена📛':
        await state.finish()
        await welcome(message)

    else:
        await bot.send_message(message.from_user.id, 'введите свой возраст')

#* gender ssetting
# if you sent "male" or "female" instead of "🚹" or "🚺", then
# bot is gonna ask you to choose one of the symbols
@dp.message_handler(state = Form.gender)
async def set_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender = message.text)
    data = await state.get_data()

    if data['gender'] == '🚹' or data['gender'] == '🚺':
        # when bot is sending the form to the admin, bot is changin symbols to text
        if data['gender'] == '🚺':
            data['gender'] = 'female'
        else:
            data['gender'] = 'male'

        print(data)

        await bot.send_message(admin_id, f"username: @{data['username']}\nname: {data['name']}\nage: {data['age']}\ngender: {data['gender']}")
        await bot.send_message(message.from_user.id, 'Спасибо что заполнили форму, я отправил вашу анкету админу, при надобности с вами свяжутся', reply_markup = ReplyKeyboardRemove())
        await state.finish()
    
    elif data['gender'] == '📛отмена📛':
        await state.finish()
        await welcome(message)
    
    else:
        await bot.send_message(message.from_user.id, 'выберите вариант ниже', reply_markup = geneder_panel)
        await Form.gender.set()

if __name__ == '__main__':
    executor.start_polling(dp)
#| coded by c0dem
