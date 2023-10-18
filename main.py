from uteils.func import read_config, create_database, create_tables, save_data_to_database
from src.api import HeadHunterEmployerAPI, HeadHunterVacancyAPI
from src.db import DBManager


def main():

    # Список с кодами работодателей с сайта HH.ru
    list_favorite_employer = [
        '1122462', '80', '15478', '3127', '193400',
        '4023', '22259', '87279', '544224', '900947'
    ]

    # Считываем параметры подключения из файла с настройками *.ini
    params = read_config()

    # Создаём базу данных
    create_database('vacancies', params)
    print("БД 'vacancies' успешно создана")

    # Создаём таблицы для базы данных
    create_tables('vacancies', params)
    print("Таблицы успешно созданы")

    # Сохранение данных о Работодателе и Вакансиях в базу данных.
    # Обход списка идентификаторов работодателей, получение информации по API.
    for employer_id in list_favorite_employer:

        employer = HeadHunterEmployerAPI(employer_id)
        employer.get_employer()

        vacancy = HeadHunterVacancyAPI(employer_id)
        vacancy.get_vacancy()

        save_data_to_database(employer, vacancy, 'vacancies', params)

    print("Данные успешно записаны в БД")

    # Инициализация экземпляра класса для работы с базой данных и имеющий несколько методов с различными выборками.
    db_vacancies = DBManager('vacancies', params)

    input_data = ""

    # Основное меню выбора команд взаимодействия с полученными данными.
    # Цикл до тех пор, пока не будет введено ключевое слово выхода.
    while input_data.lower() != 'exit':

        input_data = input(
            "Выберите пункт:\n"
            "1 - Вывести список всех компаний и количество вакансий у каждой компании.\n"
            "2 - Вывести список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на"
            " вакансию.\n"
            "3 - Вывести среднюю зарплату по всем вакансиям.\n"
            "4 - Вывести список всех вакансий, у которых зарплата выше средней среди всех вакансий.\n"
            "5 - Вывести список всех вакансии, в названии которых содержится ключевое слово.\n"
            "exit - завершить работу.\n")

        if input_data == '1':
            # Обходим и выводим результаты выборки списка всех компаний и количество вакансий у каждой компании.
            for selection_detailed_records in db_vacancies.get_companies_and_vacancies_count():
                print(selection_detailed_records)

        elif input_data == '2':
            # Обходим и выводим результаты выборки список всех вакансий с указанием названия компании, названия вакансии
            # и зарплаты и ссылки на вакансию.
            for selection_detailed_records in db_vacancies.get_all_vacancies():
                print(selection_detailed_records)

        elif input_data == '3':
            # Обходим и выводим результаты выборки средней зарплаты по всем вакансиям.
            for selection_detailed_records in db_vacancies.get_avg_salary():
                print(selection_detailed_records)

        elif input_data == '4':
            # Обходим и выводим результаты выборки список всех вакансий, у которых зарплата выше средней среди
            # всех вакансий.
            for selection_detailed_records in db_vacancies.get_vacancies_with_higher_salary():
                print(selection_detailed_records)

        elif input_data == '5':

            input_key_word = input(
                "Укажите ключевое слово для поиска в названиях вакансий:\n")

            # Обходим и выводим результаты выборки всех вакансии, в названии которых содержится ключевое слово.
            for selection_detailed_records in db_vacancies.get_vacancies_with_keyword(input_key_word):
                print(selection_detailed_records)

        elif input_data != 'exit':
            print("Введите число от 1 до 5.")


if __name__ == "__main__":
    main()

