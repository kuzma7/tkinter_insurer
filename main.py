import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# Подключение к базе данных SQLite
def connect_db():
    conn = sqlite3.connect('data_base.db')  # Имя базы данных
    return conn


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
        show_data()  # Обновить таблицу

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
        show_data()  # Обновить таблицу

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
        show_data()  # Обновить таблицу
    else:
        messagebox.showwarning("Предупреждение", "Выберите договор для удаления")


# Функция для отображения информации о страхователе
def view_insurer_details(insurer_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Имя_страхователя, Контактные_данные, Адрес FROM Страхователь WHERE id_страхователя = ?", (insurer_id,))
    insurer = cursor.fetchone()
    conn.close()

    if insurer:
        details_window = tk.Toplevel(root)
        details_window.title(f"Детали страхователя {insurer_id}")
        tk.Label(details_window, text=f"Имя страхователя: {insurer[0]}").grid(row=0, column=0)
        tk.Label(details_window, text=f"Контактные данные: {insurer[1]}").grid(row=1, column=0)
        tk.Label(details_window, text=f"Адрес: {insurer[2]}").grid(row=2, column=0)
    else:
        messagebox.showerror("Ошибка", "Страхователь не найден.")

# Функция для отображения информации о сотруднике
def view_employee_details(employee_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        SELECT 
            Сотрудник.Имя_сотрудника, 
            Отдел.Название_отдела, 
            Должности.Должность
        FROM Сотрудник
        LEFT JOIN Отдел ON Сотрудник.id_отдела = Отдел.id_отдела
        LEFT JOIN Должности ON Сотрудник.id_должности = Должности.id_должности
        WHERE Сотрудник.id_сотрудника = ?
    """
    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()
    conn.close()

    if employee:
        details_window = tk.Toplevel(root)
        details_window.title(f"Детали сотрудника {employee_id}")
        tk.Label(details_window, text=f"Имя сотрудника: {employee[0]}").grid(row=0, column=0)
        tk.Label(details_window, text=f"Название отдела: {employee[1]}").grid(row=1, column=0)
        tk.Label(details_window, text=f"Должность: {employee[2]}").grid(row=2, column=0)
    else:
        messagebox.showerror("Ошибка", "Сотрудник не найден.")

# Обновленная функция для отображения деталей договора
def view_contract_details(event):
    selected_contract = treeview.selection()
    if selected_contract:
        contract_id = treeview.item(selected_contract)['values'][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Договор WHERE id_договора = ?", (contract_id,))
        contract = cursor.fetchone()
        conn.close()

        if contract:
            details_window = tk.Toplevel(root)
            details_window.title(f"Детали договора {contract[0]}")

            tk.Label(details_window, text=f"ID Договора: {contract[0]}").grid(row=0, column=0)
            tk.Button(details_window, text=f"ID Страхователя: {contract[1]}",
                      command=lambda: view_insurer_details(contract[1])).grid(row=1, column=0)
            tk.Label(details_window, text=f"Дата заключения: {contract[2]}").grid(row=2, column=0)
            tk.Label(details_window, text=f"Сумма страховой премии: {contract[3]}").grid(row=3, column=0)
            tk.Button(details_window, text=f"ID Сотрудника: {contract[6]}",
                      command=lambda: view_employee_details(contract[6])).grid(row=4, column=0)



# Основное окно
root = tk.Tk()
root.title("Автоматизированная система учета договоров страхования")

# Кнопки для выполнения операций
tk.Button(root, text="Добавить договор", command=add_contract).pack(pady=10)
tk.Button(root, text="Обновить договор", command=update_contract).pack(pady=10)
tk.Button(root, text="Удалить договор", command=delete_contract).pack(pady=10)


# Отображение данных о договорах
def show_data():
    rows = fetch_data()
    # Очистка таблицы перед загрузкой новых данных
    for row in treeview.get_children():
        treeview.delete(row)
    for row in rows:
        treeview.insert("", "end", values=row)


tk.Button(root, text="Показать все договора", command=show_data).pack(pady=10)

# Таблица для отображения данных о договорах
columns = ("ID договора", "ID страхователя", "Дата заключения", "Сумма премии", "ID сотрудника")
treeview = ttk.Treeview(root, columns=columns, show="headings")
treeview.pack(pady=20)

# Настройка столбцов таблицы
for col in columns:
    treeview.heading(col, text=col)

# Обработчик клика по строке для отображения деталей договора
treeview.bind("<Double-1>", view_contract_details)

# Запуск главного окна
root.mainloop()
