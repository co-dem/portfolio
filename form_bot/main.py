from aiogram.utils import executor
from aiogram import Dispatcher, types, Bot
from aiogram.types import ReplyKeyboardRemove 

from btns import skip_btn, blog_link, rew_link, grades
from config import TOKEN, REWIES_ID, BLOG_ID, CURSES, DEV_ID

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage = storage)

class Form(StatesGroup):
    skiper = State()

    form_header = State()
    main_text = State()
    sharp = State()

@dp.message_handler(commands = 'send_rew')
async def make_a_new_rew(message: types.Message):
    await bot.send_message(message.from_user.id, 'для того чтобы оставить ещё отзыв, нажмите кнопку продолжить ниже', reply_markup = skip_btn)
    await Form.skiper.set()

@dp.message_handler(commands = 'help')
async def help_func(message: types.Message):
    await bot.send_message(message.from_user.id, '/send_rew - чтобы оставить новый отзыв\n/help - чтобы увидеть список команд\n\nпри необходимости вы можете связаться с разработчиком: @c0dem')

@dp.message_handler(commands = 'start')
async def welcome(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет! Я телеграм бот для оставления отзывов🥳\n\nочень надеюсь что вам понравился наш продукт и вы будете рады рассказать о нас своим знакомым и друзьям\n\nа теперь пора написсать отзыв, Для этого нажмите кнопку "продолжить"', reply_markup = skip_btn)
    await Form.skiper.set()

@dp.message_handler(state = Form.skiper)
async def cheker(message: types.Message, state: FSMContext):
    await state.update_data(skip = message.text)

    sub_check = await bot.get_chat_member(chat_id = BLOG_ID, user_id = message.from_user.id)
    userstates = ['creator', 'member']

    if sub_check['status'] == userstates[0] or userstates[1] :
        await bot.send_message(message.from_user.id, 'Пример:\n\nкрутой бот <--- заголовок\nот {ваш_ник} <--- (заполняется автоматически)\n\nосновное\nописание\nбота\n\nбот работает #прекрасно - (вам будет предоставлен небольшой выбор хештегов)', reply_markup = ReplyKeyboardRemove())
        await bot.send_message(message.from_user.id, 'Сначала введите загаловок')
        await Form.form_header.set()
    else:
        print(sub_check['status'])        
        await bot.send_message(message.from_user.id, 'Вы не подписаны на блог канал, для продолжения работы вам стоит подписаться', reply_markup = blog_link)

@dp.message_handler(state = Form.form_header)
async def header(message: types.Message, state: FSMContext):
    await state.update_data(header = message.text)
    data = await state.get_data()
    a = False
    for i in CURSES:
        if i.lower() in data['header'].lower():
            await bot.send_message(message.from_user.id, 'Использования мата и др. слов запрещено\nпопробуйте ещё раз', reply_markup = ReplyKeyboardRemove())
            a = True
            await Form.form_header.set()
            break

    if a == False:
        await bot.send_message(message.from_user.id, 'Отлично! Теперь напишите основной текст отзыва', reply_markup = ReplyKeyboardRemove()) 
        await Form.main_text.set()
    
@dp.message_handler(state = Form.main_text)
async def main_text_func(message: types.Message, state: FSMContext):
    await state.update_data(main_text = message.text)
    data = await state.get_data()
    a = False
    for i in CURSES:
        if i.lower() in data['main_text'].lower():
            await bot.send_message(message.from_user.id, 'Использования мата и других определённых слов запрещено\nпопробуйте ещё раз')
            a = True
            await Form.main_text.set()
            break

    if a == False:
        await bot.send_message(message.from_user.id, 'Прекрасно! Теперь выберите хештег\n\nпрекрасно | классно | неплохо | плохо | ужасно', reply_markup = grades) 
        await Form.sharp.set()

@dp.message_handler(state = Form.sharp)
async def sharp_func(message: types.message, state: FSMContext):
    await state.update_data(sharp_to_add = message.text)
    data = await state.get_data()

    if data['sharp_to_add'].lower() == 'прекрасно' or 'классно' or 'неплохо' or 'плохо' or 'ужасно':
        try:
            await bot.send_message(REWIES_ID, f"""{data['header']}\nотзыв от @{message.from_user.username}\n\n{data['main_text']}\n\nбот работает #{data['sharp_to_add']}""")
            await bot.send_message(message.from_user.id, 'Спасибо за отзыв!\nон уже отправлен в канал с отзывами\n\nвведите /send_rew для того чтобы оставить новый отзыв', reply_markup = rew_link)
            await state.finish()
        except Exception as e:
            await bot.send_message(DEV_ID, f'!ошибка!\nв функции - sharp_func\nошибка - {e}')
    else:
        await bot.send_message(message.from_user.id,'введите один из выше перечисленных хештегов')

executor.start_polling(dp)