import requests
from requests import JSONDecodeError

from src.exceptions import HeadHunterAPIException
from src.settings import HH_VACANCIES_URL, HH_EMPLOYERS_URL, LIST_EMPLOYERS


class HeadHunterAPI():
    """ Класс для работы с API HeadHunter """

    def __init__(self, employer_id: str) -> None:
        self.employer_id = employer_id
        self.employers_url = HH_EMPLOYERS_URL
        self.vacancies_url = HH_VACANCIES_URL
        self.headers = {'User-Agent': 'HH-User-Agent'}

    def get_employer(self) -> dict:
        """ Выполнение запроса к HH, получение информации о работодателе, обработка простых ошибок """
        params = {'locale': 'RU'}
        result = []
        response = requests.get(self.employers_url + '/' + self.employer_id,
                                headers=self.headers, params=params)
        is_allowed = response.status_code == 200
        if not is_allowed:
            raise HeadHunterAPIException(f'Ошибка запроса данных status_code: {response.status_code}, {response.text}')
        try:
            employer = response.json()
        except JSONDecodeError:
            raise HeadHunterAPIException(f'Ошибка обработки данных данных {response.text}')
        result.append({'id': employer['id'], 'name': employer['name']})
        return result


    def get_vacancies(self) -> dict:
        """ Выполнение запроса к HH, получение вакансий работодателей, обработка простых ошибок """
        result = []
        page = 0
        while True:
            params = {
                'employer_id': int(self.employer_id),
                'area': 113,
                'page': page,
                'per_page': 100
            }
            response = requests.get(self.vacancies_url, headers=self.headers, params=params)
            is_allowed = response.status_code == 200
            if not is_allowed:
                raise HeadHunterAPIException(f'Ошибка запроса данных status_code: {response.status_code}, {response.text}')
            try:
                vacancies = response.json()['items']
            except JSONDecodeError:
                raise HeadHunterAPIException(f'Ошибка обработки данных данных {response.text}')
            for vacancy in vacancies:
                result.append({'id': vacancy['id'],
                               'name': vacancy['name'],
                               'employer': vacancy['employer']['name'],
                               'salary': self.verify_salary(vacancy.get('salary')),
                               'mid_salary': self.get_middle_salary(vacancy.get('salary'))
                              })
                #print(vacancy)
            page += 1
            if response.json()['pages'] == page:
                break
        return result

    @staticmethod
    def verify_salary(salary: dict) -> str:
        """ Генерация строки с зарплатой, валидация """
        if not salary:
            return 'Зарплата не указана'
        if salary['from'] and salary['to']:
            if salary['from'] == salary['to']:
                return f'{salary['to']} {salary['currency']}'
            return f'{salary['from']}..{salary['to']} {salary['currency']}'
        elif salary['from'] and not salary['to']:
            return f'От {salary['from']} {salary['currency']}'
        elif not salary['from'] and salary['to']:
            return f'До {salary['to']} {salary['currency']}'

    @staticmethod
    def get_middle_salary(salary: dict):
        """ Вычисление среднего значения зарплаты """
        if not salary:
            return 0
        if salary['from'] and salary['to']:
            return round(0.5 * (int(salary['from']) + int(salary['to'])))
        elif salary['to']:
            return int(salary['to'])
        elif salary['from']:
            return int(salary['from'])


if __name__ == '__main__':
    pass

    # hh = HeadHunterAPI('2334525')
    #
    # vac = hh.get_vacancies()
    # empl = hh.get_employer()
    #
    # print(empl)
    # [print(v) for v in vac]
