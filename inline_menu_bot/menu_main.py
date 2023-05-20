from aiogram import *
from aiogram.utils import executor

from config import TOKEN, page_1, page_2, page_3

bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands = 'start')
async def welcome(message: types.Message):
    await bot.send_message(message.from_user.id, "Hello, I'm a menu bot by codem\nI was made for codem's portfolio\nenjoy!", reply_markup = page_1)

@dp.callback_query_handler(text = ['myself', 'exp', 'skil', 'prices', 'back_to_page_1', 'back_to_page_2', 'next_to_page_2', 'next_to_page_3'])
async def main(call: types.CallbackQuery):
    #*---------- main questions ----------*#
    if call.data == 'myself':
        await bot.send_message(call.from_user.id, 'some info about me')
    elif call.data == 'exp':
        await bot.send_message(call.from_user.id, 'some info about experience I got')
    elif call.data == 'skil':
        await bot.send_message(call.from_user.id, 'some info about my skills')
    elif call.data == 'prices':
        await bot.send_message(call.from_user.id, 'some info about my prices')
    
    #*---------- page switching ----------*#
    if call.data == 'back_to_page_1':
        await bot.delete_message(chat_id = call.from_user.id, message_id = call.message.message_id)
        await bot.send_message(call.from_user.id, 'here you can get some info about me', reply_markup = page_1)

    elif call.data == 'back_to_page_2' or call.data == 'next_to_page_2':
        await bot.delete_message(chat_id = call.from_user.id, message_id = call.message.message_id)
        await bot.send_message(call.from_user.id, 'this is page number 2 with some useful info', reply_markup = page_2)

    elif call.data == 'next_to_page_3':
        await bot.delete_message(chat_id = call.from_user.id, message_id = call.message.message_id)
        await bot.send_message(call.from_user.id, 'this is page number 3 with some price info', reply_markup = page_3)

if __name__ == '__main__':
    executor.start_polling(dp)
#| coded by c0dem
