from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from lexicon.lexicon import LEXICON
router = Router()


# Этот хэндлер будет срабатывать на команду /start вне состояний
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    # Сделать добавление нового пользователя в БД при начале общения с ботом.


@router.message(Command(commands="help"))
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])



