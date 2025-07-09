import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN
from db import create_db
from handlers import dp, bot #,on_startup_notify

#  FSM holatlarini RAM'da saqlash uchun MemoryStorage ulaymiz
storage = MemoryStorage()


# Dispatcherga storage biriktiramiz
dp.storage = storage


#  Bot ishga tushganda baza yaratiladi
async def on_startup(dp):
    create_db()
    #await on_startup_notify(dp)



#  Polling orqali botni ishga tushuramiz
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
