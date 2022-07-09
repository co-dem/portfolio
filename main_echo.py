from aiogram import *
from aiogram.utils import executor
from aiogram.utils.exceptions import MessageToDeleteNotFound
from config import TOKEN, CURSES
from fuzzywuzzy import fuzz

bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types = 'text')
async def main(message: types.Message):
    
    contin = True
    #* 2 цикла чтобы вытащить слова из словаря постучно а потом вытащить слова также постучно из сообщения
    for words in CURSES:

        for chek_word in message.text.lower().split():
            #* эта переменная отвечает за получение соотношения корня мата из словаря и мата из сообщения
            #* если он больше чем 55, то мы щитаем что это мат и кидаем предупредительное сообщение
            # TODO: сделать функцию которая при отсутствии написанного мата и процент слова = 53-54 
            # TODO: отправляем его мне на модерацию в телегу 
            coot = fuzz.ratio(words, chek_word)
            if coot >= 55:
                #* блок try except которые просто удаляют сообщение с матом и пишут предупреждение
                try:
                    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id)
                    await bot.send_message(message.from_user.id, f'слова с содержанием {words}, запрещены!')
                    contin = False
                    break

                except MessageToDeleteNotFound:
                    await bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1)
                    await bot.send_message(message.from_user.id, f'слова с содержанием {words}, запрещены!')
                    contin = False
                    break

    #* т.к. это эхо бот, после проверки сообщения на мат, при значении этой переменной True, 
    #* мы просто работаем как эхо бот, но при значении переменной False, мы просто пропускаем этот момент
    if contin == True:
        await bot.send_message(message.from_user.id, message.text)

executor.start_polling(dp)
#| coded by codem