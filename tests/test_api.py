import pytest
from os import getenv
from src.api import JobSearchPortalAPI, HeadHunterEmployerAPI, HeadHunterVacancyAPI


@pytest.fixture
def call_test_portal_api():
    url_api = 'https://api.hh.ru/employers/80'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {getenv("API_KEY_HH")}'
    }

    return JobSearchPortalAPI(url_api, headers, {})


def test_portal_api_init(call_test_portal_api):
    assert call_test_portal_api.url_api == "https://api.hh.ru/employers/80"
    assert call_test_portal_api.result_list == []


def test_portal_api_access_properties(call_test_portal_api):
    with pytest.raises(AttributeError):
        print(call_test_portal_api.__url_api)

    with pytest.raises(AttributeError):
        print(call_test_portal_api.__headers)

    with pytest.raises(AttributeError):
        print(call_test_portal_api.__params)

    with pytest.raises(AttributeError):
        print(call_test_portal_api.__result_list)


def test_portal_api_property_setting(call_test_portal_api):
    with pytest.raises(AttributeError):
        call_test_portal_api.url_api = "test"

    with pytest.raises(AttributeError):
        call_test_portal_api.headers = "test"

    with pytest.raises(AttributeError):
        call_test_portal_api.params = "test"

    with pytest.raises(AttributeError):
        call_test_portal_api.result_list = "test"


def test_portal_api_str(call_test_portal_api):
    assert str(call_test_portal_api) == "url_api = https://api.hh.ru/employers/80"


def test_portal_api_repr(call_test_portal_api):
    assert call_test_portal_api.__repr__() == "JobSearchPortalAPI('https://api.hh.ru/employers/80', '{}', '[]')"


def test_portal_api_get_requests(call_test_portal_api):
    answer = call_test_portal_api.get_requests()

    assert isinstance(answer, dict)
    assert len(answer) == 17
    assert 'id' in answer
    assert isinstance(answer['id'], str)


def test_portal_api_get_employer(call_test_portal_api):
    call_test_portal_api.get_employer()

    answer_get_employer = call_test_portal_api.result_list

    assert isinstance(answer_get_employer, list)
    assert len(answer_get_employer) == 1
    assert isinstance(answer_get_employer[0], dict)
    assert 'id' in answer_get_employer[0]
    assert isinstance(answer_get_employer[0]['id'], str)


def test_portal_api_get_employer_err(call_test_portal_api):
    url_employers = 'https://api.hh.ru/employers/0'
    test_portal_api = JobSearchPortalAPI(url_employers, {}, {'salary': 'qwe'})

    assert (test_portal_api.get_employer()) == print("Ошибка получения данных по API. Код ошибки = 404")


def test_portal_api_get_vacancy(call_test_portal_api):

    url_vacancies = 'https://api.hh.ru/vacancies'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {getenv("API_KEY_HH")}'
    }
    params = {
        'per_page': 4,
        'page': 1,
        'only_with_salary': True,
        'currency': 'RUR',
        'employer_id': '80'
    }
    test_portal_api = JobSearchPortalAPI(url_vacancies, headers, params)

    test_portal_api.get_vacancy()

    answer_get_vacancy = test_portal_api.result_list

    assert isinstance(answer_get_vacancy, list)
    assert len(answer_get_vacancy) == 8
    assert isinstance(answer_get_vacancy[0], dict)
    assert 'id' in answer_get_vacancy[0]
    assert isinstance(answer_get_vacancy[0]['id'], str)


def test_portal_api_get_vacancies_err(call_test_portal_api):
    url_vacancies = 'https://api.hh.ru/vacancies'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {getenv("API_KEY_HH")}'
    }
    params = {
        'per_page': 4,
        'page': 1,
        'only_with_salary': True,
        'currency': 'RUR',
        'employer_id': 'test'
    }

    test_portal_api = JobSearchPortalAPI(url_vacancies, headers, params)

    assert (test_portal_api.get_vacancy()) == print("Ошибка получения данных по API. Код ошибки = 400")


def test_hh_api_employer_init():
    hh_api = HeadHunterEmployerAPI("80")
    assert hh_api.url_api == "https://api.hh.ru/employers/80"
    assert hh_api.params == {}
    assert hh_api.result_list == []


def test_hh_api_vacancy_init():
    hh_api = HeadHunterVacancyAPI("80")
    assert hh_api.url_api == "https://api.hh.ru/vacancies"
    assert hh_api.params["employer_id"] == "80"
    assert hh_api.result_list == []