import logging
from pathlib import Path
from configparser import ConfigParser


# Каталог с проектом
ROOT_PATH = Path(__file__).parent.parent

# URL с вакансиями HH
HH_VACANCIES_URL = 'https://api.hh.ru/vacancies'

# URL с вакансиями HH
HH_EMPLOYERS_URL = 'https://api.hh.ru/employers'

# Формат логов
FORMAT = '%(asctime)-30s %(filename)-20s %(message)s'

logging.basicConfig(level=logging.INFO, filename='main.log', filemode='w', format=FORMAT)

# Файл с настройками базы данных
DATABASE_INI_FILE = ROOT_PATH.joinpath('data', 'database.ini')

# Список id работодателей
LIST_EMPLOYERS = [
    # '3529',
    # '242574',
    # '1073798',
    # '208707',
    # '15356',
    # '1212051',
    # '3776',
    # '3676',
    '2334525',
    '4495459'
]


def config(filename: str, section: str) -> dict:
    # Создание парсера
    parser = ConfigParser()
    # Чтение файла
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Секция {section} в файле {filename} не найдена.')
    return db


def create_db_config() -> dict:
    # Создание файла конфигурации с секцией postgresql
    # Запрос данных у пользователя
    print('Введите параметры для поключения к БД')
    host = input('host [localhost]:').lower()
    user = input('user [postgres]:').lower()
    password = input('password [postgres]:').lower()
    port = input('port [5432]:').lower()
    # Начальные данные
    filename = DATABASE_INI_FILE
    section = 'postgresql'
    db = {}
    # Обработка введённых данных
    db['host'] = host if host != '' else 'localhost'
    db['user'] = user if user != '' else 'postgres'
    db['password'] = password if password != '' else 'postgres'
    db['port'] = port if port != '' else '5432'
    # Создание парсера
    db_config = ConfigParser()
    # Заполнение данных парсера
    db_config[section] = db
    # Запись в файл
    with open(DATABASE_INI_FILE, 'w') as configfile:
        db_config.write(configfile)
    # Возврат данных БД
    return db


if __name__ == '__main__':
    pass