from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.utils as utl

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
                text=f'{utl.format_time_to_string(interval[0])}-{utl.format_time_to_string(interval[1])}',
                callback_data=f'time_{utl.format_time_to_string(interval[0])}_{utl.format_time_to_string(interval[1])}',
                )
            )
    return keyboard.adjust(1).as_markup()


def choose_any_time():
    keyboard = InlineKeyboardBuilder()
    for hour in range(8, 21):
        keyboard.add(
            InlineKeyboardButton(
                text=f'{hour}:00-{hour+1}:00',
                callback_data=f'time_{hour}:00_{hour+1}:00',
                )
            )
    return keyboard.adjust(3).as_markup()