from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

#Reply-клавиатура
reply_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Записаться на приём")],
        [KeyboardButton(text="Показать телефон менеджера")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню.",
)

#Inline-клавиатура
inline_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='YouTube', url='https://youtube.com')]
])