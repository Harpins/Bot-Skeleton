from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

#Пример билдера клавиатуры из туториала
data = ("Apple", "Banana", "Orange")

def make_fruit_buttons():
    keyboard = ReplyKeyboardBuilder()
    for fruit in data:
        keyboard.add(KeyboardButton(text=fruit))
    return keyboard.adjust(2).as_markup()
