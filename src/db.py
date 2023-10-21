import psycopg2


class DBManager:
    """
    Класс для работы с базой данных и имеющий несколько методов с различными выборками.
    """
    __slots__ = ('__database_name', '__params')

    def __init__(self, database_name: str, params: dict):
        self.__database_name = database_name
        self.__params = params

    @property
    def database_name(self):
        return self.__database_name

    @property
    def params(self):
        return self.__params

    def __str__(self):
        """
        Переопределённое представление строкового значения экземпляра класса.
        :return: Строка с данными экземпляра класса.
        """
        return f'database_name = {self.__database_name}'

    def __repr__(self):
        """
        Служебное (внутренне) представление строкового значения экземпляра класса.
        :return: Строка с данными экземпляра класса.
        """
        return f"{self.__class__.__name__}('{self.__database_name}')"

    def __execute_request(self, text_request):
        """
        Метод выполняет запрос в СУБД для получения данных.
        :param request_text: Текс запроса.
        :return: Возвращает выборку детальных записей.
        """

        # первоначальное подключение к системе управления базами данных.
        connection = psycopg2.connect(dbname=self.__database_name, **self.__params)

        # помещаем подключение и работу с СУБД в исключение на случай возникновения не предвиденных ошибок.
        try:
            # инициализация курсора для написания запросов в СУБД.
            with connection.cursor() as cursor:
                cursor.execute(text_request)

                return cursor.fetchall()

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if connection is not None:
                connection.close()

    def get_companies_and_vacancies_count(self):
        """
        Метод возвращает список всех компаний и количество вакансий у каждой компании.
        :return: Возвращает выборку детальных записей.
        """

        text_request = """
            SELECT
                employers.name AS name, 
                employers.open_vacancies AS open_vacancies 
            FROM
                employers
        """
        return self.__execute_request(text_request)

    def get_all_vacancies(self):
        """
        Метод возвращает список всех вакансий с указанием названия компании, названия вакансии и зарплаты
        и ссылки на вакансию.
        :return: Возвращает выборку детальных записей.
        """

        text_request = """
            SELECT
                employers.name AS employers_name, 
                vacancies.name AS vacancies_name,
                vacancies.salary_from AS salary_from,
                vacancies.salary_to AS salary_to,
                vacancies.alternate_url AS alternate_url
            FROM
                vacancies
                    LEFT JOIN employers
                        ON vacancies.employer_id = employers.id
        """
        return self.__execute_request(text_request)

    def get_avg_salary(self):
        """
        Метод возвращает среднюю зарплату по вакансиям.
        :return: Возвращает выборку детальных записей.
        """

        text_request = """
            SELECT
                employers.name AS employers_name, 
                vacancies.name AS vacancies_name,
                (vacancies.salary_to + vacancies.salary_from)/2 AS avg_salary
            FROM
                vacancies
                    LEFT JOIN employers
                        ON vacancies.employer_id = employers.id
        """
        return self.__execute_request(text_request)

    def get_vacancies_with_higher_salary(self):
        """
        Метод возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: Возвращает выборку детальных записей.
        """

        text_request = """
            SELECT
                (AVG(vacancies.salary_to) + AVG(vacancies.salary_from))/2 AS avg_salary_all_vacancy
            FROM
                vacancies
        """
        avg_salary_all_vacancy = self.__execute_request(text_request)[0][0]

        text_request = f"""
            SELECT
                vacancies.name AS vacancies_name,
                (vacancies.salary_to + vacancies.salary_from)/2 AS avg_salary
            FROM
                vacancies
            WHERE
                (vacancies.salary_to + vacancies.salary_from)/2 >= {avg_salary_all_vacancy}
        """

        return self.__execute_request(text_request)

    def get_vacancies_with_keyword(self, key_word: str):
        """
        Метод возвращает все вакансии, в названии которых содержатся переданные в метод ключевого слова.
        :param key_word: Ключевое слово по которому будет производиться отбор.
        :return: Возвращает выборку детальных записей.
        """

        text_request = f"""
            SELECT
                vacancies.name AS vacancies_name
            FROM
                vacancies
            WHERE
                vacancies.name LIKE '%{key_word}%'
        """
        return self.__execute_request(text_request)