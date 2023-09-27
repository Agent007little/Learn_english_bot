# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
from aiogram.fsm.state import StatesGroup, State


class FSMAddWord(StatesGroup):
    fill_word = State()   # Состояние ожидания ввода английского слова.
    fill_translation = State()   # Состояние ожидания ввода перевода слова.
