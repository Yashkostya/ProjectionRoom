import os
import sqlite3


def show_films():
    clear_console()

    cursor.execute("SELECT * FROM films;")
    films = cursor.fetchall()

    print("\n|  {0:10s}  |  {1:50s}  |  {2:12s}  |".format('Код фильма', 'Название', 'Длительность'))
    for film in films:
        print(f"|  {film[0]:10d}  |  {film[1]:50s}  |  {film[2]:12d}  |")

    print('\n1. Добавить')
    print('2. Удалить')
    print('3. Сохранить и выйти в главное меню')

    print('\nВведите номер операции:')
    choice = input()

    if choice == '1':
        add_film()
        show_films()
    elif choice == '2':
        delete_film()
        show_films()
    else:
        connection.commit()
        return


def delete_film():
    cursor.execute("SELECT * FROM films;")
    films = cursor.fetchall()

    print("|  {0:10s}  |  {1:50s}  |  {2:12s}  |".format('Код фильма', 'Название', 'Длительность'))
    for film in films:
        print(f"|  {film[0]:10d}  |  {film[1]:50s}  |  {film[2]:12d}  |")

    while True:
        filmCode = input("\nВведите код фильма, который хотите удалить: ")
        if not filmCode.isdigit():
            print("Код фильма - это число! Введите корректное значение.\n")
        elif int(filmCode) < 1:
            print("Код фильма не может быть меньше 1! Введите корректное значение.\n")
        elif not any(x for x in films if x[0] == int(filmCode)):
            print('Фильма с таким кодом не существует!')
        else:
            break

    cursor.execute(f"DELETE FROM films WHERE code = {filmCode};")


def add_film():
    name = input("\nВведите название фильма: ")

    while True:
        duration = input("\nВведите продолжительность фильма (мин.): ")
        if not duration.isdigit():
            print("Продолжительность фильма - это число! Введите корректное значение.\n")
        elif int(duration) < 1:
            print("Продолжительность фильма не может быть меньше 1! Введите корректное значение.\n")
        else:
            break

    cursor.execute(f"INSERT INTO films(name, duration) VALUES ('{name}', {duration});")


def show_links():
    clear_console()

    cursor.execute("""SELECT films.code, films.name, projectors.room
        FROM films
        INNER JOIN link
        ON films.code = link.filmCode
        INNER JOIN projectors
        ON link.projectorRoom = projectors.room;""")
    links = cursor.fetchall()

    print("\n|  {0:15s}  |  {1:50s}  |  {2:3s}  |".format('Код фильма', 'Название фильма', 'Зал'))
    for link in links:
        print(f"|  {link[0]:15d}  |  {link[1]:50s}  |  {link[2]:3d}  |")
    print("\n")

    print('\n1. Добавить привязку')
    print('2. Удалить привязку')
    print('3. Сохранить и выйти в главное меню')

    print('\nВведите номер операции:')
    choice = input()

    if choice == '1':
        add_link()
        show_links()
    elif choice == '2':
        delete_link()
        show_links()
    else:
        connection.commit()
        return


def delete_link():
    cursor.execute("""SELECT films.code, films.name, projectors.room
        FROM films
        INNER JOIN link
        ON films.code = link.filmCode
        INNER JOIN projectors
        ON link.projectorRoom = projectors.room;""")
    links = cursor.fetchall()

    print("|  {0:15s}  |  {1:50s}  |  {2:3s}  |".format('Код фильма', 'Название фильма', 'Зал'))
    for link in links:
        print(f"|  {link[0]:15d}  |  {link[1]:50s}  |  {link[2]:3d}  |")
    print("\n")

    cursor.execute("SELECT * FROM films;")
    films = cursor.fetchall()
    while True:
        filmCode = input('\nВведите код фильма, у которого хотите удалить привязку: ')
        if not filmCode.isdigit():
            print("Код фильма - это число! Введите корректное значение.\n")
        elif int(filmCode) < 1:
            print("Код фильма не может быть меньше 1! Введите корректное значение.\n")
        elif not any(x for x in films if x[0] == int(filmCode)):
            print('Фильма с таким кодом не существует!')
        else:
            break

    cursor.execute("SELECT * FROM projectors;")
    projectors = cursor.fetchall()
    while True:
        projectorRoom = input('\nВведите номер зала: ')
        if not projectorRoom.isdigit():
            print("Номер зала - это число! Введите корректное значение.\n")
        elif int(projectorRoom) < 1:
            print("Номер зала не может быть меньше 1! Введите корректное значение.\n")
        elif not any(x for x in projectors if x[0] == int(projectorRoom)):
            print('Такого номера зала не существует!')
        else:
            break

    cursor.execute(f"DELETE FROM link WHERE filmCode = '{filmCode}' AND projectorRoom = {projectorRoom};")


