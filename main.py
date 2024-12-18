import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from department_report import generate_department_report
from db_connection import connect_db


# Функция для выполнения SQL запроса
def execute_query(query, params=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


# Функция для получения данных из таблицы "Договор"
def fetch_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Договор")
    rows = cursor.fetchall()
    conn.close()
    return rows


# Функция для добавления нового договора
def add_contract():
    def save_contract():
        contract_id = entry_contract_id.get()
        insurer_id = entry_insurer_id.get()
        date = entry_date.get()
        premium = entry_premium.get()
        employee_id = entry_employee_id.get()

        query = """
        INSERT INTO Договор (id_договора, id_страхователя, Дата_заключения, Сумма_страховой_премии, id_сотрудника)
        VALUES (?, ?, ?, ?, ?)
        """
        execute_query(query, (contract_id, insurer_id, date, premium, employee_id))
        messagebox.showinfo("Успех", "Договор добавлен!")
        window_add_contract.destroy()
        show_datas()  # Обновить таблицу

    # Окно для ввода данных договора
    window_add_contract = tk.Toplevel(root)
    window_add_contract.title("Добавить договор")

    tk.Label(window_add_contract, text="ID договора").grid(row=0, column=0)
    tk.Label(window_add_contract, text="ID страхователя").grid(row=1, column=0)
    tk.Label(window_add_contract, text="Дата заключения").grid(row=2, column=0)
    tk.Label(window_add_contract, text="Сумма страховой премии").grid(row=3, column=0)
    tk.Label(window_add_contract, text="ID сотрудника").grid(row=4, column=0)

    entry_contract_id = tk.Entry(window_add_contract)
    entry_insurer_id = tk.Entry(window_add_contract)
    entry_date = tk.Entry(window_add_contract)
    entry_premium = tk.Entry(window_add_contract)
    entry_employee_id = tk.Entry(window_add_contract)

    entry_contract_id.grid(row=0, column=1)
    entry_insurer_id.grid(row=1, column=1)
    entry_date.grid(row=2, column=1)
    entry_premium.grid(row=3, column=1)
    entry_employee_id.grid(row=4, column=1)

    tk.Button(window_add_contract, text="Сохранить", command=save_contract).grid(row=5, column=1)


# Функция для обновления договора
def update_contract():
    def save_updated_contract():
        contract_id = entry_contract_id.get()
        insurer_id = entry_insurer_id.get()
        date = entry_date.get()
        premium = entry_premium.get()
        employee_id = entry_employee_id.get()

        query = """
        UPDATE Договор 
        SET id_страхователя = ?, Дата_заключения = ?, Сумма_страховой_премии = ?, id_сотрудника = ?
        WHERE id_договора = ?
        """
        execute_query(query, (insurer_id, date, premium, employee_id, contract_id))
        messagebox.showinfo("Успех", "Договор обновлен!")
        window_update_contract.destroy()
        show_datas()  # Обновить таблицу

    # Окно для обновления договора
    window_update_contract = tk.Toplevel(root)
    window_update_contract.title("Обновить договор")

    tk.Label(window_update_contract, text="ID договора").grid(row=0, column=0)
    tk.Label(window_update_contract, text="ID страхователя").grid(row=1, column=0)
    tk.Label(window_update_contract, text="Дата заключения").grid(row=2, column=0)
    tk.Label(window_update_contract, text="Сумма страховой премии").grid(row=3, column=0)
    tk.Label(window_update_contract, text="ID сотрудника").grid(row=4, column=0)

    entry_contract_id = tk.Entry(window_update_contract)
    entry_insurer_id = tk.Entry(window_update_contract)
    entry_date = tk.Entry(window_update_contract)
    entry_premium = tk.Entry(window_update_contract)
    entry_employee_id = tk.Entry(window_update_contract)

    entry_contract_id.grid(row=0, column=1)
    entry_insurer_id.grid(row=1, column=1)
    entry_date.grid(row=2, column=1)
    entry_premium.grid(row=3, column=1)
    entry_employee_id.grid(row=4, column=1)

    tk.Button(window_update_contract, text="Обновить", command=save_updated_contract).grid(row=5, column=1)


# Функция для отображения данных в таблице
def show_data(order_by="id_договора", ascending=True):
    rows = fetch_data(order_by=order_by, ascending=ascending)
    # Очистка таблицы перед загрузкой новых данных
    for row in treeview.get_children():
        treeview.delete(row)
    for row in rows:
        treeview.insert("", "end", values=row)


# Функция для удаления договора
def delete_contract():
    selected_contract = treeview.selection()
    if selected_contract:
        contract_id = treeview.item(selected_contract)['values'][0]
        query = "DELETE FROM Договор WHERE id_договора = ?"
        execute_query(query, (contract_id,))
        messagebox.showinfo("Успех", "Договор удален!")
        show_datas()  # Обновить таблицу
    else:
        messagebox.showwarning("Предупреждение", "Выберите договор для удаления")


from tkinter import ttk


def center_window(window, width=400, height=300):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (width / 2))
    y_cordinate = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x_cordinate}+{y_cordinate}")


