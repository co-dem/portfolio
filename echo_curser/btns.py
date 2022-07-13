from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

word_moderating_markup = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = '✅', callback_data = 'accept')],
        [InlineKeyboardButton(text = '❌', callback_data = 'reject')]
    ],
    row_width = 1
)
