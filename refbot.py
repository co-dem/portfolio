# ref bot example

from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor

import re


userdb = {}
bot = Bot(token='token')
dp = Dispatcher(bot)

#* function to insert users to the list (instead of adding whole database)
async def userDataBase(message):
    global userdb

    if message.from_user.username not in userdb:
        userdb[str(message.from_id)] = message.from_user.username

    print(userdb)

@dp.message_handler(regexp='^/start\s\d+')
async def main(message: types.Message):
    #* checking to see if it is private chat
    if message.chat.type == 'private':
        #* getting referrer's and referral's id 
        referrer_chat_id = re.search(r'\d+', message.text).group(0)
        referral_chat_id = message.chat.id

        #* checking some conditions
        if str(referral_chat_id) == str(referrer_chat_id):
            await bot.send_message(message.from_id, f'ваша пригласительная ссылка: `https://t.me/test_srochno_bot?start={message.chat.id}` \nотправьте её друзьям', parse_mode='MARKDOWN')      
        elif str(referral_chat_id) != str(referrer_chat_id) and str(message.from_id) not in userdb:
            await bot.send_message(message.from_id, f'вы успешно перешли по реферальной ссылки от @{userdb[str(referrer_chat_id)]}')
        elif str(referral_chat_id) != str(referrer_chat_id):
            await bot.send_message(message.from_id, 'вы уже зарегестрированы')
        #* adding user to the list
        await userDataBase(message=message)

@dp.message_handler(commands='link')
async def getRefLinkFunc(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.from_id, f'ваша пригласительная ссылка: `https://t.me/test_srochno_bot?start={message.chat.id}` \nотправьте её друзьям', parse_mode='MARKDOWN')      

@dp.message_handler(commands='start')
async def start(message: types.Message):
    if message.chat.type == 'private':
        await userDataBase(message=message)
        await bot.send_message(message.from_id, f'Доброго времени суток {message.from_user.first_name}\nэто пример бота для демонстрации работы реферальной ссылки')
        await bot.send_message(message.from_id, 'нажмите команду /link чтобы получить свою реферальную ссылку')

executor.start_polling(dp)
