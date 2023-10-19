from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from States.States import FSMLearnWords
from keyboards.learn_words_kb import create_choice_lang, create_choice_mode, create_english_choice_markup, \
    create_russian_choice_markup
from lexicon.lexicon import LEXICON_LEARN_WORDS
from middleware.middleware import get_first_rus_word, create_users_dicts_eng_rus, get_first_eng_word, delete_word

router = Router()


# Хэндлер на команду /learn_words. Выводит 2 инлайн кнопки. Учить слова на русском или английском
@router.message(Command(commands=(["learn_words"])), StateFilter(default_state))
async def process_start_learn_words(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_LEARN_WORDS["/learn_words"], reply_markup=create_choice_lang())
    await state.set_state(FSMLearnWords.wait_choice)


# Хэндлер срабатывает если пользователь не нажимает на инлайн кнопку выбора языка.
@router.message(StateFilter(FSMLearnWords.wait_choice))
async def process_unknown_command_wait_choice_state(message: Message):
    await message.answer(text=LEXICON_LEARN_WORDS["unknown_command_wait_choice"], reply_markup=create_choice_lang())


# Хэндлер срабатывает на нажатие инлайн кнопки выбора языка.
# Выводит сообщение с ожиданием выбора режима. Выбор инлайн кнопок или ручной ввод слов.
@router.callback_query(F.data.in_({"English", "Русский"}))
async def process_choice_lang(callback: CallbackQuery, state: FSMContext):
    # Переводим в состояние выбранного языка.
    if callback.data == "Русский":
        await state.set_state(FSMLearnWords.rus)
    else:
        await state.set_state(FSMLearnWords.eng)
    # Отвечаем и создаём клавиатуру выбора режима.
    await callback.message.answer(text=LEXICON_LEARN_WORDS["choice_mode"], reply_markup=create_choice_mode())
    await callback.answer()


# Хэндлер срабатывает если пользователь не нажимает на инлайн кнопку выбора режима.
@router.message(StateFilter(FSMLearnWords.eng, FSMLearnWords.rus))
async def process_unknown_command_rus_eng_state(message: Message):
    await message.answer(LEXICON_LEARN_WORDS["unknown_command_rus_eng_state"], reply_markup=create_choice_mode())


# Хэндлер начала изучения русских слов с полным вводом от пользователя. Выводить русские, ожидать английские.
@router.callback_query(F.data == "Input", StateFilter(FSMLearnWords.rus))
async def process_input_eng(callback: CallbackQuery, state: FSMContext):
    # Переводим в состояние изучения слов.
    await state.set_state(FSMLearnWords.eng_input)
    # Формируем dict пользователя для обучения.
    await create_users_dicts_eng_rus(callback.from_user.id)
    # Выводим первое слово.
    answer = get_first_rus_word(callback.from_user.id)
    await callback.message.answer(answer)
    await callback.answer()


# Хэндлер для изучения слов. Пользователь вводит английские слова самостоятельно.
# Если всё повторил, переводим в начальное состояние.
@router.message(StateFilter(FSMLearnWords.eng_input))
async def process_input_eng_continue(message: Message, state: FSMContext):
    if message.text == get_first_eng_word(message.from_user.id):
        try:
            delete_word(message.from_user.id)
            await message.answer(text=LEXICON_LEARN_WORDS["right_word"] + get_first_rus_word(message.from_user.id))
        except Exception:
            await message.answer(text=LEXICON_LEARN_WORDS["right_word_end"])
            await state.set_state(default_state)
    else:
        await message.answer(text=LEXICON_LEARN_WORDS["wrong_word"])


# Хэндлер начала изучения русских слов с выбором инлайн кнопок. Кнопки на английском.
@router.callback_query(F.data == "Inline", StateFilter(FSMLearnWords.rus))
async def process_inline_eng(callback: CallbackQuery, state: FSMContext):
    # Переход в состояние инлайн выбора английских кнопок.
    await state.set_state(FSMLearnWords.eng_inline_choice)
    # Формируем dict пользователя для обучения.
    await create_users_dicts_eng_rus(callback.from_user.id)
    # Выводим первый выбор инлайн кнопок
    answer_rus = get_first_rus_word(callback.from_user.id)
    answer_eng = get_first_eng_word(callback.from_user.id)
    await callback.message.answer(text=answer_rus, reply_markup=create_english_choice_markup(answer_eng))
    await callback.answer()


