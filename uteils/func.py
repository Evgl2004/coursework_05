from configparser import ConfigParser
import psycopg2


def read_config(filename: str = "database.ini", section: str = "postgresql") -> dict:
    """
    Функция для считывая настроек подключения к СУБД Postgres.
    :param filename: Имя файла с настройками.
    :param section: Наименование секции-блока с настройками подключения в файле настроек.
    :return: Словарь с настойками подключения.
    """
    # Инициализация инструмента для разбора файла настроек.
    parser = ConfigParser()
    # Чтение указанного файла
    parser.read(filename)
    return_dict = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            return_dict[param[0]] = param[1]
    else:
        raise Exception(
            'Секция-блок {0} не найденная в {1} файле.'.format(section, filename))
    return return_dict


def create_database(database_name: str, params: dict) -> None:
    """
    Первоначальное создание базы данных и таблиц для заполнения информации вакансиями.
    :param database_name: Имя базы данных, которая будет создана.
    :param params: Набор передаваемых параметров для подключения к СУБД.
    :return:
    """

    # первоначальное подключение к СУДБ к системной базе данных.
    connection = psycopg2.connect(dbname='postgres', **params)
    # выставляем параметр автоматически фиксировать транзакции после выполнения каждого запроса к СУБД.
    connection.autocommit = True

    # помещаем подключение и работу с СУБД в исключение на случай возникновения не предвиденных ошибок.
    try:
        # инициализация курсора для написания запросов в СУБД.
        with connection.cursor() as cursor:
            # перед созданием новой базы данных удаляем базу данных если она уже существует.
            cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")

            # создаём новую базу данных.
            cursor.execute(f"CREATE DATABASE {database_name}")
    finally:
        if connection is not None:
            connection.close()


def create_tables(database_name: str, params: dict) -> None:
    """
    Первоначальное создание-инициализация таблиц, полей, связей базы данных.
    :param database_name: Имя базы данных в которой будут производиться работы (выполняться запросы).
    :param params: Набор передаваемых параметров для подключения к СУБД.
    :return:
    """

    # первоначальное подключение к СУДБ к системной базе данных.
    connection = psycopg2.connect(dbname=database_name, **params)

    # помещаем подключение и работу с СУБД в исключение на случай возникновения не предвиденных ошибок.
    try:
        # инициализация курсора для написания запросов в СУБД.
        with connection.cursor() as cursor:
            # создаём таблицу "Работодатель" и соответствующие поля.
            cursor.execute("""
                CREATE TABLE employer (
                    id varchar(25),
                    name varchar(100),
                    open_vacancies integer,
                    site_url varchar(100),
                    trusted boolean,
                    accredited_it_employer boolean,
                    
                    CONSTRAINT pk_employer_id PRIMARY KEY (id)                    
                );
            """)

            # создаём таблицу "Вакансии" и соответствующие поля.
            cursor.execute("""
                CREATE TABLE vacancy (
                    id varchar(25),
                    employer_id varchar(25),
                    name varchar(100),
                    description text,
                    published_at date,
                    alternate_url varchar(100),
                    salary_from integer,
                    salary_to integer,
                    archived boolean,
                    
                    CONSTRAINT pk_vacancy_id PRIMARY KEY (id),
                    CONSTRAINT fk_vacancy_employer FOREIGN KEY(employer_id) REFERENCES employer(id)
                );
            """)
            connection.commit()
    finally:
        if connection is not None:
            connection.close()