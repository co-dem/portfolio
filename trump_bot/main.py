from aiogram.utils import executor
from aiogram import Dispatcher, Bot, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.message import ContentType

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import *
from funcs import *

from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup


orders = []                             #* variable to store orders (for developer only)
dt = {}                                 #* dt and           are created to make oder process exactlyer
user_data = {}                          #*        user_data
storage = MemoryStorage()               #* memory object
bot = Bot(TOKEN)                        #* bot object
dp = Dispatcher(bot, storage = storage) #* Dispatcher object

class Form(StatesGroup): 
    product = State()
    main_info = State()  


#* function to create an account for user
# userid | username | orderplace | ordertime | product
def login_func(user) -> None:
    global user_data

    # if user doesn't exist, add him 
    if user_data.get(user.from_user.username) == None:
        
        user_data[user.from_user.username] = user.from_user.username 
        user_data[user.from_user.username] = {
            'id'        : user.from_id,
            'username'  : user.from_user.username,
            'product'   : None,    #* product that user ordered
            'main_info' : None
        }
    #* if user already exists, set all data to none
    else:
        user_data[user.from_user.username]['product'] = None
        user_data[user.from_user.username]['main_info'] = None

#* starting function
'''
here we set the access level for user:
basic user | manager | developer

and creating an account for user
'''
@dp.message_handler(commands = ['start', 'order'])
async def welcome(message: types.Message):
    
    upload_products()
    await set_bot_commands(bot = bot)   # setting hot commands
    login_func(user = message)          # creating an account

    print('[log]: new user ->', user_data)

    #* developer access level
    if message.text == '/start' and message.from_id == 798330024:
        await bot.send_message(message.from_id, f'Привет {message.from_user.username}!❤️\nЯ бот, который сделает процесс оформления заказа приятным\nуровень доступа: developer', reply_markup = developer_panel)
    #* manager access level
    elif message.text == '/start' and message.from_user.id == MANAGER_ID:
        await bot.send_message(message.from_id, f'Привет {message.from_user.username}!\nЯ бот для оформления заказа на различную технику от stuff with trump\nуровень доступа: manger', reply_markup = manager_panel)
    #* basic user access level
    elif message.text == '/start' and message.from_user.id != MANAGER_ID:
        await bot.send_message(message.from_id, f'Привет {message.from_user.username}!❤️\nЯ бот для оформления заказа на различную технику от stuff with trump\nвыбери действие ниже', reply_markup = user_panel)

    # same
    elif message.text == '/order' and message.from_id == 798330024:
        await bot.send_message(message.from_id, 'Я перевёл вас в главное меню', reply_markup = developer_panel)    
    
    elif message.text == '/order' and message.from_id == MANAGER_ID:
        await bot.send_message(message.from_id, 'Я перевёл вас в главное меню', reply_markup = manager_panel)    
    
    elif message.text == '/order' and message.from_id != MANAGER_ID:
        await bot.send_message(message.from_id, 'Я перевёл вас в главное меню', reply_markup = user_panel)    


@dp.message_handler(content_types = 'text')
async def msg_handler_func(message: types.Message):
    global orders

    #* developer commads handling
    if message.text.lower() == 'оформить заказ' and message.from_id == 798330024:
        await bot.send_message(message.from_id, 'Начнём процесс оформления заказа\nдля начала вы можете выбрать товар который хотите у нас заказать', reply_markup = ReplyKeyboardRemove())
        update_database()
        catalog_string = ''
        for i in get_products(update_database()):
            if i == 'product name':
                continue
            catalog_string += f'{i}\n'
        await bot.send_message(MANAGER_ID, catalog_string)
        await Form.product.set()

    elif message.text.lower() == 'посмотреть статистику' and message.from_id == 798330024:
        stat_string = ''
        for i in showstats().items():
            stat_string += f'{i[0]}: {i[1]}\n'
        await bot.send_message(message.from_id, stat_string)

    elif message.text.lower() == 'очистить статистику' and message.from_id == 798330024:
        try:
            clear_stats()
            await bot.send_message(798330024, 'stats cleard successfully')
            print(f'clear stats: True\nstats: {showstats()}')
        except Exception as e:
            await bot.send_message(798330024, f'[error]: in clearing stats -> {e}')
            print(f'[error]: in clearing stats -> {e}')

    elif message.text.lower() == 'очистить заказы' and message.from_id == 798330024:
        orders = []
        print(f'[log]: all info from "orders" was deleted -> orders: {orders}')
        await bot.send_message(message.from_id, 'вся информация из "orders" была удалена')

    elif message.text.lower() == 'посмотреть заказы' and message.from_id == 798330024:
        await bot.send_message(798330024, orders)

    elif message.text.lower() == 'отключить бота' and message.from_id == 798330024:
        await bot.delete_message(chat_id = message.chat.id, message_id=message.message_id)
        quit()

    #* basic user commands handling
    elif message.text.lower() == 'оформить заказ💨':
        await bot.send_message(message.from_id, 'Начнём процесс оформления заказа\nдля начала вы можете выбрать товар который хотите у нас заказать', reply_markup = ReplyKeyboardRemove())
        update_database()
        catalog_string = ''
        for i in get_products(update_database()):
            if i == 'product name':
                continue
            catalog_string += f'{i}\n'
        await bot.send_message(message.from_id, catalog_string)
        await Form.product.set()

    elif message.text.lower() == '⭐️оставить отзыв⭐️':          
        await bot.send_message(message.from_id, 'todo: создать тг канал с отзывами и отправлять сообщение с ссылкой на этот тг канал')
    
    elif message.text.lower() == '👷‍♂️менеджер👷‍♂️':
        await bot.send_message(message.from_id, '<a href="https://t.me/oleg_supp">👷‍♂️наш менеджер👷‍♂️</a>', parse_mode = 'HTML')

    #* manager commands handling
    elif message.text == '📊показать статистику' and message.from_id == MANAGER_ID:
        update_database()
        stat_string = ''
        for i in showstats().items():
            stat_string += f'{i[0]}: {i[1]}\n'
        await bot.send_message(message.from_id, stat_string)

    elif message.text == 'посмотреть каталог📋' and message.from_id == DEVELOPER_ID:
        update_database()
        catalog_string = ''
        for i in get_products(update_database()):
            catalog_string += f'{i}\n'
        await bot.send_message(MANAGER_ID, catalog_string)

