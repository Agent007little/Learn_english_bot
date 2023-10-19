from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from lexicon.lexicon import LEXICON_MAIN_COMMANDS

router = Router()


# Хэндлер срабатывает на неизвестные команды от пользователя
@router.message(StateFilter(default_state))
async def process_unknown_command(message: Message):
    await message.answer(LEXICON_MAIN_COMMANDS["unknown_command"])
