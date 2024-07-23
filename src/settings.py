import logging
from pathlib import Path


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
    '1073798',
    '15356',
    '1212051',
    '3676',
    '2334525',
    '4495459',
    '1480111',
    '4586593',
    '1473395',
    '1513283'
]


if __name__ == '__main__':
    pass
