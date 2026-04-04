import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            phone VARCHAR(20) UNIQUE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("saved")

def import_csv(path):
    conn = get_connection()
    cur = conn.cursor()
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING", (row[0], row[1]))
    conn.commit()
    cur.close()
    conn.close()
    print("imported")

def show_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def search(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{name}%",))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def update(name, new_phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE phonebook SET phone=%s WHERE first_name=%s", (new_phone, name))
    conn.commit()
    cur.close()
    conn.close()
    print("updated")

def delete(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE first_name=%s", (name,))
    conn.commit()
    cur.close()
    conn.close()
    print("deleted")

def menu():
    create_table()
    while True:
        print("\n1. add\n2. import csv\n3. show all\n4. search\n5. update\n6. delete\n0. exit")
        c = input("choice: ")
        if c == "1":
            insert(input("name: "), input("phone: "))
        elif c == "2":
            import_csv("contacts.csv")
        elif c == "3":
            show_all()
        elif c == "4":
            search(input("name: "))
        elif c == "5":
            update(input("name: "), input("new phone: "))
        elif c == "6":
            delete(input("name: "))
        elif c == "0":
            break

menu()