def add_link():
    cursor.execute("SELECT * FROM films;")
    films = cursor.fetchall()

    print("|  {0:10s}  |  {1:50s}  |  {2:12s}  |".format('Код фильма', 'Название', 'Длительность'))
    for film in films:
        print(f"|  {film[0]:10d}  |  {film[1]:50s}  |  {film[2]:12d}  |")

    while True:
        filmCode = input("\nВведите код фильма, который хотите привязать к залу: ")
        if not filmCode.isdigit():
            print("Код фильма - это число! Введите корректное значение.\n")
        elif int(filmCode) < 1:
            print("Код фильма не может быть меньше 1! Введите корректное значение.\n")
        elif not any(x for x in films if x[0] == int(filmCode)):
            print('Фильма с таким кодом не существует!')
        else:
            break

    cursor.execute("SELECT * FROM projectors;")
    projectors = cursor.fetchall()

    print("|  {0:3s}  |  {1:6s}  |".format('Зал', 'Модель'))
    for projector in projectors:
        print(f"|  {projector[0]:3d}  |  {projector[1]:6s}  |")

    while True:
        projectorRoom = input("\nК какому залу привязать этот фильм? ")
        if not projectorRoom.isdigit():
            print("Номер зала - это число! Введите корректное значение.\n")
        elif int(projectorRoom) < 1:
            print("Номер зала не может быть меньше 1! Введите корректное значение.\n")
        elif not any(x for x in projectors if x[0] == int(projectorRoom)):
            print('Такого номера зала не существует!')
        else:
            cursor.execute(f"SELECT COUNT(*) FROM link WHERE filmCode = {filmCode} AND projectorRoom = {projectorRoom};")
            if cursor.fetchone()[0] == 0:
                break
            else:
                print("Фильм не может быть повторно привязан к залу! Введите корректное значение.\n")

    cursor.execute(f"INSERT INTO link(projectorRoom,filmCode) VALUES ({projectorRoom}, {filmCode});")


def show_projectors():
    clear_console()

    cursor.execute("SELECT * FROM projectors ORDER BY room;")
    projectors = cursor.fetchall()

    print("\n|  {0:4s}  |  {1:6s}  |".format('Зал', 'Модель'))
    for projector in projectors:
        print(f"|  {projector[0]:4d}  |  {projector[1]:6s}  |")

    print('\n1. Добавить')
    print('2. Удалить')
    print('3. Сохранить и выйти в главное меню')

    print('\nВведите номер операции:')
    choice = input()

    if choice == '1':
        add_projector()
        show_projectors()
    elif choice == '2':
        delete_projector()
        show_projectors()
    else:
        connection.commit()
        return


def delete_projector():
    cursor.execute("SELECT * FROM projectors;")
    projectors = cursor.fetchall()
    while True:
        room = input('\nВведите номер зала: ')
        if not room.isdigit():
            print("Номер зала - это число! Введите корректное значение.\n")
        elif int(room) < 1:
            print("Номер зала не может быть меньше 1! Введите корректное значение.\n")
        elif not any(x for x in projectors if x[0] == int(room)):
            print('Такого номера зала не существует!')
        else:
            break

    cursor.execute(f"DELETE FROM projectors WHERE room = {room};")


def add_projector():
    cursor.execute("SELECT * FROM projectors;")
    projectors = cursor.fetchall()
    while True:
        room = input('\nВведите номер зала: ')
        if not room.isdigit():
            print("Номер зала - это число! Введите корректное значение.\n")
        elif int(room) < 1:
            print("Номер зала не может быть меньше 1! Введите корректное значение.\n")
        else:
            cursor.execute(f"SELECT COUNT(*) FROM projectors WHERE room = {room};")
            if cursor.fetchone()[0] == 0:
                break
            else:
                print("Такой зал уже существует! Введите корректное значение.\n")

    model = input("\nВведите модель проектора: ")

    cursor.execute(f"INSERT INTO projectors (model, room) VALUES ('{model}', {room});")


def print_main_menu():
    clear_console()
    print('\n1. Фильмы')
    print('2. Проекторы')
    print('3. Привязка')
    print('4. Выйти из программы')


def clear_console():
    os.system('cls')


def init_database():
    # SQL-запрос для создания таблицы фильмов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS films (
        code     INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT    NOT NULL,
        duration INTEGER NOT NULL
    );
    """)
    # SQL-запрос для создания таблицы проекторов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projectors (
        room  INTEGER PRIMARY KEY NOT NULL,
        model TEXT    NOT NULL
    );
    """)
    # SQL-запрос для создания таблицы-связи (связь многие ко многим)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS link (
        filmCode      INTEGER NOT NULL,
        projectorRoom INTEGER NOT NULL,
        FOREIGN KEY (filmCode) REFERENCES films (code) ON DELETE CASCADE,
        FOREIGN KEY (projectorRoom) REFERENCES projectors (room) ON DELETE CASCADE
    );
    """)


def main():
    # Инициализировать базу данных
    init_database()

    while True:
        clear_console()
        print_main_menu()

        print('\nВведите номер операции:')
        choice = input()

        if choice == '1':
            clear_console()
            show_films()
        elif choice == '2':
            clear_console()
            show_projectors()
        elif choice == '3':
            clear_console()
            show_links()
        else:
            exit()


# Создание подключения к базе данных
connection = sqlite3.connect("ProjectionRoom.db")

# Объект, при помощи которого можно выполнять запросы
cursor = connection.cursor()

main()
