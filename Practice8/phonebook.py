import psycopg2
from config import DB_CONFIG

def connect():
    return psycopg2.connect(**DB_CONFIG)

def search(pattern):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def upsert(name, surname, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s, %s);", (name, surname, phone))
    conn.commit()
    cur.close()
    conn.close()

def bulk_insert(names, surnames, phones):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_contacts(%s::varchar[], %s::varchar[], %s::varchar[]);", (names, surnames, phones))
    conn.commit()
    cur.execute("SELECT * FROM invalid_contacts;")
    bad = cur.fetchall()
    cur.close()
    conn.close()
    return bad

def get_page(limit, offset):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def delete_phone(phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(p_phone := %s);", (phone,))
    conn.commit()
    cur.close()
    conn.close()

def delete_name(name, surname):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(p_name := %s, p_surname := %s);", (name, surname))
    conn.commit()
    cur.close()
    conn.close()

def main():
    upsert("Amir", "Seitkali", "+77001112233")
    upsert("Dana", "Akhmetova", "+77002223344")
    upsert("Amir", "Seitkali", "+77009999999")

    bad = bulk_insert(
        ["Lena", "Nurlan", "Test"],
        ["Kim", "Ospanov", "Guy"],
        ["+77004445566", "87005556677", "abc"]
    )
    print("invalid:", bad)

    print(search("Amir"))
    print(get_page(3, 0))

    delete_phone("+77009999999")
    delete_name("Dana", "Akhmetova")

main()
