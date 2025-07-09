from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from handlers import ADMIN_IDS

async def on_startup(dp):
    create_db()

    #  Oddiy foydalanuvchilar uchun buyruqlar
    await dp.bot.set_my_commands(
        commands=[
            BotCommand("start", "Botni boshlash"),
        ],
        scope=BotCommandScopeDefault()
    )

    #  Har bir admin uchun maxsus buyruq ko‘rsatamiz
    for admin_id in ADMIN_IDS:
        await dp.bot.set_my_commands(
            commands=[
                BotCommand("start", "Botni boshlash"),
                BotCommand("send_univer", "Xabarni barcha userlarga yuborish"),
                BotCommand("send_new", "Rasmli bildirish yuborish"),
            ],
            scope=BotCommandScopeChat(chat_id=admin_id)
        )
