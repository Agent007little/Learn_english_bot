import re


def only_english(s):
    pattern = re.compile(r"^[a-zA-Z\' ]+$")
    word = pattern.search(s)
    return True if word else False


def only_russian(s):
    pattern = re.compile(r"^[а-яА-Я ]+$")
    word = pattern.search(s)
    return True if word else False
