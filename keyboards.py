from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

# Til tanlash uchun inline tugmalar
def language_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    uz = InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz")
    ru = InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")
    markup.add(uz, ru)
    return markup

# Telefon raqam jo'natish uchun tugma (reply)
def phone_button(text):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    phone = KeyboardButton(text=text, request_contact=True)
    markup.add(phone)
    return markup

# "Men haqimda" tugmasi uchun inline tugma
def about_button(text):
    markup = InlineKeyboardMarkup()
    about = InlineKeyboardButton(text=text, callback_data="about")
    markup.add(about)
    return markup





"""# /start tugmasi (reply keyboard)
def start_reply_button(text):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text=text)
    markup.add(button)
    return markup"""