# Хэндлер изучения слов. Инлайн кнопки на английском языке.
# Если неверно нотификация ошибки. Если верно след инлайн клавиатура
# Если весь словарь повторён, переход в начальное состояние
@router.callback_query(StateFilter(FSMLearnWords.eng_inline_choice))
async def process_inline_eng_continue(callback: CallbackQuery, state: FSMContext):
    if callback.data == "wrong":
        await callback.answer(text="Неверный ответ.")
    if callback.data == "right":
        try:
            delete_word(callback.from_user.id)
            answer_eng = get_first_eng_word(callback.from_user.id)
            await callback.message.answer(
                text=LEXICON_LEARN_WORDS["right_word"] + get_first_rus_word(callback.from_user.id),
                reply_markup=create_english_choice_markup(answer_eng))
            await callback.answer()
        except Exception:
            await callback.message.answer(text=LEXICON_LEARN_WORDS["right_word_end"])
            await state.set_state(default_state)


# Хэндлер начала изучения английских слов с полным вводом от пользователя. Ожидается ввод русских слов.
@router.callback_query(F.data == "Input", StateFilter(FSMLearnWords.eng))
async def process_input_rus(callback: CallbackQuery, state: FSMContext):
    # Переводим в состояние изучения слов.
    await state.set_state(FSMLearnWords.rus_input)
    # Формируем dict пользователя для обучения.
    await create_users_dicts_eng_rus(callback.from_user.id)
    # Выводим первое слово.
    answer = get_first_eng_word(callback.from_user.id)
    await callback.message.answer(answer)
    await callback.answer()


# Хэндлер для изучения слов. Пользователь вводит русские слова самостоятельно.
# Если всё повторил, переводим в начальное состояние.
@router.message(StateFilter(FSMLearnWords.rus_input))
async def process_input_rus_continue(message: Message, state: FSMContext):
    if message.text == get_first_rus_word(message.from_user.id):
        try:
            delete_word(message.from_user.id)
            await message.answer(text=LEXICON_LEARN_WORDS["right_word"] + get_first_eng_word(message.from_user.id))
        except Exception:
            await message.answer(text=LEXICON_LEARN_WORDS["right_word_end"])
            await state.set_state(default_state)
    else:
        await message.answer(text=LEXICON_LEARN_WORDS["wrong_word"])


# Хэндлер начала изучения английских слов с выбором инлайн кнопок. Кнопки на русском.
@router.callback_query(F.data == "Inline", StateFilter(FSMLearnWords.eng))
async def process_inline_rus(callback: CallbackQuery, state: FSMContext):
    # Переход в состояние инлайн выбора русских кнопок.
    await state.set_state(FSMLearnWords.rus_inline_choice)
    # Формируем dict пользователя для обучения.
    await create_users_dicts_eng_rus(callback.from_user.id)
    # Выводим первый выбор инлайн кнопок
    answer_rus = get_first_rus_word(callback.from_user.id)
    answer_eng = get_first_eng_word(callback.from_user.id)
    await callback.message.answer(text=answer_eng, reply_markup=create_russian_choice_markup(answer_rus))
    await callback.answer()


# Хэндлер изучения слов. Инлайн кнопки на русском языке.
# Если неверно - нотификация ошибки. Если верно след инлайн клавиатура.
# Если весь словарь повторён, переход в начальное состояние.
@router.callback_query(StateFilter(FSMLearnWords.rus_inline_choice))
async def process_inline_eng_continue(callback: CallbackQuery, state: FSMContext):
    if callback.data == "wrong":
        await callback.answer(text="Неверный ответ.")
    if callback.data == "right":
        try:
            delete_word(callback.from_user.id)
            answer_rus = get_first_rus_word(callback.from_user.id)
            await callback.message.answer(
                text=LEXICON_LEARN_WORDS["right_word"] + get_first_eng_word(callback.from_user.id),
                reply_markup=create_russian_choice_markup(answer_rus))
            await callback.answer()
        except Exception:
            await callback.message.answer(text=LEXICON_LEARN_WORDS["right_word_end"])
            await state.set_state(default_state)
            await callback.answer()