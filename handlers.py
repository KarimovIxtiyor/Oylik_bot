import asyncio

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
from db import get_name_by_user_id
from broadcast import send_about_to_user
from datetime import datetime
from aiogram.types import BotCommand, BotCommandScopeChat,ReplyKeyboardRemove



from config import BOT_TOKEN
from language import lang
from db import (
    add_user, update_user, is_registered,
    get_user_info, get_user_language,get_all_user_ids,get_users_by_language
)
from keyboards import (
    language_buttons, about_button,
    phone_button
)

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Foydalanuvchi uchun ro'yxat holatlari
class Registration(StatesGroup):
    name = State()
    surname = State()
    phone = State()

# Admin ID
ADMIN_IDS = [562831245]

# /start komandasi
@dp.message_handler(commands="start", state="*")
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Menu da commands lar ro`yxati hosil qilish
    commands = [BotCommand("start", "Boshlash")]
    if user_id in ADMIN_IDS:
        commands.append(BotCommand("send_univer", "Xabar yuborish"))
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeChat(chat_id=user_id))

    if is_registered(user_id):
        # Ro‘yxatdan o‘tgan bo‘lsa, "Men haqimda" tugmasi chiqadi
        language = get_user_language(user_id)
        await message.answer(
            text="Ok",
            reply_markup=about_button(lang[language]["about_me"])
        )
    else:
        # Aks holda til tanlash menyusi
        await message.answer(lang["uz"]["welcome"], reply_markup=language_buttons())



# Til tanlanganda callback
@dp.callback_query_handler(lambda c: c.data.startswith("lang_"), state="*")
async def language_callback(callback: types.CallbackQuery, state: FSMContext):
    code = callback.data.split("_")[1]
    user_id = callback.from_user.id
    await state.update_data(language=code)
    add_user(user_id, code)
    await callback.message.answer(lang[code]["ask_name"])
    await Registration.name.set()


# Ism qabul qilish
@dp.message_handler(state=Registration.name)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_id = message.from_user.id
    language = (await state.get_data())["language"]
    update_user(user_id, "name", message.text)
    await message.answer(lang[language]["ask_surname"])
    await Registration.surname.set()


# Familiya qabul qilish
@dp.message_handler(state=Registration.surname)
async def surname_handler(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    user_id = message.from_user.id
    language = (await state.get_data())["language"]
    update_user(user_id, "surname", message.text)
    await message.answer(lang[language]["ask_phone"], reply_markup=phone_button(lang[language]["ask_phone"]))
    await Registration.phone.set()


# Telefon raqam qabul qilish
@dp.message_handler(content_types=types.ContentType.CONTACT, state=Registration.phone)
@dp.message_handler(content_types=types.ContentType.TEXT, state=Registration.phone)
async def phone_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    language = (await state.get_data())["language"]
    phone = message.contact.phone_number if message.contact else message.text
    update_user(user_id, "phone", phone)
    await message.answer(lang[language]["registered"],reply_markup=ReplyKeyboardRemove())
    await state.finish()

# "Men haqimda" tugmasi
@dp.callback_query_handler(lambda c: c.data == "about")
async def about_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    await callback.answer(lang[language]["loading"])

    info = get_user_info(user_id)
    text = f"{lang[language]['about_me']}\n👤 {info[0]} {info[1]}\n📞 {info[2]}"
    await callback.message.answer(text)




# /send_go yuborilganda barcha userlarga 'about' yuborish
@dp.message_handler(commands="send_go", state="*")
async def broadcast_salom(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Sizda ruxsat yo‘q.")
        return

    user_ids = get_all_user_ids()

    for user_id in user_ids:
        try:
            await send_about_to_user(dp.bot, user_id)
        except Exception as e:
            print(f"[!] {user_id} ga yuborilmadi: {e}")
        #        fail+=1

        await asyncio.sleep(.05)




# /send_univer xabar yuborilganda adminda sms olib uni hamma foydalanuvchiga yuborish

from aiogram.dispatcher.filters.state import State, StatesGroup

class BroadcastState(StatesGroup):
    waiting_for_text = State()



@dp.message_handler(commands="send_univer", state="*")
async def start_universal_broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Sizda ruxsat yo‘q.")
        return

    await message.reply(" Yubormoqchi bo‘lgan POSTingizni tashlang:")
    await BroadcastState.waiting_for_text.set()

@dp.message_handler(state=BroadcastState.waiting_for_text, content_types=types.ContentTypes.ANY)
async def send_universal_broadcast(message: types.Message, state: FSMContext):
    user_ids = get_all_user_ids()
    success = 0
    failed = 0

    with open("log_send_univer.txt", "w", encoding="utf-8") as log:
        log.write("Yuborilishi boshlandi:\n\n")

        for user_id in user_ids:
            try:
                if message.photo:
                    await message.bot.send_photo(
                        user_id,
                        message.photo[-1].file_id,
                        caption=message.caption
                    )
                elif message.text:
                    await message.bot.send_message(user_id, message.text)
                elif message.video:
                    await message.bot.send_video(
                        user_id,
                        message.video.file_id,
                        caption=message.caption
                    )
                else:
                    continue

                name, surname, phone = get_user_info(user_id)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"Yuborildi: {user_id} | {name} {surname} | 📞 {phone} | 🕒 {timestamp}\n")
                success += 1

            except Exception as e:
                log.write(f"Xatolik: {user_id} | {e}\n")
                failed += 1

            await asyncio.sleep(0.05)

        log.write(f"\n Umumiy yuborilgan: {success} ta\n  Xatoliklar: {failed} ta\n")

    await message.reply(f"{success} ta foydalanuvchiga yuborildi.\n{failed} ta xato bo‘ldi.")
    await state.finish()