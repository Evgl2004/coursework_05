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

    # первоначальное подключение к системе управления базами данных.
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

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

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

    # первоначальное подключение к системе управления базами данных.
    connection = psycopg2.connect(dbname=database_name, **params)

    # помещаем подключение и работу с СУБД в исключение на случай возникновения не предвиденных ошибок.
    try:
        # инициализация курсора для написания запросов в СУБД.
        with connection.cursor() as cursor:
            # перед созданием новых таблиц удаляем таблицы, если они уже существует.
            cursor.execute("""
                DROP TABLE IF EXISTS vacancies;
                DROP TABLE IF EXISTS employers;
            """)
            connection.commit()

            # создаём таблицу "Работодатель" и соответствующие поля.
            cursor.execute("""
                CREATE TABLE employers (
                    id serial,
                    id_employer varchar(25),
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
                CREATE TABLE vacancies (
                    id serial,
                    id_vacancy varchar(25),
                    employer_id integer,
                    name varchar(100),
                    description text,
                    published_at date,
                    alternate_url varchar(100),
                    salary_from integer,
                    salary_to integer,
                    archived boolean,
                    
                    CONSTRAINT pk_vacancies_id PRIMARY KEY (id),
                    CONSTRAINT fk_vacancies_employers FOREIGN KEY(employer_id) REFERENCES employers(id)
                );
            """)
            connection.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()


def save_data_to_database(result_list_employer,
                          result_list_vacancy,
                          database_name: str,
                          params: dict) -> None:
    """
    Функция производит внесение данных полученных из запроса API с сайта вакансий, представленных в виде словарей
    класса в СУБД (запись).
    :param result_list_employer: Словарь с данными по Работодателю.
    :param result_list_vacancy: Словарь с данными по Вакансиям.
    :param database_name: Имя базы данных в которой будут производиться работы (выполняться запросы).
    :param params: Набор передаваемых параметров для подключения к СУБД.
    :return:
    """

    # первоначальное подключение к системе управления базами данных.
    connection = psycopg2.connect(dbname=database_name, **params)

    # помещаем подключение и работу с СУБД в исключение на случай возникновения не предвиденных ошибок.
    try:
        # инициализация курсора для написания запросов в СУБД.
        with connection.cursor() as cursor:
            # вносим запись в таблицу "Работодатель".
            cursor.execute("""
                INSERT INTO employers (
                    id_employer,
                    name,
                    open_vacancies,
                    site_url,
                    trusted,
                    accredited_it_employer                   
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (result_list_employer[0]['id'],
                 result_list_employer[0]['name'],
                 result_list_employer[0]['open_vacancies'],
                 result_list_employer[0]['site_url'],
                 result_list_employer[0]['trusted'],
                 result_list_employer[0]['accredited_it_employer'])
            )

            # после запроса получаем идентификатор добавленной записи, чтобы организовать связь с таблицей Вакансии.
            employer_id = cursor.fetchone()[0]

            # вносим запись в таблицу "Вакансии" обходя весь список с данными.
            for item in result_list_vacancy:
                cursor.execute("""
                    INSERT INTO vacancies (
                        id_vacancy,
                        employer_id,
                        name,
                        description,
                        published_at,
                        alternate_url,
                        salary_from,
                        salary_to,
                        archived
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """,
                    (item['id'],
                     employer_id,
                     item['name'],
                     item['snippet']['responsibility'],
                     item['published_at'],
                     item['alternate_url'],
                     item["salary"]['from'] if item["salary"] is not None and item["salary"]['from'] is not None else 0,
                     item["salary"]['to'] if item["salary"] is not None and item["salary"]['to'] is not None else 0,
                     item['archived'])
                )

            connection.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()
