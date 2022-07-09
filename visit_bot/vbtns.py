from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_page = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('я'), KeyboardButton('способы связи')],
        [KeyboardButton('прайс'), KeyboardButton('тг каналы')],
        [KeyboardButton('портфолио')]
    ],
    resize_keyboard = True
)
