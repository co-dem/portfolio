from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '5317213631:AAHDUv3QjY6Y4aU_PIsCWe-fzIFcZjWS-e8'
admin_id = 798330024

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