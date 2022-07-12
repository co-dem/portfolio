from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = 'your_token'

page_1 = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = 'me', callback_data = 'myself')], 
        [InlineKeyboardMarkup(text = '➡️', callback_data = 'next_to_page_2')] 
    ], 
    row_width = 1
)

page_2 = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = 'experience', callback_data = 'exp'), InlineKeyboardButton(text = 'skills', callback_data = 'skil')],
        [InlineKeyboardButton(text = '⬅️', callback_data = 'back_to_page_1'), InlineKeyboardButton(text = '➡️', callback_data = 'next_to_page_3')]
    ]
)

page_3 = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = 'price', callback_data = 'prices')],
        [InlineKeyboardButton(text = '⬅️', callback_data = 'back_to_page_2')]
    ]
)