def styled_label(parent, text, row, col, **kwargs):
    label = ttk.Label(parent, text=text, anchor="w", font=("Arial", 12), **kwargs)
    label.grid(row=row, column=col, padx=10, pady=5, sticky="w")
    return label


def update_insurer_details(insurer_id, name, contact, address):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Страхователь
        SET Имя_страхователя = ?, Контактные_данные = ?, Адрес = ?
        WHERE id_страхователя = ?
    """, (name, contact, address, insurer_id))
    conn.commit()
    conn.close()
    tk.messagebox.showinfo("Успех", "Информация о страхователе успешно обновлена.")


def view_insurer_details(insurer_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Имя_страхователя, Контактные_данные, Адрес FROM Страхователь WHERE id_страхователя = ?",
                   (insurer_id,))
    insurer = cursor.fetchone()
    conn.close()

    def open_edit_window():
        edit_window = tk.Toplevel(details_window)
        edit_window.title(f"Изменить данные страхователя {insurer_id}")
        center_window(edit_window, width=400, height=300)

        ttk.Label(edit_window, text="Имя:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        name_entry.insert(0, insurer[0])

        ttk.Label(edit_window, text="Контактные данные:").grid(row=1, column=0, padx=10, pady=5)
        contact_entry = ttk.Entry(edit_window)
        contact_entry.grid(row=1, column=1, padx=10, pady=5)
        contact_entry.insert(0, insurer[1])

        ttk.Label(edit_window, text="Адрес:").grid(row=2, column=0, padx=10, pady=5)
        address_entry = ttk.Entry(edit_window)
        address_entry.grid(row=2, column=1, padx=10, pady=5)
        address_entry.insert(0, insurer[2])

        def save_changes():
            update_insurer_details(insurer_id, name_entry.get(), contact_entry.get(), address_entry.get())
            edit_window.destroy()
            details_window.destroy()

        ttk.Button(edit_window, text="Сохранить", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

    details_window = tk.Toplevel(root)
    details_window.title(f"Детали страхователя {insurer_id}")
    center_window(details_window, width=500, height=250)

    frame = ttk.Frame(details_window, padding=20)
    frame.pack(fill="both", expand=True)

    if insurer:
        styled_label(frame, f"Имя страхователя: {insurer[0]}", 0, 0)
        styled_label(frame, f"Контактные данные: {insurer[1]}", 1, 0)
        styled_label(frame, f"Адрес: {insurer[2]}", 2, 0)
        ttk.Button(frame, text="Изменить", command=open_edit_window).grid(row=3, column=0, pady=10, sticky="w")
    else:
        ttk.Label(frame, text="Страхователь не найден.", font=("Arial", 12, "italic")).grid(row=0, column=0)


def update_employee_details(employee_id, name, dept_id, position_id, salary):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        UPDATE Сотрудник
        SET Имя_сотрудника = ?, id_отдела = ?, id_должности = ?
        WHERE id_сотрудника = ?
    """
    cursor.execute(query, (name, dept_id, position_id, employee_id))

    # Обновление оклада в таблице Должности
    salary_query = """
        UPDATE Должности
        SET Оклад = ?
        WHERE id_должности = (SELECT id_должности FROM Сотрудник WHERE id_сотрудника = ?)
    """
    cursor.execute(salary_query, (salary, employee_id))

    conn.commit()
    conn.close()


