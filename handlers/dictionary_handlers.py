from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from database.database import save_word, show_my_dict, get_word_from_db
from filters.filters import only_english, only_russian

from States.States import FSMAddWord
from lexicon.lexicon import LEXICON_ADD_WORD

router = Router()

users_add_word_dict = {}  # dict[int[str:str]]


# Хэндлер для команды /my_dict
@router.message(Command(commands=["my_dict"]), StateFilter(default_state))
async def process_my_dict_command(message: Message):
    text = await show_my_dict(message.from_user.id)
    await message.answer(text=text)


# Этот хэндлер срабатывает на команду /add_word.
# Переводит в состояние ожидания ввода английского слова.
@router.message(Command(commands="add_word"), StateFilter(default_state))
async def process_add_word_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADD_WORD[message.text])
    # Устанавливаем состояние ожидания ввода слова
    await state.set_state(FSMAddWord.fill_word)


# Этот хэндлер срабатывает если введено слово без цифр и прочих знаков
# Переводит в состояние ожидания ввода перевода слова.
@router.message(StateFilter(FSMAddWord.fill_word), lambda x: only_english(x.text))
async def process_word_sent(message: Message, state: FSMContext):
    # Добавляем в временный словарь английское слово.
    users_add_word_dict[message.from_user.id] = {"eng": message.text.lower(), "rus": ""}
    # Получаем возможный перевод
    possible_translation = get_word_from_db(users_add_word_dict[message.from_user.id]["eng"])
    if possible_translation:
        await message.answer(text=LEXICON_ADD_WORD["offer_translation"] + possible_translation)
    else:
        await message.answer(text=LEXICON_ADD_WORD["word_sent"])
    # Устанавливаем состояние ожидания ввода перевода
    await state.set_state(FSMAddWord.fill_translation)


# Этот хэндлер срабатывает если английское слово введено неверно.
@router.message(StateFilter(FSMAddWord.fill_word))
async def warning_no_english(message: Message):
    await message.answer(text=LEXICON_ADD_WORD["warning_no_english"])


# Этот хэндлер срабатывает после ввода перевода.
# Переводит в стандартное состояние.
# Сохраняет слово с переводом в БД.
@router.message(StateFilter(FSMAddWord.fill_translation), lambda x: only_russian(x.text))
async def process_translation_sent(message: Message, state: FSMContext):
    users_add_word_dict[message.from_user.id]["rus"] = message.text.lower()
    eng, rus = users_add_word_dict[message.from_user.id]["eng"], users_add_word_dict[message.from_user.id]["rus"]
    await save_word(eng, rus, int(message.from_user.id))
    await message.answer(LEXICON_ADD_WORD["translation_sent"])
    # Перевод в стандартное состояние.
    await state.clear()
    del users_add_word_dict[message.from_user.id]


# Этот хэндлер срабатывает если перевод введёт некорректно.
@router.message(StateFilter(FSMAddWord.fill_translation))
async def warning_no_russian(message: Message):
    await message.answer(text=LEXICON_ADD_WORD["warning_no_russian"])
