from aiogram import *
from aiogram.utils import executor
from aiogram.utils.exceptions import MessageToDeleteNotFound

from btns import word_moderating_markup
from config import TOKEN, CURSES, MODERATED_WORDS, ADMIN_ID

from dataclasses import dataclass
from fuzzywuzzy import fuzz

bot = Bot(TOKEN)
dp = Dispatcher(bot)

#* mini database
@dataclass
class userinfo:
    id: int
    msg: str

@dp.message_handler(content_types = 'text')
async def main(message: types.Message):
    cont = True
    tws = 0
    for word_from_list in CURSES:
        for word_from_msg in message.text.lower().split():
            #* second loop
            #* here we are cheking for some trigger words
            coot = fuzz.ratio(word_from_list, word_from_msg)
            if coot >= 55 and word_from_msg not in MODERATED_WORDS:
                cont = False
                try:
                    await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
                except MessageToDeleteNotFound:
                    pass

                finally:
                    await bot.send_message(message.from_user.id, 'we found foul curse in your message so I had to delete your message')

            elif coot > 50 and coot < 55 and word_from_msg not in MODERATED_WORDS:
                cont = False
                try:
                    #* if we found a suspicious word, bot will send it to the admin (to me) in moderating purposes
                    add_crimanls_id = userinfo(id = message.from_user.id, msg = message.text.lower())
                    await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
                except MessageToDeleteNotFound:
                    pass

                finally:
                    await bot.send_message(798330024, word_from_msg[tws], reply_markup = word_moderating_markup)
                    await bot.send_message(message.from_user.id, 'we noticed a suspicious word in your message\have sent it to moderation, provided the message does not contain profanity, we will put the trigger word in the database and will not disturb any more users with this message\n the condition that the message contains profanity I will ban you for one day\ngood day')

            tws += 1
            
        #* first loop
        #* if bot found a curse in the message, he will chek it trugh the hole list so we have to breake the loop
        if cont == False:
            break

    #* out of all loops
    #* if cont equals True
    if cont:
        await bot.send_message(message.chat.id, message.text)

#* that is a magick part of code so no one should know what is this
@dp.callback_query_handler(text = ['accept', 'reject'])
async def accept_reject(call: types.CallbackQuery):
    criminals_id = userinfo()
    if call.data == 'accept':
        await bot.send_message(call.from_user.id, "I'm sorry\n the word I thought was suspicious was not, I already entered it in the white list")
        await bot.send_message(798330024, f'I found a suspicious message {criminals_id.msg}')
    elif call.data == 'reject':
        try:
            await bot.ban_chat_member(chat_id = call.chat.id, user_id = criminals_id.id)

        except Exception as e:
            sub = await bot.get_chat_member(chat_id = -1001767304406, user_id = criminals_id.id)
            if sub['status'] == 'left' or 'kicked':
                await bot.send_message(call.from_user.id, "you are in the private chat so I'll forgive you that")
            elif sub['status'] == 'member':
                try:
                    await bot.ban_chat_member(chat_id = -1001767304406, user_id = criminals_id.id)
                except Exception:
                    await bot.send_message(call.from_user.id, 'you are you are too lucky today')

if __name__ == '__main__':
    executor.start_polling(dp)
#| coded by codem