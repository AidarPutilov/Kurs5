from src.db_manager import DBManager
from src.head_hunter_api import HeadHunterAPI
from src.settings import DATABASE_INI_FILE, LIST_EMPLOYERS
from src.utils import db_config, user_dialog, create_db


def main():
    # Чтение или создание файла с настройками БД
    db_config_data = db_config(DATABASE_INI_FILE)

    # Создание БД
    print('Создание базы данных и таблиц...')
    create_db('hh', db_config_data)

    # Создание объекта для работы с БД
    hh_db = DBManager(dbname='hh',
                      employers_table='employers',
                      vacancies_table='vacancies',
                      **db_config_data)

    # Получение данных от HH
    print('Получение данных от Head Hunter и заполнение базы данных...')
    for employer in LIST_EMPLOYERS:
        # Получение данных из HH
        hh_api = HeadHunterAPI(employer)
        hh_employer = hh_api.get_employer()
        hh_vacancies = hh_api.get_vacancies()

        # Заполнение базы данных
        hh_db.insert_data(hh_employer, hh_vacancies)

    # Диалог с пользователем
    user_dialog(hh_db)

    # Удаление объекта, закрытие БД
    print('Программа завершена')
    del hh_db


if __name__ == '__main__':
    main()
