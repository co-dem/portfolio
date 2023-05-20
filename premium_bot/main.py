from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types.message import ContentType

from config import *

from datetime import date


bot = Bot(TOKEN)
dp = Dispatcher(bot)

tarifs = {
    '1 неделя': 100, # 100
    '1 месяц' : 200, # 200
    'навсегда': 300  # 300
}
user_data = {}


def login(user):
    global user_data

    if user_data.get(user.from_user.username) == None:
        user_data[user.from_user.username] = user.from_user.username 
        user_data[user.from_user.username] = {
            'id'      : user.from_id,
            'username': user.from_user.username,
            'endate'  : '2023-12-12',
            'balance' : 600
        }

get_expiring_date = lambda x: eval(str(x).replace('-', '').replace('', '+')[1:-1])
async def expiring_date_check():
    global user_data


    td = date.today()
    today_date = get_expiring_date(td)

    for x, y in user_data.items():
        check_date = get_expiring_date(y['endate'])
        print(check_date, today_date)
        if int(today_date) >= int(check_date):
            await bot.send_message(y['id'], 'ваша подписка на наш приват канал закончилась(\nвы можете её продлить нажам кнопку "приобрести доступ" ниже')
            return False

async def waste_money_func(option, user):
    global user_data

    if option == 100 and user_data[user.from_user.username]['balance'] >= 100 and await expiring_date_check() == False:
        user_data[user.from_user.username]['balance'] -= 100
        user_data[user.from_user.username]['endate'] = get_expiring_date(date.today()) + 7

    elif option == 200 and user_data[user.from_user.username]['balance'] >= 200 and await expiring_date_check() == False:
        user_data[user.from_user.username]['balance'] -= 200
        user_data[user.from_user.username]['endate'] = get_expiring_date(date.today()) + 30
    
    elif option == 300 and user_data[user.from_user.username]['balance'] >= 300 and await expiring_date_check() == False:
        user_data[user.from_user.username]['balance'] -= 300
        user_data[user.from_user.username]['endate'] =  get_expiring_date(date.today()) + 9999888
    
    elif user_data[user.from_user.username].get('endate') != None:
        return 'вы уже есть доступ к нашему телеграм каналу\nдождитесь до окончания подписки и оформите ещё раз'
    else: 
        return 'не достаточно средств'
    print(user_data[user.from_user.username]['endate'])
    return user_data[user.from_user.username]['balance']

@dp.message_handler(commands = 'start')
async def welcome_func(message: types.Message):
    login(message)
    print('[log]: new user |', user_data)
    await bot.send_message(message.from_id, f'Привет {message.from_user.username}\nтут ты можешь купить доступ в наш приватный канал.\nдля этого тебе нужно:\nпополнить баланс\nвыбрать тариф\nприобрести его', reply_markup = user_main_menu)

@dp.message_handler(commands = 'rep')
async def add_money(message: types.Message):
    try:
        await buy(message = message, amount = message.text.split(' ')[1], data = message.from_user.username, user_data = user_data)
    except IndexError as e:
        await bot.send_message(message.from_user.id, 'введены неверные данные\nпопробуйте ещё раз')

@dp.message_handler(content_types = 'text')
async def commands_handling_func(message: types.Message):
    if message.text.lower() == 'приобрести доступ':
        await bot.send_message(message.from_id, '1 week: 100 rub\n1 month: 200 rub\nforever: 300 rub', reply_markup = tarifs_mrk)
        await expiring_date_check()
    
    elif message.text.lower() == 'баланс':
        await bot.send_message(message.from_id, f'ваш баланс: {user_data[message.from_user.username]["balance"]}')
        await expiring_date_check()
    
    elif message.text.lower() == 'пополнить баланс':
        await bot.send_message(message.from_id, 'чтобы пополнить баланс вам нужно ввести команду\n/rep [сумма]')

    elif message.text.lower() in tarifs:
        for description, option in tarifs.items():
            if description == message.text.lower():
                answ = await waste_money_func(option = option, user = message)
                if str(answ).isdigit():
                    await bot.send_message(message.from_id, f'оплата {option}rub прошла успешно\nвот ваша ссылка - [link]', reply_markup = user_main_menu)
                else:
                    await bot.send_message(message.from_id, answ, reply_markup = user_main_menu)
                print('balance:', user_data[message.from_user.username]['balance'])


async def buy(message: types.Message, data, user_data, amount):
    if PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(user_data[data]["id"], "Тестовый платеж!!!")

    PRICE = types.LabeledPrice(label = 'доступ к приватке', amount = int(amount)*100)
    
    await bot.send_invoice(user_data[data]["id"],
                           title="приватка",
                           description=f'пополнение счёта',
                           provider_token=PAYMENT_TOKEN,
                           currency="rub",
                           photo_url='https://sienaconstruction.com/wp-content/uploads/2017/05/test-image.jpg',
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
    global user_data
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.from_id, f"✅Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно✅")
    user_data[message.from_user.username]['balance'] += message.successful_payment.total_amount // 100

executor.start_polling(dp)
#| coded by c0dem
