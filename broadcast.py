from db import get_user_info, get_user_language
from language import lang
from aiogram import  Bot


async def send_about_to_user(bot:Bot,user_id:int):
    language=get_user_language(user_id)
    info = get_user_info(user_id)

    if info:
        text = f"{lang[language]['about_me']}\n"
        text += f"👤 {info[0]} {info[1]}\n📞 {info[2]}"
        await bot.send_message(user_id, text)

