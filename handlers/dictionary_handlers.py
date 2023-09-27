from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from filters.filters import only_english, only_russian

from States.States import FSMAddWord
from lexicon.lexicon import LEXICON

router = Router()


# Этот хэндлер срабатывает на команду /add_word.
# Переводит в состояние ожидания ввода английского слова.
@router.message(Command(commands="add_word"), StateFilter(default_state))
async def process_add_word_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON[message.text])
    # Устанавливаем состояние ожидания ввода слова
    await state.set_state(FSMAddWord.fill_word)


# Этот хэндлер срабатывает если введено слово без цифр и прочих знаков
# Переводит в состояние ожидания ввода перевода слова.
@router.message(StateFilter(FSMAddWord.fill_word), lambda x: only_english(x.text))
async def process_word_sent(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["word_sent"])
    # Устанавливаем состояние ожидания ввода перевода
    await state.set_state(FSMAddWord.fill_translation)


# Этот хэндлер срабатывает если английское слово введено неверно.
@router.message(StateFilter(FSMAddWord.fill_word))
async def warning_no_english(message: Message):
    await message.answer(text=LEXICON["warning_no_english"])


# Этот хэндлер срабатывает после ввода перевода.
# Переводит в стандартное состояние.
# Сохраняет слово с переводом в БД.
@router.message(StateFilter(FSMAddWord.fill_translation), lambda x: only_russian(x.text))
async def process_translation_sent(message: Message, state: FSMContext):
    # Тут нужно сохранить данные в БД!!!!!!!!!!!!!!!!!!!!!!!!!

    await message.answer(LEXICON["translation_sent"])
    # Перевод в стандартное состояние.
    await state.clear()


# Этот хэндлер срабатывает если перевод введёт некорректно.
@router.message(StateFilter(FSMAddWord.fill_translation))
async def warning_no_russian(message: Message):
    await message.answer(text=LEXICON["warning_no_russian"])
