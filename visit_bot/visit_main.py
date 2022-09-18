from aiogram import Dispatcher, types, Bot
from aiogram.utils import executor
from vbtns import main_page

bot = Bot(your_token)
dp = Dispatcher(bot)

@dp.message_handler(commands = 'start')
async def main(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет👋! Я визитыч одного очень интересного разработчика телеграм ботов👾\nя был создан, чтобы представлять его другим людям в то время как он усердно работает над новыми заказами/проектами🫠\nвыберите пункт ниже чтобы я мог на него ответить🤖', reply_markup = main_page)

@dp.message_handler(content_types = 'text')
async def text_handler(message: types.Message):
    if message.text.lower() == 'я':
        await bot.send_message(message.from_user.id, 'Я мужчина средних лет который родился и вырос в Азербайджане🇦🇿, русский выучил в школе.\nДелаю ботов на заказ, опыт разработки примерно <strong>года 2</strong>, для самого создания использую python(aiogram), недавно вышел на фриланс и уже занимаюсь этим профессионально\n\nмои сильные качетсва:\n•делаю быстрых и качественных ботов\n(в этом вы можете убедится сами посетив вкладку "портфолио")\n•крутейшие админ панели\n(что бы убедиться нужно купить одного🤡)\n•короткие сроки выполнения\n(1 - 4 дня <strong>максимум</strong>)\n•и многое другой\n\nмои минусы:\не работаю с плтежами\не работаю с криптой\n•всё', parse_mode = 'html')
    elif message.text.lower() == 'способы связи':
        await bot.send_message(message.from_user.id, 'telegram: @c0dem\ngmail: codemworker@gmail.com')
    elif message.text.lower() == 'прайс':
        await bot.send_message(message.from_user.id, 'Все зависит только от <strong>сложности и примерной продолжительности</strong> проекта\n     ❗работаю только по предоплате❗', parse_mode = 'html')
    elif message.text.lower() == 'тг каналы':
        await bot.send_message(message.from_user.id, 'блог - https://t.me/razrab_blog\nотзывы - https://t.me/codemrew')
    elif message.text.lower() == 'портфолио':
        await bot.send_message(message.from_user.id, 'бот для отправки отзывов - @form_fill_bot\nбот визитка - @visitch_bot\nи ещё несколько ботов')

executor.start_polling(dp)
#| coded by codem
