from aiogram import Bot, Dispatcher, executor, types
import json
from main import check_new,print_hi,get_pars,f5,check_all_items
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
import asyncio

bot = Bot(token="5199184635:AAHZgal57l-fFQLgPkG-5sF4rOwPW2FNcOo", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
ADMINS  = [419861815,488008538]

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.reply("Успешно")




async def news_every_minute(last):
    while True:
        reloud_page = f5()
        if (check_new(reloud_page, last)):
            for admin_id in ADMINS:
                await bot.send_message(admin_id, "ОБНОВИЛСЯ МАГАЗИН")
            last = get_pars()
            await asyncio.sleep(100)
        else: print("Pysto")

        await asyncio.sleep(5)
if __name__ == '__main__':
    print("Запускаю браузер")
    print_hi()  # Запускаем браузер и парсим src
    print("Получаю последний элемент")
    last = get_pars()  # Открываем src парсим все данные и возвращаем послдений елемент
    #last = "0.1151"
    #check_all_items()
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute(last))
    executor.start_polling(dp)