def view_employee_details(employee_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Обновленный запрос с учетом оклада
    query = """
        SELECT 
            Сотрудник.Имя_сотрудника, 
            Отдел.id_отдела,
            Отдел.Название_отдела, 
            Должности.id_должности,
            Должности.Должность,
            Должности.Оклад  -- Добавляем оклад
        FROM Сотрудник
        LEFT JOIN Отдел ON Сотрудник.id_отдела = Отдел.id_отдела
        LEFT JOIN Должности ON Сотрудник.id_должности = Должности.id_должности
        WHERE Сотрудник.id_сотрудника = ?
    """
    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()
    conn.close()

    def open_edit_window():
        edit_window = tk.Toplevel(details_window)
        edit_window.title(f"Изменить данные сотрудника {employee_id}")
        center_window(edit_window, width=400, height=350)  # Увеличиваем размер окна

        ttk.Label(edit_window, text="Имя:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        name_entry.insert(0, employee[0])

        ttk.Label(edit_window, text="ID отдела:").grid(row=1, column=0, padx=10, pady=5)
        dept_entry = ttk.Entry(edit_window)
        dept_entry.grid(row=1, column=1, padx=10, pady=5)
        dept_entry.insert(0, employee[1])

        ttk.Label(edit_window, text="ID должности:").grid(row=2, column=0, padx=10, pady=5)
        position_entry = ttk.Entry(edit_window)
        position_entry.grid(row=2, column=1, padx=10, pady=5)
        position_entry.insert(0, employee[3])

        ttk.Label(edit_window, text="Оклад:").grid(row=3, column=0, padx=10, pady=5)
        salary_entry = ttk.Entry(edit_window)
        salary_entry.grid(row=3, column=1, padx=10, pady=5)
        salary_entry.insert(0, employee[5])  # Отображаем оклад

        def save_changes():
            update_employee_details(employee_id, name_entry.get(), dept_entry.get(), position_entry.get(),
                                    salary_entry.get())
            edit_window.destroy()
            details_window.destroy()

        ttk.Button(edit_window, text="Сохранить", command=save_changes).grid(row=4, column=0, columnspan=2, pady=10)

    details_window = tk.Toplevel(root)
    details_window.title(f"Детали сотрудника {employee_id}")
    center_window(details_window, width=500, height=350)  # Увеличиваем размер окна

    frame = ttk.Frame(details_window, padding=20)
    frame.pack(fill="both", expand=True)

    if employee:
        styled_label(frame, f"Имя сотрудника: {employee[0]}", 0, 0)
        styled_label(frame, f"Название отдела: {employee[2]}", 1, 0)
        styled_label(frame, f"Должность: {employee[4]}", 2, 0)
        styled_label(frame, f"Оклад: {employee[5]:.2f} руб.", 3, 0)  # Добавляем отображение оклада
        ttk.Button(frame, text="Изменить", command=open_edit_window).grid(row=4, column=0, pady=10, sticky="w")
    else:
        ttk.Label(frame, text="Сотрудник не найден.", font=("Arial", 12, "italic")).grid(row=0, column=0)


def view_contract_details(event):
    selected_contract = treeview.selection()
    if selected_contract:
        contract_id = treeview.item(selected_contract)['values'][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Договор WHERE id_договора = ?", (contract_id,))
        contract = cursor.fetchone()
        conn.close()

        details_window = tk.Toplevel(root)
        details_window.title(f"Детали договора {contract[0]}")
        center_window(details_window, width=600, height=400)

        frame = ttk.Frame(details_window, padding=20)
        frame.pack(fill="both", expand=True)

        if contract:
            styled_label(frame, f"ID Договора: {contract[0]}", 0, 0)
            tk.Button(frame, text=f"ID Страхователя: {contract[1]}",
                      command=lambda: view_insurer_details(contract[1])).grid(row=1, column=0, padx=10, pady=5,
                                                                              sticky="w")
            styled_label(frame, f"Дата заключения: {contract[2]}", 2, 0)
            styled_label(frame, f"Сумма страховой премии: {contract[3]}", 3, 0)
            tk.Button(frame, text=f"ID Сотрудника: {contract[6]}",
                      command=lambda: view_employee_details(contract[6])).grid(row=4, column=0, padx=10, pady=5,
                                                                               sticky="w")


import csv


# Функция для создания отчета по сотруднику (с учетом только сотрудников с договорами)
def generate_employee_report():
    # Окно для выбора сотрудника
    report_window = tk.Toplevel(root)
    report_window.title("Отчет по сотруднику")
    report_window.geometry("400x200")

    tk.Label(report_window, text="Выберите сотрудника:", font=("Arial", 12)).pack(pady=10)

    # Выпадающий список с ФИО сотрудников, у которых есть заключенные договоры
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        SELECT DISTINCT 
            Сотрудник.id_сотрудника, 
            Сотрудник.Имя_сотрудника
        FROM Договор
        INNER JOIN Сотрудник ON Договор.id_сотрудника = Сотрудник.id_сотрудника
    """
    cursor.execute(query)
    employees = cursor.fetchall()
    conn.close()

    if not employees:
        tk.messagebox.showinfo("Информация", "Нет сотрудников с заключенными договорами.")
        report_window.destroy()
        return

    employee_var = tk.StringVar()
    employee_dropdown = ttk.Combobox(report_window, textvariable=employee_var, state="readonly", width=30)
    employee_dropdown['values'] = [f"{emp[1]} (ID: {emp[0]})" for emp in employees]
    employee_dropdown.pack(pady=10)

    # Функция для генерации CSV отчета
    def create_report():
        selected = employee_var.get()
        if not selected:
            tk.messagebox.showwarning("Ошибка", "Выберите сотрудника из списка!")
            return

        employee_id = int(selected.split("ID: ")[1][:-1])  # Извлечение ID сотрудника
        employee_name = selected.split(" (")[0]  # Имя сотрудника

        # Запрос на выборку данных о договорах, заключенных сотрудником
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            SELECT 
                Договор.id_договора,
                Страхователь.Имя_страхователя,
                Договор.Дата_заключения,
                Договор.Сумма_страховой_премии
            FROM Договор
            LEFT JOIN Страхователь ON Договор.id_страхователя = Страхователь.id_страхователя
            WHERE Договор.id_сотрудника = ?
        """
        cursor.execute(query, (employee_id,))
        contracts = cursor.fetchall()
        conn.close()

        # Проверка, есть ли данные для отчета
        if not contracts:
            tk.messagebox.showinfo("Информация", f"У сотрудника {employee_name} нет заключенных договоров.")
            return

        # Генерация CSV файла
        filename = f"{employee_name}_отчет.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID договора", "Имя страхователя", "Дата заключения", "Сумма премии"])
            writer.writerows(contracts)

        tk.messagebox.showinfo("Успех", f"Отчет сохранен как {filename}")

    # Кнопка для генерации отчета
    tk.Button(report_window, text="Сгенерировать", command=create_report, font=("Arial", 12), bg="lightblue").pack(
        pady=20)


# Функция для отображения статистики и графика
def show_statistics():
    # Окно для отображения статистики
    stats_window = tk.Toplevel(root)
    stats_window.title("Статистика по договорам")
    stats_window.geometry("800x600")

    # Подключение к базе данных
    conn = connect_db()
    cursor = conn.cursor()

    # Запросы для статистики
    cursor.execute("SELECT COUNT(*) FROM Договор")
    total_contracts = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(Сумма_страховой_премии) FROM Договор")
    total_premium = cursor.fetchone()[0]

    cursor.execute("""
        SELECT strftime('%Y-%m', Дата_заключения) AS month, COUNT(*) 
        FROM Договор 
        GROUP BY month 
        ORDER BY month
    """)
    contracts_by_month = cursor.fetchall()
    conn.close()

    # Показать общее количество договоров
    tk.Label(stats_window, text=f"Общее количество договоров: {total_contracts}", font=("Arial", 12)).pack(pady=10)

    # Показать общую сумму страховых премий
    total_premium_display = total_premium if total_premium else 0
    tk.Label(stats_window, text=f"Общая сумма страховых премий: {total_premium_display:.2f} руб.",
             font=("Arial", 12)).pack(pady=10)

    # Построение графика
    if contracts_by_month:
        months = [row[0] for row in contracts_by_month]
        counts = [row[1] for row in contracts_by_month]

        # Преобразуем даты в месяц и год
        months = [mdates.datestr2num(month + '-01') for month in months]

        # Построение графика с использованием Matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))

        # Используем plot вместо plot_date
        ax.plot(months, counts, marker='o', linestyle='-', color='blue')

        # Форматирование оси X для отображения месяцев
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.set_title("Количество заключенных договоров по месяцам")
        ax.set_xlabel("Месяц")
        ax.set_ylabel("Количество договоров")
        ax.grid()

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # Встраивание графика в окно
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    else:
        tk.Label(stats_window, text="Нет данных для отображения графика.", font=("Arial", 12)).pack(pady=20)


# Основное окно
root = tk.Tk()
root.title("Автоматизированная система учета договоров страхования")
root.geometry("1100x600")  # Увеличим размер окна для удобства

# Кнопки для выполнения операций
tk.Button(root, text="Добавить договор", command=add_contract).pack(pady=10)
tk.Button(root, text="Обновить договор", command=update_contract).pack(pady=10)
tk.Button(root, text="Удалить договор", command=delete_contract).pack(pady=10)
tk.Button(root, text="Отчет по сотруднику", command=generate_employee_report).pack(pady=10)
tk.Button(root, text="Статистика по договорам", command=show_statistics).pack(pady=10)
# Кнопка "Статистика по отделам"
tk.Button(root, text="Статистика по отделам", command=generate_department_report).pack(pady=10)


# Функция выборки данных с ФИО сотрудника
def fetch_data():
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        SELECT 
            Договор.id_договора,
            Страхователь.Имя_страхователя,
            Договор.Дата_заключения,
            Договор.Сумма_страховой_премии,
            Сотрудник.Имя_сотрудника
        FROM Договор
        LEFT JOIN Страхователь ON Договор.id_страхователя = Страхователь.id_страхователя
        LEFT JOIN Сотрудник ON Договор.id_сотрудника = Сотрудник.id_сотрудника
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


# Отображение данных о договорах
def show_datas():
    rows = fetch_data()
    # Очистка таблицы перед загрузкой новых данных
    for row in treeview.get_children():
        treeview.delete(row)
    for row in rows:
        treeview.insert("", "end", values=row)


tk.Button(root, text="Показать все договора", command=show_datas).pack(pady=10)

# Таблица для отображения данных о договорах
columns = ("ID договора", "Имя страхователя", "Дата заключения", "Сумма премии", "ФИО сотрудника")
treeview = ttk.Treeview(root, columns=columns, show="headings", height=20)
treeview.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Настройка столбцов таблицы
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, anchor=tk.W)

# Обработчик клика по строке для отображения деталей договора
treeview.bind("<Double-1>", view_contract_details)

# Запуск главного окна
root.mainloop()
