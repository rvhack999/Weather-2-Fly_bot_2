""" точка входа, код запуска бота и инициализации всех остальных модулей """

import logging
import text
from aiogram import Bot, Dispatcher, types, executor
import kb
import config
from utils import get_weather

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=text.greet.format(name=message.from_user.full_name), reply_markup=kb.start_kb)


@dp.message_handler(content_types=['location'])
async def get_cords(msg: types.Message):
    lon = msg.location.longitude
    lat = msg.location.latitude
    if len(get_weather(lat, lon)) == 24:
        await bot.send_message(chat_id=msg.from_user.id, text='Сегодня благоприятный день! Летай когда угодно!')
    else:
        for i, j in get_weather(lat, lon).items():
            await bot.send_message(chat_id=msg.from_user.id, text=f'Дата: {i[:10]}\n'
                                                                  f'         Время: {i[11:]}\n'
                                                                  f'                     Коэффициент: {j}')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
