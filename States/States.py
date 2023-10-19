# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
from aiogram.fsm.state import StatesGroup, State


class FSMAddWord(StatesGroup):
    fill_word = State()   # Состояние ожидания ввода английского слова.
    fill_translation = State()   # Состояние ожидания ввода перевода слова.


class FSMLearnWords(StatesGroup):
    wait_choice = State()
    rus = State()
    eng = State()
    rus_inline_choice = State()
    eng_inline_choice = State()
    rus_input = State()
    eng_input = State()
