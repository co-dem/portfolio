from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = 'your bot token'
PAYMENT_TOKEN = 'your payment token'

user_main_menu = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('приобрести доступ')],
        [KeyboardButton('баланс'),KeyboardButton('пополнить баланс')]
    ],
    resize_keyboard = True
)

tarifs_mrk = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('навсегда')],
        [KeyboardButton('1 месяц')],
        [KeyboardButton('1 неделя')]
    ],
    resize_keyboard = True
)
