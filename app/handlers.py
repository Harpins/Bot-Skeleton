from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import app.keyboards as kb
import app.builder as builder

router = Router()

#Ожидает команду /start - отправляет приветствие, создает Reply-клавиатуру
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!", reply_markup=kb.reply_main)

#Ожидает в чате сообщение 'фрукты' - отправляет сообщение, создает Reply-клавиатуру через builder  
@router.message(F.text == 'фрукты')
async def cmd_start(message: Message):
    await message.answer("SampleText", reply_markup=builder.make_fruit_buttons())

#Ожидает изображение в чате - высылает ID изображение, затем само изображение
@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f"ID фотографии: {message.photo[-1].file_id}")
    await message.answer_photo(photo=message.photo[-1].file_id)
