import psycopg2


class DBManager:
    """ Класс для работы с базой данных вакансий и работодателей HH """

    def __init__(self, dbname: str,
                 employers_table: str,
                 vacancies_table: str,
                 host: str, user: str,
                 password: str,
                 port: str):
        self.employers_table = employers_table
        self.vacancies_table = vacancies_table
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self._drop_tables()
        self._create_tables()

    def __del__(self):
        self.conn

    def _drop_tables(self):
        """ Удаление таблиц """
        with self.conn:
            self.cur.execute(f"""
            DROP TABLE IF EXISTS {self.vacancies_table}, {self.employers_table};
            """)

    def _create_tables(self):
        """ Создание таблиц """
        with self.conn:
            self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.employers_table} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULl,
            url VARCHAR(255)
            );
            """)
            self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.vacancies_table} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            employer_id INT REFERENCES {self.employers_table}(id),
            salary VARCHAR(50),
            mid_salary INT,
            url VARCHAR(255)
            );
            """)

    def insert_data(self, employer: dict, vacancies: list[dict]) -> None:
        """ Добавление данных в БД """
        with self.conn:
            self.cur.execute(
                f"INSERT INTO {self.employers_table} (name, url) VALUES (%s, %s) RETURNING id",
                (employer['name'], employer['url']))
            employer_id = self.cur.fetchone()[0]
            for vacancy in vacancies:
                self.cur.execute(
                    f"INSERT INTO {self.vacancies_table} "
                    f"(name, employer_id, salary, mid_salary, url) "
                    f"VALUES (%s, %s, %s, %s, %s)",
                    (vacancy['name'], employer_id, vacancy['salary'], vacancy['mid_salary'], vacancy['url']))

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """ Получает список всех компаний и количество вакансий у каждой компании """
        with self.conn:
            self.cur.execute(f"SELECT {self.employers_table}.name, "
                             f"COUNT({self.vacancies_table}.id) "
                             f"FROM {self.employers_table} "
                             f"JOIN {self.vacancies_table} "
                             f"ON {self.employers_table}.id={self.vacancies_table}.employer_id "
                             f"GROUP BY {self.employers_table}.name;")
            return self.cur.fetchall()

    def get_all_vacancies(self) -> list[tuple]:
        """ Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию """
        with self.conn:
            self.cur.execute(f"SELECT {self.employers_table}.name, "
                             f"{self.vacancies_table}.name, "
                             f"{self.vacancies_table}.salary, "
                             f"{self.vacancies_table}.url "
                             f"FROM {self.employers_table} "
                             f"JOIN {self.vacancies_table} "
                             f"ON {self.employers_table}.id={self.vacancies_table}.employer_id ")
            return self.cur.fetchall()

    def get_avg_salary(self) -> list[tuple]:
        """ Получает среднюю зарплату по вакансиям """
        with self.conn:
            self.cur.execute(f"SELECT {self.employers_table}.name, "
                             f"AVG({self.vacancies_table}.mid_salary) "
                             f"FROM {self.employers_table} "
                             f"JOIN {self.vacancies_table} "
                             f"ON {self.employers_table}.id={self.vacancies_table}.employer_id "
                             f"GROUP BY {self.employers_table}.name")
            return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям """
        with self.conn:
            self.cur.execute(f"SELECT {self.employers_table}.name, "
                             f"{self.vacancies_table}.name, "
                             f"{self.vacancies_table}.salary, "
                             f"{self.vacancies_table}.url "
                             f"FROM {self.employers_table} "
                             f"JOIN {self.vacancies_table} "
                             f"ON {self.employers_table}.id={self.vacancies_table}.employer_id "
                             f"WHERE {self.vacancies_table}.mid_salary >"
                             f"(SELECT AVG(mid_salary) FROM vacancies)")
            return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keywords: list[str]) -> list[tuple]:
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова """
        where_params = ' AND '.join([f"{self.vacancies_table}.name ILIKE '%{keyword}%'" for keyword in keywords])
        with self.conn:
            self.cur.execute(f"SELECT {self.employers_table}.name, "
                             f"{self.vacancies_table}.name, "
                             f"{self.vacancies_table}.salary, "
                             f"{self.vacancies_table}.url "
                             f"FROM {self.employers_table} "
                             f"JOIN {self.vacancies_table} "
                             f"ON {self.employers_table}.id={self.vacancies_table}.employer_id "
                             f"WHERE {where_params}")
            return self.cur.fetchall()


if __name__ == '__main__':
    pass
