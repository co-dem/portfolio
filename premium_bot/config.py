from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '5317213631:AAHDUv3QjY6Y4aU_PIsCWe-fzIFcZjWS-e8'
PAYMENT_TOKEN = '381764678:TEST:54491'

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