import csv
from tkinter import messagebox
from db_connection import connect_db


def generate_department_report():
    # Подключение к базе данных
    conn = connect_db()
    cursor = conn.cursor()

    # Запрос для получения данных о сотрудниках, их отделах и должностях
    query = """
        SELECT 
            Сотрудник.Имя_сотрудника,
            Отдел.Название_отдела,
            Должности.Должность,
            Должности.Оклад
        FROM Сотрудник
        LEFT JOIN Отдел ON Сотрудник.id_отдела = Отдел.id_отдела
        LEFT JOIN Должности ON Сотрудник.id_должности = Должности.id_должности
    """
    cursor.execute(query)
    employees = cursor.fetchall()
    conn.close()

    # Создание CSV файла
    file_name = "department_report.csv"
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ФИО", "Отдел", "Должность", "Оклад"])

        # Заполнение данных о сотрудниках
        for employee in employees:
            writer.writerow(employee)

    # Показ сообщения об успешном создании отчета
    messagebox.showinfo("Успех", f"Отчет по отделам успешно создан и сохранен в файл {file_name}")
