from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random

from lexicon.lexicon import bot_dict_eng_words, bot_dict_rus_words


# Функция, генерирующая клавиатуру для выбора языка изучения слов.
def create_choice_lang():
    kb_builder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками.
    kb_builder.row(InlineKeyboardButton(text="Русский", callback_data="Русский"),
                   InlineKeyboardButton(text="English", callback_data="English"),
                   width=2)
    return kb_builder.as_markup()


# Функция, генерирующая клавиатуру для выбора режима изучения слов.
def create_choice_mode():
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text="C вариантами ответа", callback_data="Inline"),
                   InlineKeyboardButton(text="Напишу слово сам", callback_data="Input", ),
                   width=2)

    return kb_builder.as_markup()


# Создание инлайн клавиатуры для выбора английских слов. На вход получает слово, которое должно быть ответом.
def create_english_choice_markup(answer: str):
    kb_builder = InlineKeyboardBuilder()
    inline_buttons = english_random_markup(answer)
    kb_builder.row(*inline_buttons, width=2)

    return kb_builder.as_markup()


# Создаёт рандомные инлайн кнопки на английском. На вход получает слово, которое должно быть ответом.
def english_random_markup(answer: str) -> list[InlineKeyboardButton]:
    result_buttons = list()
    # Заполнить список 1 правильной кнопкой
    result_buttons.append(InlineKeyboardButton(text=answer, callback_data="right"))
    # Добавить 3 неверных ответа с рандомными словами из общего словаря.
    random_words = random.sample(bot_dict_eng_words, 3)
    for word in random_words:
        result_buttons.append(InlineKeyboardButton(text=word, callback_data="wrong"))
    # Перемешать кнопки
    random.shuffle(result_buttons)
    return result_buttons


# Создание инлайн клавиатуры для выбора русских слов. На вход получает слово, которое должно быть ответом.
def create_russian_choice_markup(answer: str):
    kb_builder = InlineKeyboardBuilder()
    inline_buttons = russian_random_markup(answer)
    kb_builder.row(*inline_buttons, width=2)

    return kb_builder.as_markup()


# Создаёт рандомные инлайн кнопки на русском. На вход получает слово, которое должно быть ответом.
def russian_random_markup(answer: str) -> list[InlineKeyboardButton]:
    result_buttons = list()
    # Заполнить список 1 правильной кнопкой
    result_buttons.append(InlineKeyboardButton(text=answer, callback_data="right"))
    # Добавить 3 неверных ответа с рандомными словами из общего словаря.
    random_words = random.sample(bot_dict_rus_words, 3)
    for word in random_words:
        result_buttons.append(InlineKeyboardButton(text=word, callback_data="wrong"))
    # Перемешать кнопки
    random.shuffle(result_buttons)
    return result_buttons