@dp.message_handler(state = Form.product)
async def choose_product(message: types.Message, state: FSMContext):
    global data, dt, orders

    await state.update_data(product = message.text.lower())
    data = await state.get_data()

    #* cheking if product that user choosed is available
    available_product = check_product(data['product'].lower()) == True
    print('passing product check: ', available_product)

    if available_product == False:
        await bot.send_message(message.from_id, 'К сожаленью у нас нет данного товара или вы не правильно ввели его название\nпопробуйте ещё раз')
        await Form.product.set()
    else:
        dt = data
        user_data[message.from_user.username]['product'] = data['product']

        print(f'[log]: user - {message.from_user.username} orders - {data["product"]}')

        await bot.send_message(message.from_id, 'отлично!\nтеперь вам нужно заполнить основную информацию с помошью которой мы сможем выслать вам ваш заказ\nФ.И.О. - Город - Товар - Почтовое отделение и индекс - номер телефона')
        await Form.main_info.set()

@dp.message_handler(state = Form.main_info)
async def getting_main_info(message: types.Message, state: FSMContext):
    global data, dt, orders

    await state.update_data(info = message.text)
    await state.update_data(username = message.from_user.username)
    data = await state.get_data()

    user_data[message.from_user.username]['main_info'] = data['info']

    #* creating inline menu with username
    ACCEPT_MENU = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text = f'отклонить {user_data[message.from_user.username]["username"]}', callback_data = f'reject'), 
            InlineKeyboardButton(text = f'одобрить {user_data[message.from_user.username]["username"]}', callback_data = f'accept')]
        ]
    ) 

    #* sending all info that user sended to the manager 
    await bot.send_message(message.from_id, '📤отлично, я отправил ваш заказ на модерацию📤\nожидайте, в течении 5 минут, вам придёт сообщение')
    await bot.send_message(MANAGER_ID, f'@{message.from_user.username}\n\
product: {user_data[message.from_user.username]["product"]}\n\
place: {user_data[message.from_user.username]["main_info"]}📥', reply_markup = ACCEPT_MENU)
        
    await state.finish()


@dp.callback_query_handler()
async def moderation_func(call: types.CallbackQuery):
    global orders
    print(user_data)

    if call.data == 'reject':
        for name in user_data:
            if name in call.message.text:
                print(name)
                await bot.send_message(user_data[name]['id'], '❌ваш заказ отоклонён❌\nпо вопросам обращяйтесь к \n<a href = "https://t.me/c0dem">👷‍♂️менеджеру👷‍♂️</a>', parse_mode = 'HTML')

    elif call.data == 'accept':
        for name in user_data:
            if name in call.message.text:
                changestats(user_data[data["username"]]["product"].lower())
                orders.append(user_data[data["username"]]["product"])
                print(name)
                print(orders)

                await bot.send_message(user_data[name]['id'], f'✨ваш заказ одобрен✨\n  \n<a href = "https://t.me/c0dem">👷‍♂️менеджеру👷‍♂️</a>', parse_mode = 'HTML')
                await buy(call.message, data, user_data)

    await bot.send_message(user_data[name]['id'], '🔄если хотите оформить ещё заказ, то вам нужно использывать эту комманду: /order')                                                                                                                                                                

async def buy(message: types.Message, data, user_data):
    if PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(user_data[data["username"]]["id"], "Тестовый платеж!!!")

    product = user_data[data["username"]]["product"]
    photo_link = 'https://www.apple.com/newsroom/images/product/airpods/standard/Apple_AirPods-Pro_New-Design_102819_big.jpg.large.jpg'
    for x, y in product_photo.items():
        if x == product:
            photo_link = y

    # PRICE = types.LabeledPrice(label=f'покупка {product}\nпредоплата', 
    #                            amount = int( ( ( ( ( get_price(product) * 27.40 * 100 ) / 100 * get_sale(product) ) / 2 ) ) / 100)
    
    PRICE = types.LabeledPrice(label = product, amount = int( (((1000 * 27.40 * 100) / 100 * 70)/2)/100) ) # 100 rub 70% от 100 = 70
    
    await bot.send_invoice(user_data[data["username"]]["id"],
                           title="предоплата товара",
                           description=f'предоплата на {product}\nвам нужно оплатить половину цены товара c учётом акции, а после того как мы вышлем вам трек-номер, вам нужно юудет оплатить вторую часть',
                           provider_token=PAYMENT_TOKEN,
                           currency="rub",
                           photo_url=photo_link,
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           payload="test-invoice-payload")

# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

# successful payment
@dp.message_handler(content_types= ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(user_data[data["username"]]["id"], f"✅Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно✅")

if __name__ == '__main__':
    executor.start_polling(dp)
#| coded by codem