# Курсовой проект по БД 

## Задание
В рамках проекта вам необходимо получить данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.

## Основные шаги проекта 

1. Получить данные о работодателях и их вакансиях с сайта hh.ru. Для этого используйте публичный API hh.ru и библиотеку 
requests.
2. Выбрать не менее 10 интересных вам компаний, от которых вы будете получать данные о вакансиях по API.
3. Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях. Для работы с БД используйте библиотеку 
psycopg2.
4. Реализовать код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
5. Создать класс DBManager, который будет подключаться к БД PostgreSQL .

## Класс DBManager
Имеет следующие методы:

- get_companies_and_vacancies_count() — получает список всех компаний и количество вакансий у каждой компании.
- get_all_vacancies() — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
- get_avg_salary() — получает среднюю зарплату по вакансиям.
- get_vacancies_with_higher_salary() — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
- get_vacancies_with_keyword() — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.