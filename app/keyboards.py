from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)

# Reply-клавиатура
reply_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Записаться на приём")],
        [KeyboardButton(text="Показать телефон менеджера")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню.",
)

# Inline-клавиатура
inline_main = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="YouTube", url="https://youtube.com")]]
)


# Поделиться контактом
button_request_contact = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Поделиться контактом", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


# Вызов менеджера
get_manager = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Показать телефон менеджера")],
    ],
    resize_keyboard=True,
)

# Персональные данные
agree_with_terms = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Согласен"), KeyboardButton(text="Не согласен")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

# Тип записи
booking_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать салон", callback_data="by_salon_at_first")],
        [
            InlineKeyboardButton(
                text="Выбрать мастера", callback_data="by_master_at_first"
            )
        ],
    ]
)

# Подтверждение салона
confirm_salon = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Подтвердить", callback_data="chosen_salon_confirmed"
            )
        ],
    ]
)

# Подтверждение процедуры
confirm_procedure = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Подтвердить", callback_data="chosen_procedure_confirmed"
            )
        ],
    ]
)

# Подтверждение специалиста
confirm_specialist = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Подтвердить", callback_data="chosen_specialist_confirmed"
            )
        ],
    ]
)

# Подтверждение записи
confirm_booking = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="booking_confirmed")],
    ]
)

# Уточню время у менеджера
call_manager_later = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Обязательно", callback_data="time_00:00_00:00")],
    ]
)
