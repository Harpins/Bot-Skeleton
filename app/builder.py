from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import app.utils as utl
from datetime import datetime

def make_salons_buttons():
    keyboard = InlineKeyboardBuilder()
    salons = utl.get_salons()
    for salon in salons:
        keyboard.add(
            InlineKeyboardButton(
                text=f'{salon['name']} - {salon['address']}',
                callback_data=f'salon_{salon['id']}',
                )
            )
    return keyboard.adjust(1).as_markup()

def make_procedures_buttons():
    keyboard = InlineKeyboardBuilder()
    procedures = utl.get_procedures()
    for procedure in procedures:
        keyboard.add(
            InlineKeyboardButton(
                text=f'{procedure['name']} - {procedure['price']} p.',
                callback_data=f'procedure_{procedure['id']}',
                )
            )
    return keyboard.adjust(1).as_markup()

def make_specialists_buttons(filtered_specialists):
    keyboard = InlineKeyboardBuilder()
    for specialist in filtered_specialists:
        keyboard.add(
            InlineKeyboardButton(
                text=f'{specialist['user']['username'].replace('_', ' ')}',
                callback_data=f'specialist_{specialist['id']}',
                )
            )
    return keyboard.adjust(1).as_markup()


def choose_free_time(free_time_intervals):
    keyboard = InlineKeyboardBuilder()
    for interval in free_time_intervals:
        keyboard.add(
            InlineKeyboardButton(
                text=f'{utl.format_time_to_string(interval[0])}_{utl.format_time_to_string(interval[1])}',
                callback_data=f'time_{utl.format_time_to_string(interval[0])}_{utl.format_time_to_string(interval[1])}',
                )
            )
    return keyboard.adjust(1).as_markup()
    