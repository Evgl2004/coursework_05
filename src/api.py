from abc import ABC, abstractmethod
from os import getenv

import requests


class API(ABC):
    """
    Абстрактный класс.
    Общие методы для всех потомков:
    1. Получить ответ на запрос к веб-порталу по API.
    2. Получить информацию о работодателе с веб-портала по API.
    3. Получить список вакансий с веб-портала по API.
    """
    __slots__ = ('__url_api', '__result_list', '__headers', '__params')

    @abstractmethod
    def get_requests(self):
        """
        Получить ответ на запрос к веб-порталу по API.
        :return: Возвращает данные в формате JSON.
        """
        pass

    @abstractmethod
    def get_employer(self):
        """
        Получить информацию о работодателе с веб-портала по API.
        Полученные данные хранятся в экземпляре классе.
        :return:
        """
        pass

    @abstractmethod
    def get_vacancy(self):
        """
        Получить список вакансий с веб-портала по API.
        Полученные данные хранятся в экземпляре классе.
        :return:
        """
        pass


class JobSearchPortalAPI(API):
    """
    Класс описывающий работу API веб-порталов.
    Общие методы и свойства.
    Имеет предопределенный перечень свойств, закрытых для пользовательского использования.
    """
    __slots__ = ('__url_api', '__result_list', '__headers', '__params')

    def __init__(self, url_api: str, headers: dict, params: dict):
        """
        Метод инициализации экземпляров класса РаботаПоискаВебПорта из входящих данных.
        :param url_api: Ссылка на API.
        :param headers: Заголовок с передаваемыми на портал параметрами.
        :param params: Параметры запроса.
        """
        self.__url_api = url_api
        self.__headers = headers
        self.__params = params
        self.__result_list = []

    @property
    def url_api(self):
        return self.__url_api

    @property
    def headers(self):
        return self.__headers

    @property
    def params(self):
        return self.__params

    @property
    def result_list(self):
        return self.__result_list

    def __str__(self):
        """
        Переопределённое представление строкового значения экземпляра класса.
        :return: Строка с данными экземпляра класса.
        """
        return f'url_api = {self.__url_api}'

    def __repr__(self):
        """
        Служебное (внутренне) представление строкового значения экземпляра класса.
        :return: Строка с данными экземпляра класса.
        """
        return f"{self.__class__.__name__}('{self.__url_api}', '{self.__params}', '{self.__result_list}')"

    def get_requests(self):
        """
        Получить ответ на запрос к веб-порталу по API.
        :return: Возвращает данные в формате JSON.
        """

        # В запросе используем параметры, которые были получены при инициализации экземпляра класса
        response = requests.get(self.url_api, headers=self.headers, params=self.params)

        # Если ошибки отсутствуют возвращаем данные в формате JSON.
        # Иначе возвращаем Исключение с описанием ошибки.
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения данных по API. Код ошибки = {response.status_code}")

    def get_employer(self):
        """
        Получить информацию о работодателе с веб-портала по API.
        Полученные данные хранятся в экземпляре классе.
        :return:
        """
        self.__result_list = []

        # В обработчике исключений производим запрос через API к веб-порталу.
        # Если возникает Исключение обрабатываем.
        try:
            result_request = self.get_requests()
        except Exception as error:
            print(error)
        else:
            self.__result_list.append(result_request)

    def get_vacancy(self, pages_count=2):
        """
        Получить список вакансий с веб-портала по API.
        Полученные данные хранятся в экземпляре классе.
        :param pages_count: Количество запрашиваемых с веб-портала страниц.
        :return:
        """
        self.__result_list = []

        # В запросе направляемом по API указываем количество страниц, которое хотим получить в ответ.
        # Затем обходим каждую страницу.
        for page_number in range(pages_count):
            self.__params['page'] = page_number

            # В обработчике исключений производим запрос через API к веб-порталу.
            # Если возникает Исключение обрабатываем.
            try:
                vacancies_page = self.get_requests()['items']
            except Exception as error:
                print(error)
            else:
                self.__result_list.extend(vacancies_page)


class HeadHunterEmployerAPI(JobSearchPortalAPI):
    """
    Класс описывающий работу API веб-порталов HeadHunter, получение информации о Работодателе.
    """
    def __init__(self, employer_id: str):
        """
        Инициализация конкретными параметрами для работы API с веб-порталом HeadHunter.
        :param employer_id: Идентификатор работодателя по которому будет получена информация.
        """
        url_api = 'https://api.hh.ru/employers/' + employer_id
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {getenv("API_KEY_HH")}'
        }

        super().__init__(url_api, headers, {})


class HeadHunterVacancyAPI(JobSearchPortalAPI):
    """
    Класс описывающий работу API веб-порталов HeadHunter, получение информации о Вакансиях.
    """
    def __init__(self, employer_id: str, number_records: int = 4):
        """
        Инициализация конкретными параметрами для работы API с веб-порталом HeadHunter.
        :param number_records: Количество записей запрашиваемых с веб-портала.
        :param employer_id: Список идентификаторов работодателей, по которым происходит отбор.
        """
        url_api = 'https://api.hh.ru/vacancies'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {getenv("API_KEY_HH")}'
        }

        params = {
            'per_page': number_records,
            'page': 1,
            'only_with_salary': True,
            'currency': 'RUR',
            'employer_id': employer_id
        }
        super().__init__(url_api, headers, params)
