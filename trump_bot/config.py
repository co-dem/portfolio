from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats,\
                          ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = 'token'
PAYMENT_TOKEN = 'token'
MANAGER_ID   = 12345
DEVELOPER_ID = 12345

product_photo = {
    'airpods pro': 'https://www.apple.com/newsroom/images/product/airpods/standard/Apple_AirPods-Pro_New-Design_102819_big.jpg.large.jpg',
    'airpods max': 'https://mobile-review.com/articles/2020/image/apple-airpods-max-preview/7.jpg'
}

user_panel = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('Оформить заказ💨')],
        [KeyboardButton('⭐️Оставить отзыв⭐️'), KeyboardButton('👷‍♂️Менеджер👷‍♂️')]
    ],
    resize_keyboard = True
)

manager_panel = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('📊показать статистику'), KeyboardButton('посмотреть каталог📋')]
    ],
    resize_keyboard = True
)

developer_panel = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('оформить заказ')],
        [KeyboardButton('посмотреть статистику'), KeyboardButton('очистить статистику')],
        [KeyboardButton('посмотреть заказы'), KeyboardButton('очистить заказы')],
        [KeyboardButton('отключить бота')]
    ],
    resize_keyboard = True
)


async def set_bot_commands(bot: Bot):
    commands = [
            BotCommand(command = "/manager", description = "получить контакты манеджера"),
            BotCommand(command = "/order", description = "сделать новый заказ")
        ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
