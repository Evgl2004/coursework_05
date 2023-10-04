from uteils.func import read_config, create_database, create_tables


def main():

    # считываем параметры подключения из файла с настройками *.ini
    params = read_config()

    # создаём базу данных
    create_database('vacancies', params)
    print("БД 'vacancies' успешно создана")

    # создаём таблицы для базы данных
    create_tables('vacancies', params)
    print("Таблицы успешно созданы")


if __name__ == "__main__":
    main()

