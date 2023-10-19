LEXICON_MAIN_COMMANDS: dict[str: str] = {
    "/start": "Это бот для изучения английского языка.\n"
              "Я умею вести словарь английских слов.\n"
              "Введи команду /add_word, чтобы добавить новое слово.\n"
              "Введи команду /my_dict, чтобы посмотреть свой словарь.\n"
              "Можем учить твои слова из словаря с помощью команды /learn_words.\n"
              "В любой момент напиши команду /help и я помогу тебе."
              "Все эти команды есть в быстром доступе во вкладке 'Меню'.",
    "/help": "Это бот для изучения английского.\n"
             "Я умею вести ваш личный словарь и учить ваши записанные слова.\n"
             "Для добавления нового слова введите /add_word.\n"
             "Чтобы увидеть ваш словарь введите /my_dict.\n"
             "Можем учить твои слова из словаря с помощью команды /learn_words.\n",
    "unknown_command": "Я пока не знаю этой команды."
}

LEXICON_ADD_WORD: dict[str: str] = {
    "/add_word": "Введите английское слово для добавления в словарь",
    "word_sent": "Отлично! Теперь введите перевод.",
    "offer_translation": "Введите перевод на русском.\n"
                         "Вот так это слово перевели другие пользователи: ",
    "empty_dict": "Ваш словарь пустой.\nДобавьте слова с помощью команды /add_word",
    "warning_no_english": "Введите английское слово, без цифр и знаков препинания.",
    "translation_sent": "Перевод успешно сохранён.",
    "warning_no_russian": "Введите перевод на русском, без цифр и знаков препинания."
}

LEXICON_COMMANDS_MENU: dict[str: str] = {
    "/add_word": "Добавить новое слово в свой словарь.",
    "/my_dict": "Показывает все ваши слова из словаря.",
    "/learn_words": "Учить слова из моего словаря.",
    "/help": "Помощь в любой ситуации."
}

LEXICON_LEARN_WORDS: dict[str: str] = {
    "/learn_words": "С какого языка вы хотите переводить слова?",
    "choice_mode": "Какой режим вы выбираете?",
    "right_word": "Верно!\n\n",
    "right_word_end": "Верно!\n\nВы повторили все слова.",
    "wrong_word": "Перевод не верный.",
    "unknown_command_wait_choice": "Выберите язык с на котором будут появляться слова.\n"
                                   "Вы будете переводить на другой язык.",
    "unknown_command_rus_eng_state": "Выберите режим в котором вы будете учить слова."
}

bot_dict_eng_words = []
bot_dict_rus_words = []

with open("lexicon\dict_eng_words.txt", "r", encoding="utf-8") as file:
    words = file.readlines()
    for word in words:
        bot_dict_eng_words.append(word.rstrip())

with open("lexicon\dict_rus_words.txt", "r", encoding="utf-8") as file:
    words = file.readlines()
    for word in words:
        bot_dict_rus_words.append(word.rstrip())