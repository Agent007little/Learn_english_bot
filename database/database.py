import psycopg2

from config_data.config import load_database, DataBase
from lexicon.lexicon import LEXICON_ADD_WORD

# Загружаем данные БД
db: DataBase = load_database()
# Переменная для установки соединения с БД
connection = psycopg2.connect(
    port=5433,
    user=db.user_db,
    password=db.user_password,
    database=db.name_db)
# Автоматическое сохранение запросов к БД.
connection.autocommit = True


def init_db(force: bool = False):
    """Создаём нужные таблицы если их ещё нет.
    Параметр force в значении True создаст таблицы в базе данных
    или очистит их если они уже созданы и заполнены данными."""
    with connection.cursor() as c:
        if force:
            c.execute("DROP TABLE IF EXISTS users, words, user_word CASCADE")

            c.execute("CREATE TABLE users("
                      "id serial PRIMARY KEY,"
                      "tg_id integer NOT NULL);")

            c.execute("CREATE TABLE words("
                      "id serial PRIMARY KEY,"
                      "eng varchar(255) NOT NULL,"
                      "rus varchar(255) NOT NULL);")

            c.execute("CREATE TABLE user_word("
                      "user_id integer REFERENCES users(id),"
                      "word_id integer REFERENCES words(id),"
                      "CONSTRAINT user_word_id PRIMARY KEY (user_id, word_id));")


async def save_user(telegram_id: int):
    """Функция сохраняющая нового пользователя в БД. Таблица users. """
    with connection.cursor() as c:
        c.execute("INSERT INTO users(tg_id)"
                  "SELECT (%s)"
                  "WHERE NOT EXISTS (SELECT 1 FROM users WHERE tg_id = (%s));", (telegram_id, telegram_id))


async def save_word(eng: str, rus: str, tg_id: int):
    """Функция сохраняет английское слово с переводом в БД. И создаёт зависимость между пользователем и его словарём."""
    with connection.cursor() as c:
        c.execute("INSERT INTO words (eng, rus) "
                  "SELECT %s, %s "
                  "WHERE NOT EXISTS "
                  "(SELECT 1 FROM words WHERE eng = %s AND rus = %s);", (eng, rus, eng, rus))

        c.execute("INSERT INTO user_word (user_id, word_id) "
                  "SELECT users.id, words.id "
                  "FROM users, words "
                  "WHERE users.tg_id = %s "
                  "AND words.eng = %s "
                  "AND words.rus = %s "
                  "ON CONFLICT DO NOTHING;", (tg_id, eng, rus))


async def show_my_dict(user_tg_id):
    """Показывает словарь пользователя. Если он пустой, вернуть текст пустого словаря из лексикона"""
    with connection.cursor() as c:
        c.execute("SELECT words.eng, words.rus "
                  "FROM users "
                  "JOIN user_word ON users.id = user_word.user_id "
                  "JOIN words ON user_word.word_id = words.id "
                  "WHERE users.tg_id = (%s);", (user_tg_id,))
        result_str = ''
        fetchall = c.fetchall()
        if fetchall:
            for i in fetchall:
                result_str += f"{i[0]} - {i[1]}\n"
            return result_str
        else:
            return LEXICON_ADD_WORD["empty_dict"]


def get_user_dict_eng_rus(user_tg_id: int) -> dict[str: str]:
    """Создаёт англо-русский словарь пользователя."""
    with connection.cursor() as c:
        c.execute("SELECT words.eng, words.rus "
                  "FROM users "
                  "JOIN user_word ON users.id = user_word.user_id "
                  "JOIN words ON user_word.word_id = words.id "
                  "WHERE users.tg_id = (%s);", (user_tg_id,))
        fetchall: list[tuple[str: str]] = c.fetchall()
        result_dict = dict()
        for i in fetchall:
            result_dict[i[0]] = i[1]
        return result_dict


def get_word_from_db(eng: str):
    """Возвращает перевод английского слова, если он существует."""
    with connection.cursor() as c:
        c.execute("SELECT rus "
                  "FROM words "
                  "WHERE eng = %s;", (eng,))
        fetchall: list[tuple[str]] = c.fetchall()
        if not fetchall:
            return None
        result_str = ""
        for item in fetchall:
            result_str = result_str + item[0] + ", "
        return result_str[:-2]

