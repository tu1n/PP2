
import csv
import json
from connect import get_connection

#открываем соединение с базой данных
conn = get_connection()


def show(rows):
    """Печатает контакты в виде таблицы."""
    if not rows:
        print("  Контактов нет.\n")
        return
    print(f"\n  {'ID':<5} {'Имя':<15} {'Фамилия':<15} {'Email':<22} {'ДР':<13} {'Группа'}")
    print("  " + "-" * 78)
    for r in rows:
        # r = (id, first_name, last_name, email, birthday, group)
        print(f"  {r[0]:<5} {str(r[1]):<15} {str(r[2] or ''):<15} {str(r[3] or ''):<22} {str(r[4] or ''):<13} {str(r[5] or '')}")
    print()


def add_contact():
    print("\n--- Добавить контакт ---")

    # Просим пользователя ввести данные
    fname =input("Имя: ").strip()
    lname =input("Фамилия (Enter = пропустить): ").strip() or None
    email = input("Email    (Enter = пропустить): ").strip() or None
    bday  =input("День рождения ГГГГ-ММ-ДД (Enter = пропустить): ").strip() or None

    #показываем список групп
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM groups ORDER BY id")
        groups = cur.fetchall()
    print("Группы:")
    for gid, gname in groups:
        print(f"  {gid}. {gname}")

    g = input("Номер группы (Enter = пропустить): ").strip()
    group_id =int(g) if g.isdigit() else None

    #    Вставляем контакт в таблицу contacts
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO contacts (first_name, last_name, email, birthday, group_id) VALUES (%s,%s,%s,%s,%s) RETURNING id",
            (fname, lname, email, bday, group_id)
        )
        contact_id = cur.fetchone()[0]

    # Добавляем телефоны (можно несколько)
    while True:
        phone = input("Телефон (Enter = стоп): ").strip()
        if not phone:
            break
        ptype = input("Тип — home / work / mobile: ").strip()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                (contact_id, phone, ptype)
            )

    conn.commit()
    print("✅ Контакт добавлен!\n")


def filter_by_group():
    print("\n--- Фильтр по группе ---")

    #ппоказываем все группы
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM groups ORDER BY id")
        groups = cur.fetchall()
    for gid, gname in groups:
        print(f"  {gid}. {gname}")

    g = input("Номер группы: ").strip()
    if not g.isdigit():
        print("Неверный ввод.")
        return

    #тут выбираем контакты этой группы
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            WHERE c.group_id = %s
            ORDER BY c.first_name
        """, (int(g),))
        show(cur.fetchall())


def search_email():
    print("\n--- Поиск по email ---")
    query = input("Введи часть email (например gmail): ").strip()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            WHERE c.email ILIKE %s
            ORDER BY c.first_name
        """, (f"%{query}%",))   # %query% = содержит эту строку
        show(cur.fetchall())


def sort_contacts():
    print("\n--- Сортировка ---")
    print("  1. По имени")
    print("  2. По дню рождения")
    print("  3. По дате добавления")
    ch = input("Выбери: ").strip()

    # Определяем по какому полю сортировать
    if ch == "1":
        col = "c.first_name"
    elif ch == "2":
        col = "c.birthday"
    elif ch == "3":
        col = "c.created_at"
    else:
        col = "c.first_name"

    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY {col}
        """)
        show(cur.fetchall())


def paginate():
    print("\n--- Листание страниц ---")
    page_size = 3   # 3 контакта на странице
    offset    = 0   # начинаем с первого

    while True:
        # вызываем функцию из БД
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (page_size, offset))
            rows = cur.fetchall()

            # Считаем общее количество контактов
            cur.execute("SELECT COUNT(*) FROM contacts")
            total = cur.fetchone()[0]

        page       = offset // page_size + 1
        total_pages = max((total + page_size - 1) // page_size, 1)

        print(f"\n  Страница {page} из {total_pages}  (всего: {total})")
        show(rows)
        print("  n = следующая   p = предыдущая   q = выход")
        cmd = input("  → ").strip().lower()

        if cmd == "n":
            if offset + page_size < total:
                offset += page_size
            else:
                print("  Это последняя страница.")
        elif cmd == "p":
            if offset > 0:
                offset -= page_size
            else:
                print("  Это первая страница.")
        elif cmd == "q":
            break


def export_json():
    print("\n--- Экспорт в JSON ---")

    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email,
                   c.birthday::text, g.name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
        """)
        contacts = cur.fetchall()

    result = []
    for (cid, fn, ln, em, bd, gr) in contacts:
        # Получаем все телефоны этого контакта
        with conn.cursor() as cur:
            cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (cid,))
            phones = cur.fetchall()

        result.append({
            "first_name": fn,
            "last_name":  ln or "",
            "email":      em or "",
            "birthday":   bd or "",
            "group":      gr or "",
            "phones": [{"phone": p, "type": t} for p, t in phones]
        })

    # Записываем в файл
    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ Сохранено {len(result)} контактов → contacts.json\n")


