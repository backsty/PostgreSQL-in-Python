import psycopg2
from pprint import pprint


def create_db(cur):
    """Создание основной таблицы с информацией о клиентах"""
    cur.execute("""
                DROP TABLE phones;
                DROP TABLE customers;
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS customers(
                id SERIAL PRIMARY KEY,
                client_name VARCHAR(100) NOT NULL,
                client_surname VARCHAR(100) NOT NULL,
                client_email VARCHAR(100) NOT NULL);
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS phones(
                phone VARCHAR(100) UNIQUE,
                client_id INTEGER REFERENCES customers(id));
                """)
    conn.commit()  # Фиксируем в бд

def delete_db(cur):
    cur.execute("""
                DROP TABLE customers, phones CASCADE;
                """)

def add_new_client(cur, client_name, client_surname, client_email):
    """Добавление нового клиента в БД"""
    cur.execute("""
                INSERT INTO customers (client_name, client_surname, client_email) VALUES(%s, %s, %s) RETURNING id;
                """, (client_name, client_surname, client_email))
    client_id = cur.fetchone()[0]
    return client_id


def add_phone(cur, client_id, phone):
    cur.execute("""
    INSERT INTO phones(client_id, phone) VALUES(%s, %s);
    """, (client_id, phone))
    conn.commit()  # Добавление в Бд


def change_client(cur):
    """Изменение информации о клиенте"""
    client_id = input("Введите ID клиента, информацию которого вы хотите изменить: ")
    print("Для изменения информации о клиенте, вам нужно ввести нужную команду:\n"
          "1 - изменить имя\n"
          "2 - изменить фамилию\n"
          "3 - изменить email\n"
          "4 - изменить номер телефона")

    command_symbol = int(input("Введите номер команды: "))

    while True:
        if command_symbol == 1:
            # input_id_customers = input("Введите id клиента, имя которого хотите изменить: ")
            input_name_customers = input("Введите новое имя: ")
            cur.execute("""
                        UPDATE customers SET client_name=%s WHERE id=%s;
                        """, (input_name_customers, client_id))
            break
        elif command_symbol == 2:
            input_surname_customers = input("Введите новую фамилию: ")
            cur.execute("""
                        UPDATE customers SET client_surname=%s WHERE id=%s;
                        """, (input_surname_customers, client_id))
            break
        elif command_symbol == 3:
            input_email_customers = input("Введите новый email: ")
            cur.execute("""
                        UPDATE customers SET client_email=%s WHERE id=%s;
                        """, (input_email_customers, client_id))
            break
        elif command_symbol == 4:
            input_phone_customers = input("Введите новый номер телефона: ")
            cur.execute("""
                        UPDATE phones SET phone=%s WHERE client_id=%s;
                        """, (input_phone_customers, client_id))
            break
        else:
            print("К сожалению, вы ввели неправильную команду, или данные уже изменены на текущие, "
                  "в противном случае, пожалуйста повторите ввод")


def delete_phone(cur):
    """Удаление номера телефона клиента из таблицы phone"""
    client_id = input("Введите ID клиента, телефон которого вы хотите удалить: ")
    phone_num_for_del = input("Введите новый номер телефона, который хотите удалить: ")

    while True:
        cur.execute("""
                    DELETE FROM phones WHERE client_id=%s AND phone=%s;
                    """, (client_id, phone_num_for_del))
        return f"Телефонный номер клиента, чей id {client_id} успешно удалён!"


def delete_client(cur):
    """Удаление информации о клиенте на данный момент времени"""
    client_id = input("Введите id клиента, чью информацию вы хотите удалить: ")
    client_name = input("Введите Имя человека, чью информацию вы хотите удалить: ")
    client_surname = input("Введите Фамилию человека, чью информацию вы хотите удалить: ")
    client_email = input("Введите email человека, чью информацию вы хотите удалить: ")
    phone_num_for_del = input("Введите новый номер телефона, который хотите удалить: ")

    """Удаление связи из таблицы phone (Сначала удаляем из phone т к от неё зависит таблица customers"""
    cur.execute("""
                DELETE FROM phones WHERE client_id=%s AND phone=%s;
                """, (client_id, phone_num_for_del))

    """Удаление связи из таблицы customers"""
    cur.execute("""
                DELETE FROM customers WHERE id=%s AND client_name=%s AND client_surname=%s AND client_email=%s;
                """, (client_id, client_name, client_surname, client_email))
    return f"Клиент удалён из Бд. Его id {client_id}"


