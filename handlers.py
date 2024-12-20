from aiogram import Bot, Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
import app.keyboards as kb
import app.builder as builder

router = Router()


#Ожидает команду /start - отправляет приветствие, запрашивает согласие на обработку персональных данных
@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    doc_path = 'app/Personal_data.pdf'
    document = FSInputFile(doc_path)
    await message.answer('Здравствуйте')
    await message.answer_document(
        document=document,
        caption='''Для предоставления вам персонализированных услуг нам необходимо получить ваше согласие на обработку персональных данных''',
        reply_markup=kb.agree_with_terms
        )
    
    
#Не согласен
@router.message(F.text == 'Не согласен')
async def not_agree(message: Message):
    await call_manager(message)

#Вызов менеджера
async def call_manager(message: Message):
    await message.answer("Записаться можно по телефону: `8(800)555-35-35`", parse_mode="MARKDOWN")


#Примеры обработчиков
#Ожидает в чате сообщение 'фрукты' - отправляет сообщение, создает Reply-клавиатуру через builder  
@router.message(F.text == 'фрукты')
async def fruits(message: Message):
    await message.answer("SampleText", reply_markup=builder.make_fruit_buttons())

#Ожидает изображение в чате - высылает ID изображение, затем само изображение
@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f"ID фотографии: {message.photo[-1].file_id}")
    await message.answer_photo(photo=message.photo[-1].file_id)
