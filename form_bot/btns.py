from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#| reply markups |#
skip_btn = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('продолжить')]
    ],
    resize_keyboard = True
)

grades = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('прекрасно'), KeyboardButton('классно')],
        [KeyboardButton('неплохо')],
        [KeyboardButton('плохо'), KeyboardButton('ужасно')]
    ],
    resize_keyboard = True
)

#| inline markups |#
blog_link = InlineKeyboardMarkup()
link_btn = InlineKeyboardButton(text = 'ссылка на канал', url = 'https://t.me/razrab_blog')
blog_link.add(link_btn)

rew_link = InlineKeyboardMarkup()
link_btn = InlineKeyboardButton(text = 'ссылка на канал', url = 'https://t.me/codemrew')
rew_link.insert(link_btn)
