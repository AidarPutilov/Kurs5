import psycopg2
from pathlib import Path
from configparser import ConfigParser
from src.db_manager import DBManager
from src.settings import DATABASE_INI_FILE


def db_config(filename: str) -> dict:
    # Функция чтения или создания файла кофигурации БД
    section = 'postgresql'
    # Создание парсера
    parser = ConfigParser()
    # Чтение файла
    if Path(filename).exists():
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f'Секция {section} в файле {filename} не найдена.')
        return db
    # Создание файла конфигурации с секцией postgresql
    # Запрос данных у пользователя
    print('Введите параметры для поключения к БД')
    host = input('host [localhost]:').lower()
    user = input('user [postgres]:').lower()
    password = input('password [postgres]:').lower()
    port = input('port [5432]:').lower()
    # Начальные данные
    db = {}
    # Обработка введённых данных
    db['host'] = host if host != '' else 'localhost'
    db['user'] = user if user != '' else 'postgres'
    db['password'] = password if password != '' else 'postgres'
    db['port'] = port if port != '' else '5432'
    # Создание парсера
    config = ConfigParser()
    # Заполнение данных парсера
    config[section] = db
    # Запись в файл
    with open(DATABASE_INI_FILE, 'w') as configfile:
        config.write(configfile)
    # Возврат данных БД
    return db


def create_db(dbname: str, db: dict) -> None:
    """ Cоздание рабочей базы данных """
    conn = psycopg2.connect(dbname='postgres', **db)
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f'CREATE DATABASE {dbname}')
    except:
        pass
    cur.close()
    conn.close()


def user_dialog(hh_db: DBManager) -> None:
    """ Диалог с пользователем, вывод результатов выборки БД """
    while True:
        print('1 - Список всех компаний и количество вакансий у каждой компании\n'
              '2 - Список всех вакансий с указанием названия компании,'
              'названия вакансии и зарплаты и ссылки на вакансию\n'
              '3 - Средняя зарплату по вакансиям\n'
              '4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
              '5 - Список всех вакансий, в названии которых содержатся переданные в метод слова\n'
              '0 - Выход')
        user_input = input('Выберите действие: ')
        if user_input == '0':
            break
        elif user_input == '1':
            # Список всех компаний и количество вакансий у каждой компании
            companies_and_vacancies_counts = hh_db.get_companies_and_vacancies_count()
            [print(f'{a[0]} - {a[1]} вакансий') for a in companies_and_vacancies_counts]
            print(f'{len(companies_and_vacancies_counts)} записей')
        elif user_input == '2':
            # Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
            all_vacancies = hh_db.get_all_vacancies()
            [print(f'{a[0]}, {a[1]}, Зарплата: {a[2]}, URL: {a[3]}') for a in all_vacancies]
            print(f'{len(all_vacancies)} записей')
        elif user_input == '3':
            # Средняя зарплата по вакансиям
            avg_salary = hh_db.get_avg_salary()
            [print(f'{a[0]} - {int(a[1])} RUR') for a in avg_salary]
            print(f'{len(avg_salary)} записей')
        elif user_input == '4':
            # Список всех вакансий, у которых зарплата выше средней по всем вакансиям
            vacancies_with_higher_salary = hh_db.get_vacancies_with_higher_salary()
            [print(f'{a[0]}, {a[1]}, Зарплата: {a[2]}, URL: {a[3]}') for a in vacancies_with_higher_salary]
            print(f'{len(vacancies_with_higher_salary)} записей')
        elif user_input == '5':
            # Список всех вакансий, в названии которых содержатся переданные в метод слова
            keywords_str = input('Введите ключевые слова через пробел, например "сотрудник склада": ')
            keywords = keywords_str.split()
            vacancies_with_keyword = hh_db.get_vacancies_with_keyword(keywords)
            [print(f'{a[0]}, {a[1]}, Зарплата: {a[2]}, URL: {a[3]}') for a in vacancies_with_keyword]
            print(f'{len(vacancies_with_keyword)} записей')
        else:
            print('Ошибка ввода')


if __name__ == '__main__':
    pass
