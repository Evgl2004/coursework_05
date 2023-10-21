import pytest
import uteils.func as func

import psycopg2


def test_read_config():
    assert func.read_config("database.ini")['user'] == "postgres"


def test_read_config_err():
    with pytest.raises(Exception):
        func.read_config("database.ini", "test")


def test_create_database():

    database_name = "test_db"
    params = func.read_config("database.ini")

    func.create_database(database_name, params)

    connection = psycopg2.connect(dbname='postgres', **params)
    connection.autocommit = True

    with pytest.raises(Exception):
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE {database_name}")

        if connection is not None:
            connection.close()


def test_create_tables():

    database_name = "test_db"
    params = func.read_config("database.ini")

    func.create_database(database_name, params)
    func.create_tables(database_name, params)

    connection = psycopg2.connect(dbname=database_name, **params)

    with pytest.raises(Exception):
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE vacancies (
                    id serial PRIMARY KEY
                );
            """)
            connection.commit()

        if connection is not None:
            connection.close()

    connection = psycopg2.connect(dbname=database_name, **params)

    with pytest.raises(Exception):
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE employers (
                    id serial PRIMARY KEY
                );
            """)
            connection.commit()

        if connection is not None:
            connection.close()


def test_save_data_to_database():

    database_name = "test_db"
    params = func.read_config("database.ini")

    func.create_database(database_name, params)
    func.create_tables(database_name, params)

    employer = [
        {'id': '123',
         'name': 'ООО "Супер предприятие"',
         'open_vacancies': 22,
         'site_url': 'https://my.emp.pro/',
         'trusted': True,
         'accredited_it_employer': True}
    ]

    vacancy = [
        {'id': '404',
         'name': 'Продавец',
         'snippet': {'responsibility': 'Вставать каждый день по утрам и ходить на работу'},
         'published_at': '2023-05-18',
         'alternate_url': 'https://hh.ru/vacancy/404',
         'salary': {'from': 25000, 'to': 30000},
         'archived': False},

        {'id': '405',
         'name': 'Продавец-консультант',
         'snippet': {'responsibility': 'Вставать не каждый день по утрам и ходить на работу'},
         'published_at': '2023-06-18',
         'alternate_url': 'https://hh.ru/vacancy/405',
         'salary': {'from': 35000, 'to': 40000},
         'archived': False}
    ]

    connection = psycopg2.connect(dbname=database_name, **params)

    with connection.cursor() as cursor:
        cursor.execute("""
            TRUNCATE TABLE vacancies, employers RESTART IDENTITY CASCADE
        """)
        connection.commit()

        if connection is not None:
            connection.close()

    func.save_data_to_database(employer, vacancy, database_name, params)

    connection = psycopg2.connect(dbname=database_name, **params)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                employers.name AS name, 
                employers.open_vacancies AS open_vacancies 
            FROM
                employers
        """)

        assert cursor.fetchall() == [('ООО "Супер предприятие"', 22)]

        if connection is not None:
            connection.close()