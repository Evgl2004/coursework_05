from uteils.func import read_config, create_database, create_tables, save_data_to_database
from src.api import HeadHunterEmployerAPI, HeadHunterVacancyAPI


def main():

    list_favorite_employer = [
        '1122462', '80', '15478', '3127', '193400',
        '4023', '22259', '87279', '544224', '900947'
    ]

    # считываем параметры подключения из файла с настройками *.ini
    params = read_config()

    # создаём базу данных
    create_database('vacancies', params)
    print("БД 'vacancies' успешно создана")

    # создаём таблицы для базы данных
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


if __name__ == "__main__":
    main()

