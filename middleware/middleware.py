from database.database import get_user_dict_eng_rus

users_dicts_eng_rus = dict()


# Заполняем словарь нужными нам значениями.
async def create_users_dicts_eng_rus(user_tg_id: int):
    global users_dicts_eng_rus
    users_dicts_eng_rus[user_tg_id] = get_user_dict_eng_rus(user_tg_id)
    return None


# генератор для получения слова из словаря пользователя.
def get_first_rus_word(user_tg_id: int):
    return list(users_dicts_eng_rus[user_tg_id].values())[0]


def get_first_eng_word(user_tg_id: int):
    return list(users_dicts_eng_rus[user_tg_id].keys())[0]


def delete_word(user_td_id: int):
    del users_dicts_eng_rus[user_td_id][get_first_eng_word(user_td_id)]

