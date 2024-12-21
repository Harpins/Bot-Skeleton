from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command
import app.keyboards as kb
import app.builder as builder
import app.utils as utl
from datetime import date

router = Router()

# Словарь для хранения результатов функций
storage = {
    "client": {},
    "specialist": {"user": {"username": ""}},
    "procedure": {"name": "", "price": ""},
    "salon": {},
    "start_time": "",
    "end_time": "",
    "availability": {},
}


# Ожидает команду /start - отправляет приветствие, запрашивает согласие на обработку персональных данных


@router.message(CommandStart())
async def cmd_start(message: Message):
    doc_path = "app/Personal_data.pdf"
    document = FSInputFile(doc_path)
    await message.answer("Здравствуйте")
    await message.answer("Получить телефон менеджера можно по команде /manager")
    await message.answer_document(
        document=document,
        caption="""Для предоставления вам персонализированных услуг нам необходимо получить ваше согласие на обработку персональных данных""",
        reply_markup=kb.agree_with_terms,
    )


# Вызов менеджера


@router.message(Command("manager"))
async def call_manager(message: Message):
    await message.answer(
        "Уточнить информацию можно по телефону: `8(800)555-35-35`",
        parse_mode="MARKDOWN",
    )


# Согласен


@router.message(F.text == "Согласен")
async def get_client_data(message: Message):
    await message.answer(
        "Поделитесь контактными данными чтобы продолжить",
        reply_markup=kb.button_request_contact,
    )


# Не согласен


@router.message(F.text == "Не согласен")
async def not_agree(message: Message):
    await call_manager(message)


# Получение контакта, проверка наличия пользователя в базе, регистрация клиента


@router.message(F.contact)
async def handle_contact(message: Message):
    if message.contact:
        phone_number = message.contact.phone_number
        first_name = message.contact.first_name
        last_name = message.contact.last_name
        user_id = message.from_user.id
        username = f"{first_name}_{last_name}"
        if utl.check_client(user_id, phone_number):
            client = utl.check_client(user_id, phone_number)
        else:
            await message.reply("Сохраняем Ваши данные")
            client = utl.make_client_template(user_id, phone_number, username)
            utl.register_user(client)
        storage["client"] = client
        await choose_booking(message)


# Выбор типа записи


async def choose_booking(message: Message):
    await message.answer("Выберите тип записи:", reply_markup=kb.booking_type)


# Вариант записи салон-услуга-мастер

# Выбрать салон


@router.callback_query(F.data == "by_salon_at_first")
async def choose_salon(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "Выберите салон", reply_markup=builder.make_salons_buttons()
    )


# Обработка выбора салона


@router.callback_query(F.data.startswith("salon_"))
async def handle_salon_callback(callback: CallbackQuery):
    await callback.answer()
    salon_id = int(callback.data.split("_")[1])
    salons = utl.get_salons()
    salon = utl.get_by_id(salons, salon_id)
    if salon:
        storage["salon"] = salon
        await callback.message.answer(
            text=f"{salon['name']}", reply_markup=kb.confirm_salon
        )


# Выбор услуги
@router.callback_query(F.data == "chosen_salon_confirmed")
async def choose_procedure(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "Выберите процедуру", reply_markup=builder.make_procedures_buttons()
    )


# Обработка выбора услуги


@router.callback_query(F.data.startswith("procedure_"))
async def handle_procedure_callback(callback: CallbackQuery):
    await callback.answer()
    procedure_id = int(callback.data.split("_")[1])
    procedures = utl.get_procedures()
    procedure = utl.get_by_id(procedures, procedure_id)
    if procedure:
        storage["procedure"] = procedure
        await callback.message.answer(
            text=f"{procedure['name']}\nОписание процедуры: {procedure['description']}\nСтоимость: {procedure['price']} руб.",
            reply_markup=kb.confirm_procedure,
        )


# Выбор специалиста
@router.callback_query(F.data == "chosen_procedure_confirmed")
async def choose_specialist(callback: CallbackQuery):
    await callback.answer()
    specialists = utl.get_specialists()
    procedure = storage["procedure"]
    salon = storage["salon"]
    filtered_specialists = utl.filter_specialists(specialists, salon, procedure)
    await callback.message.answer(
        "Выберите специалиста",
        reply_markup=builder.make_specialists_buttons(filtered_specialists),
    )


# Обработка выбора специалиста


@router.callback_query(F.data.startswith("specialist_"))
async def handle_specialist_callback(callback: CallbackQuery):
    await callback.answer()
    specialist_id = int(callback.data.split("_")[1])
    specialists = utl.get_specialists()
    specialist = utl.get_by_id(specialists, specialist_id)
    if specialist:
        storage["specialist"] = specialist
        await callback.message.answer(
            text=f"{specialist['user']['username'].replace('_', ' ')}",
            reply_markup=kb.confirm_specialist,
        )


# Выбор свободного времени
@router.callback_query(F.data == "chosen_specialist_confirmed")
async def choose_time(callback: CallbackQuery):
    await callback.answer()
    availabilities = utl.get_availabilities()
    specialist = storage["specialist"]
    salon = storage["salon"]
    found_availabilities = utl.filter_availabilities(availabilities, specialist, salon)
    if found_availabilities:
        occupied_time = utl.get_occupied_time_intervals(found_availabilities)
        free_time = utl.get_free_time_intervals(occupied_time)
        await callback.message.answer(
            "Свободное время", reply_markup=builder.choose_free_time(free_time)
        )
    else:
        await callback.message.answer(
            "Выберите время для записи сегодня",
            reply_markup=builder.choose_any_time(),
        )


# Обработка выбора свободного времени и подтверждение записи
@router.callback_query(F.data.startswith("time_"))
async def handle_choose_time_callback(callback: CallbackQuery):
    await callback.answer()
    start_time = f'{date.today().isoformat()}-{callback.data.split("_")[1]}'
    end_time = f'{date.today().isoformat()}-{callback.data.split("_")[2]}'
    storage["start_time"] = start_time
    storage["end_time"] = end_time
    specialist = storage["specialist"]["user"]["username"].replace("_", " ")
    msg_template = f"Вы записаны на {storage['procedure']['name']}. Стоимость {storage['procedure']['price']} руб.\nСпециалист - {specialist}\nВремя записи по {start_time} по {end_time}"
    await callback.message.answer(msg_template, reply_markup=kb.confirm_booking)


# Обработка подтверждения записи


@router.callback_query(F.data == "booking_confirmed")
async def handle_confirmation_callback(callback: CallbackQuery):
    await callback.answer()
    params = {
        "client": storage["client"],
        "salon": storage["salon"],
        "procedure": storage["procedure"],
        "availability": storage["availability"],
        "price": storage["procedure"]["price"],
        "phone_number": storage["client"]["phone_number"],
        "confirmed": True,
    }
    utl.register_booking(params)
    await callback.message.answer("Запись создана")
    await call_manager(callback.message)
