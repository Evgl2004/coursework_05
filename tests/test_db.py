import pytest
from src.db import DBManager
from uteils.func import read_config, create_database, create_tables, save_data_to_database


@pytest.fixture
def call_test_db():
    params = read_config("database.ini")
    # Создаём тестовую базу данных.
    create_database('test_db', params)

    # Создаём таблицы для базы данных.
    create_tables('test_db', params)

    # Создаём наборы данных о Работодателе и Вакансиях для базы данных.
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

    # Сохранение данных о Работодателе и Вакансиях в базу данных.
    save_data_to_database(employer, vacancy, 'test_db', params)


@pytest.fixture
def call_test_db_manager():
    return DBManager('test_db', read_config("database.ini"))


def test_db_manager_init(call_test_db, call_test_db_manager):
    assert call_test_db_manager.database_name == "test_db"
    assert call_test_db_manager.params['user'] == "postgres"


def test_db_manager_access_properties(call_test_db, call_test_db_manager):
    with pytest.raises(AttributeError):
        print(call_test_db_manager.__database_name)

    with pytest.raises(AttributeError):
        print(call_test_db_manager.__params)


def test_db_manager_property_setting(call_test_db, call_test_db_manager):
    with pytest.raises(AttributeError):
        call_test_db_manager.database_name = "test"

    with pytest.raises(AttributeError):
        call_test_db_manager.params = "test"


def test_db_manager_str(call_test_db, call_test_db_manager):
    assert str(call_test_db_manager) == "database_name = test_db"


def test_db_manager_repr(call_test_db, call_test_db_manager):
    assert call_test_db_manager.__repr__() == "DBManager('test_db')"


def test_db_manager_get_companies_and_vacancies_count(call_test_db, call_test_db_manager):
    assert call_test_db_manager.get_companies_and_vacancies_count() == [('ООО "Супер предприятие"', 22)]


def test_db_manager_get_all_vacancies(call_test_db, call_test_db_manager):
    result = [
        ('ООО "Супер предприятие"',
         'Продавец',
         25000,
         30000,
         'https://hh.ru/vacancy/404'),

        ('ООО "Супер предприятие"',
         'Продавец-консультант',
         35000,
         40000,
         'https://hh.ru/vacancy/405')
    ]
    assert call_test_db_manager.get_all_vacancies() == result


def test_db_manager_get_avg_salary(call_test_db, call_test_db_manager):
    assert call_test_db_manager.get_avg_salary() == [('ООО "Супер предприятие"', 'Продавец', 27500),
                                                     ('ООО "Супер предприятие"', 'Продавец-консультант', 37500)]


def test_db_manager_get_vacancies_with_higher_salary(call_test_db, call_test_db_manager):
    assert call_test_db_manager.get_vacancies_with_higher_salary() == [('Продавец-консультант', 37500)]


def test_db_manager_get_vacancies_with_keyword(call_test_db, call_test_db_manager):
    assert call_test_db_manager.get_vacancies_with_keyword('Продавец') == [('Продавец',), ('Продавец-консультант',)]
