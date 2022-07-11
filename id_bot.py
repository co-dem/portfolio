from aiogram.utils import executor
from aiogram import Dispatcher, types, Bot
from aiogram.utils.exceptions import MessageTextIsEmpty

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

class msgid(StatesGroup):
    msg = State()

#* some important vars
TOKEN = 'your token'
storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage = storage)

#!                              id bot                              !#

#* just a welcome func
@dp.message_handler(commands = 'start')
async def welcome(message: types.Message):
    await bot.send_message(message.from_user.id, "Hello, I'm an id bot\nand I'll help you with getting ids of different chnnels/groups/people")
    await bot.send_message(message.from_user.id, "just forward me any message, from any chat you want and I'll send you id of it")
    await bot.send_message(message.from_user.id, f'your id is {message.from_user.id}')
    await msgid.msg.set()

#* main id getter handler
@dp.message_handler(state = msgid.msg)
async def get_id_func(message: types.Message, state: FSMContext):
    #* here we are getting forwarded message from channel/chat
    ffch = message.forward_from_chat
    #* here we are getting forwarded message from private chat
    ff = message.forward_from
    
    try:
        #* here, for example, we try to get the id of private chat but we get an error and go to the except block
        #* where we get the id of private chat
        await bot.send_message(message.from_user.id, f"id ---> {ffch.id}")

    except (MessageTextIsEmpty, AttributeError) as e:
        #* I'm tooo lasy to explain what is happening here
        #*                 |: sorry :|
        if type(e) == AttributeError and ff is not None:
            await bot.send_message(message.from_user.id, f'id is ---> {ff.id}')
        if type(e) == MessageTextIsEmpty:
            await bot.send_message(message.from_user.id, '⚠️error⚠️\nplease try again')
        else:
            if ff is None:
                await bot.send_message(message.from_user.id, f'your id is ---> {message.from_user.id}')
            else:
                await bot.send_message(message.from_user.id, f'id is {ff.id}')
        
executor.start_polling(dp)
#| coded by codem
