from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = 'your_token'     # bot's token
admin_id = <admin_id>    # admin's telegram id

main_panel = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('📁заполнить форму📁')]
    ],
    resize_keyboard = True
)

geneder_panel = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('🚹'), KeyboardButton('🚺')],
        [KeyboardButton('📛отмена📛')]
    ],
    resize_keyboard = True
)

cancel_btn = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('📛отмена📛')]
    ],
    resize_keyboard = True
)
