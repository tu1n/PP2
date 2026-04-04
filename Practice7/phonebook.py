import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50),
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert(first_name, last_name, phone):
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO phonebook (first_name, last_name, phone)
        VALUES (%s, %s, %s)
        ON CONFLICT (phone) DO UPDATE
        SET first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name
    """, (first_name, last_name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("saved")

def import_csv(path):
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [(r["first_name"], r["last_name"], r["phone"]) for r in reader]
    cur.executemany("""
        INSERT INTO phonebook (first_name, last_name, phone)
        VALUES (%s, %s, %s)
        ON CONFLICT (phone) DO UPDATE
        SET first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name
    """, rows)
    conn.commit()
    cur.close()
    conn.close()
    print(f"imported {len(rows)} rows")

def search(name="", phone=""):
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    if name:
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{name}%",))
    elif phone:
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (f"{phone}%",))
    else:
        cur.execute("SELECT * FROM phonebook ORDER BY first_name")
    rows = cur.fetchall()
    for r in rows:
        print(r)
    cur.close()
    conn.close()

def update_by_name(old_name, new_name=None, new_phone=None):
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE phonebook SET first_name=%s WHERE first_name=%s", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone=%s WHERE first_name=%s", (new_phone, old_name))
    conn.commit()
    print("updated", cur.rowcount, "rows")
    cur.close()
    conn.close()

def delete(name=None, phone=None):
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    if name:
        cur.execute("DELETE FROM phonebook WHERE first_name=%s", (name,))
    elif phone:
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()
    print("deleted", cur.rowcount, "rows")
    cur.close()
    conn.close()

def menu():
    create_table()
    while True:
        print("\n1. add\n2. import csv\n3. search\n4. update\n5. delete\n0. exit")
        c = input("choice: ")
        if c == "1":
            fn = input("first name: ")
            ln = input("last name: ")
            ph = input("phone: ")
            insert(fn, ln, ph)
        elif c == "2":
            path = input("csv path [contacts.csv]: ") or "contacts.csv"
            import_csv(path)
        elif c == "3":
            print("1. by name  2. by phone  3. all")
            s = input("choice: ")
            if s == "1":
                search(name=input("name: "))
            elif s == "2":
                search(phone=input("phone prefix: "))
            else:
                search()
        elif c == "4":
            old = input("current first name: ")
            nn = input("new name (enter to skip): ")
            np = input("new phone (enter to skip): ")
            update_by_name(old, nn or None, np or None)
        elif c == "5":
            print("1. by name  2. by phone")
            s = input("choice: ")
            if s == "1":
                delete(name=input("name: "))
            elif s == "2":
                delete(phone=input("phone: "))
        elif c == "0":
            break

if __name__ == "__main__":
    menu()