def find_client(cur):
    """Добавляем функцию для поиска клиента по данным из таблицы customers"""
    print("Для поиска информации о клиенте, введите нужную команду: \n"
          "1 - Найти по имени\n"
          "2 - Найти по фамилии\n"
          "3 - Найти по email\n"
          "4 - Найти по номеру телефона")

    command_symbol_find = int(input("Введите номер команды для поиска информации о клиенте: "))

    while True:

        if command_symbol_find == 1:
            input_name = input("Введите имя клиента: ")
            cur.execute("""
                        SELECT ct.id, ct.client_name, ct.client_surname, ct.client_email, p.phone
                        FROM customers AS ct
                        LEFT JOIN phones AS p ON p.client_id = ct.id
                        WHERE client_name=%s
                        """, (input_name,))
            print(cur.fetchall())
            break
        elif command_symbol_find == 2:
            input_surname = input("Введите фамилию клиента: ")
            cur.execute("""
                        SELECT ct.id, ct.client_name, ct.client_surname, ct.client_email, p.phone
                        FROM customers AS ct
                        LEFT JOIN phones AS p ON p.client_id = ct.id
                        WHERE client_surname=%s
                        """, (input_surname,))
            print(cur.fetchall())
            break
        elif command_symbol_find == 3:
            input_email = input("Введите email клиента: ")
            cur.execute("""
                        SELECT ct.id, ct.client_name, ct.client_surname, ct.client_email, p.phone
                        FROM customers AS ct
                        LEFT JOIN phones AS p ON p.client_id = ct.id
                        WHERE client_email=%s
                        """, (input_email,))
            print(cur.fetchall())
            break
        elif command_symbol_find == 4:
            input_phone = input("Введите номер телефона клиента: ")
            cur.execute("""
                        SELECT ct.id, ct.client_name, ct.client_surname, ct.client_email, p.phone
                        FROM customers AS ct
                        LEFT JOIN phones AS p ON p.client_id = ct.id
                        WHERE phone=%s
                        """, (input_phone,))
            print(cur.fetchall())
            break
        else:
            print("К сожалению, нам не удалось найти информацию о клиенте, пожалуйста проверьте "
                  "правильность введённых вами данных и попробуйте ещё раз!")


def check_table(cur):
    """Функция, которая отображает содержимое таблиц"""
    cur.execute("""
    SELECT * FROM customers;
    """)
    pprint(cur.fetchall())
    cur.execute("""
    SELECT * FROM phones
    """)
    pprint(cur.fetchall())


with psycopg2.connect(database="clients_db", user="postgres", password="Pro23242pro") as conn:
    with conn.cursor() as cur:
        create_db(cur)

        add_new_client(cur, "Artem", "Grace", "ArtemGrace@gmail.com")
        add_new_client(cur, "Alfie", "Smith", "AlfieSmith@mail.ru")
        add_new_client(cur, "Harry", "Moore", "HarryMoore@mail.ru")
        add_new_client(cur, "Charlie", "Williams", "CharlieWilliams@gmail.com")
        add_new_client(cur, "Oliver", "Taylor", "OliverTaylor@mail.ru")
        add_new_client(cur, "Jack", "Miller", "JackMiller@gmail.com")
        add_new_client(cur, "Tony", "Stark", "TonyStark@mail.ru")
        add_new_client(cur, "John", "Evans", "JohnEvans@mail.ru")

        add_phone(cur, 1, "+79659900202")
        add_phone(cur, 2, "+79665009500")
        add_phone(cur, 3, "+79069070070")
        add_phone(cur, 4, "+79069955955")
        add_phone(cur, 5, "+79039996799")
        add_phone(cur, 6, "+77773330303")
        add_phone(cur, 7, "+79659997007")
        add_phone(cur, 8, "+79832001122")

        # # Сделал для того, чтобы id было вначале, а за ним шёл phone
        # cur.execute("""
        # SELECT phones.client_id, phones.phone
        # FROM phones
        # JOIN customers ON customers.id = phones.client_id;
        # """)
        # result = cur.fetchall()
        # pprint(result)

        change_client(cur)

        delete_phone(cur)

        delete_client(cur)

        find_client(cur)

        check_table(cur)

cur.close()
conn.close()