def import_json():
    print("\n--- Импорт из JSON ---")
    filename = input("Имя файла (Enter = contacts.json): ").strip() or "contacts.json"

    try:
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return

    added = skipped = 0

    for item in data:
        fname = item.get("first_name", "").strip()
        if not fname:
            continue

        # Проверяем — есть ли уже такой контакт
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM contacts WHERE first_name = %s LIMIT 1", (fname,))
            exists = cur.fetchone()

        if exists:
            ans = input(f"  '{fname}' уже есть! Перезаписать? (y/n): ").strip().lower()
            if ans == "y":
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM contacts WHERE id = %s", (exists[0],))
                conn.commit()
            else:
                skipped += 1
                continue

        # Получаем group_id (или создаём группу)
        group_id = None
        grp = item.get("group", "").strip()
        if grp:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM groups WHERE name = %s", (grp,))
                row = cur.fetchone()
                if row:
                    group_id = row[0]
                else:
                    cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (grp,))
                    group_id = cur.fetchone()[0]

        # Вставляем контакт
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO contacts (first_name, last_name, email, birthday, group_id) VALUES (%s,%s,%s,%s,%s) RETURNING id",
                (fname, item.get("last_name") or None, item.get("email") or None,
                 item.get("birthday") or None, group_id)
            )
            cid = cur.fetchone()[0]

            # Вставляем телефоны
            for ph in item.get("phones", []):
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                    (cid, ph["phone"], ph.get("type", "mobile"))
                )
        conn.commit()
        added += 1

    print(f"✅ Добавлено: {added}, пропущено: {skipped}\n")


#ИМПОРТ ИЗ CSV


def import_csv():
    print("\n--- Импорт из CSV ---")
    filename = input("Имя файла (Enter = contacts.csv): ").strip() or "contacts.csv"

    try:
        f = open(filename, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return

    added = 0
    for row in csv.DictReader(f):
        fname = row.get("first_name", "").strip()
        if not fname:
            continue

        # Получаем group_id
        group_id = None
        grp = row.get("group", "").strip()
        if grp:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM groups WHERE name = %s", (grp,))
                g = cur.fetchone()
                if g:
                    group_id = g[0]
                else:
                    cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (grp,))
                    group_id = cur.fetchone()[0]

        # Вставляем контакт (ON CONFLICT DO NOTHING = не дублировать)
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO contacts (first_name, last_name, email, birthday, group_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING RETURNING id",
                (fname,
                 row.get("last_name") or None,
                 row.get("email")     or None,
                 row.get("birthday")  or None,
                 group_id)
            )
            res = cur.fetchone()

        # Вставляем телефон если есть
        if res and row.get("phone"):
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                    (res[0], row["phone"], row.get("phone_type", "mobile"))
                )
        conn.commit()
        added += 1

    f.close()
    print(f"✅ Импортировано из CSV: {added}\n")



def add_phone():
    print("\n--- Добавить телефон (процедура) ---")
    name  = input("Имя контакта: ").strip()
    phone = input("Номер телефона: ").strip()
    ptype = input("Тип (home/work/mobile): ").strip()

    try:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print("✅ Телефон добавлен!\n")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}\n")

def move_to_group():
    print("\n--- Переместить в группу (процедура) ---")
    name  = input("Имя контакта: ").strip()
    group = input("Название группы: ").strip()

    try:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print("✅ Контакт перемещён в группу!\n")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}\n")


def smart_search():
    print("\n--- Умный поиск ---")
    query = input("Введи текст (имя / email / телефон): ").strip()

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        show(cur.fetchall())


# ГЛАВНОЕ МЕНЮ


def main():
    print("╔════════════════════════════════╗")
    print("║      PhoneBook — TSIS 1        ║")
    print("╚════════════════════════════════╝")

    while True:
        print("  Меню:")
        print("  1.  Добавить контакт")
        print("  2.  Фильтр по группе")
        print("  3.  Поиск по email")
        print("  4.  Сортировка")
        print("  5.  Листать страницы")
        print("  6.  Экспорт в JSON")
        print("  7.  Импорт из JSON")
        print("  8.  Импорт из CSV")
        print("  9.  Добавить телефон (процедура)")
        print("  10. Переместить в группу (процедура)")
        print("  11. Умный поиск (имя / email / телефон)")
        print("  0.  Выход")

        choice = input("\n  Выбери пункт: ").strip()

        if   choice =="1":  add_contact()
        elif choice =="2":  filter_by_group()
        elif choice == "3":  search_email()
        elif choice == "4":  sort_contacts()
        elif choice == "5":  paginate()
        elif choice == "6":  export_json()
        elif choice == "7":  import_json()
        elif choice == "8":  import_csv()
        elif choice == "9":  add_phone()
        elif choice == "10": move_to_group()
        elif choice == "11": smart_search()
        elif choice == "0":
            print("Пока!")
            break
        else:
            print("Нет такого пункта, попробуй ещё раз.\n")


#и запуск программы
if __name__ == "__main__":
    main()
    conn.close()
