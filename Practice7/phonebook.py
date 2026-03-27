"""
PhoneBook Application — Practice 7
Integrates Python with PostgreSQL via psycopg2.
Supports: create table, import CSV, console entry,
          search/filter, update, delete.
"""

import csv
import re
from connect import get_connection


# ─────────────────────────────────────────────
#  SETUP
# ─────────────────────────────────────────────

def create_table():
    """Create the phonebook table if it does not exist yet."""
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id         SERIAL PRIMARY KEY,
        first_name VARCHAR(50)  NOT NULL,
        last_name  VARCHAR(50),
        phone      VARCHAR(20)  NOT NULL UNIQUE
    );
    """
    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
        print("[OK] Table 'phonebook' is ready.")
    except Exception as e:
        print(f"[ERROR] create_table: {e}")
    finally:
        conn.close()


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def is_valid_phone(phone: str) -> bool:
    """Accept formats like +7XXXXXXXXXX or 8XXXXXXXXXX (10-15 digits)."""
    return bool(re.fullmatch(r"[+]?\d{10,15}", phone.strip()))


def print_rows(rows):
    """Pretty-print a list of phonebook rows."""
    if not rows:
        print("  (no records found)")
        return
    print(f"\n  {'ID':<5} {'First Name':<15} {'Last Name':<15} {'Phone':<20}")
    print("  " + "-" * 55)
    for row in rows:
        pid, fn, ln, ph = row
        print(f"  {pid:<5} {fn:<15} {ln or '':<15} {ph:<20}")
    print()


# ─────────────────────────────────────────────
#  CREATE / INSERT
# ─────────────────────────────────────────────

def insert_one(first_name: str, last_name: str, phone: str):
    """Insert a single contact; update phone if name already exists."""
    if not is_valid_phone(phone):
        print(f"  [WARN] Invalid phone number: '{phone}'. Skipping.")
        return

    # Upsert: if the phone already exists, update the name instead
    sql = """
    INSERT INTO phonebook (first_name, last_name, phone)
    VALUES (%s, %s, %s)
    ON CONFLICT (phone)
    DO UPDATE SET first_name = EXCLUDED.first_name,
                  last_name  = EXCLUDED.last_name;
    """
    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name.strip(), last_name.strip(), phone.strip()))
        print(f"  [OK] Saved: {first_name} {last_name} — {phone}")
    except Exception as e:
        print(f"  [ERROR] insert_one: {e}")
    finally:
        conn.close()


def insert_from_csv(filepath: str):
    """Load contacts from a CSV file (columns: first_name, last_name, phone)."""
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"  [ERROR] File not found: {filepath}")
        return

    valid, skipped = [], []
    for row in rows:
        fn = row.get("first_name", "").strip()
        ln = row.get("last_name", "").strip()
        ph = row.get("phone", "").strip()
        if fn and ph and is_valid_phone(ph):
            valid.append((fn, ln, ph))
        else:
            skipped.append(row)

    if skipped:
        print(f"  [WARN] Skipped {len(skipped)} invalid row(s):")
        for r in skipped:
            print(f"         {r}")

    if not valid:
        print("  No valid rows to import.")
        return

    sql = """
    INSERT INTO phonebook (first_name, last_name, phone)
    VALUES (%s, %s, %s)
    ON CONFLICT (phone)
    DO UPDATE SET first_name = EXCLUDED.first_name,
                  last_name  = EXCLUDED.last_name;
    """
    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.executemany(sql, valid)
        print(f"  [OK] Imported {len(valid)} contact(s) from '{filepath}'.")
    except Exception as e:
        print(f"  [ERROR] insert_from_csv: {e}")
    finally:
        conn.close()


def console_insert():
    """Prompt the user to enter one contact manually."""
    print("\n  --- Add Contact ---")
    first_name = input("  First name : ").strip()
    last_name  = input("  Last name  : ").strip()
    phone      = input("  Phone      : ").strip()

    if not first_name:
        print("  [WARN] First name cannot be empty.")
        return
    insert_one(first_name, last_name, phone)


# ─────────────────────────────────────────────
#  READ / SEARCH
# ─────────────────────────────────────────────

def search_contacts(name_filter: str = "", phone_prefix: str = ""):
    """
    Search contacts:
      - name_filter   : partial match on first_name or last_name (case-insensitive)
      - phone_prefix  : phone number starts with this string
    Leaving both empty returns all contacts.
    """
    conditions = []
    params = []

    if name_filter:
        conditions.append(
            "(LOWER(first_name) LIKE %s OR LOWER(last_name) LIKE %s)"
        )
        like = f"%{name_filter.lower()}%"
        params += [like, like]

    if phone_prefix:
        conditions.append("phone LIKE %s")
        params.append(f"{phone_prefix}%")

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    sql = f"SELECT id, first_name, last_name, phone FROM phonebook {where} ORDER BY first_name;"

    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
        print_rows(rows)
    except Exception as e:
        print(f"  [ERROR] search_contacts: {e}")
    finally:
        conn.close()


def console_search():
    """Interactive search menu."""
    print("\n  --- Search Contacts ---")
    print("  1. By name (partial)")
    print("  2. By phone prefix")
    print("  3. Show all")
    choice = input("  Choice: ").strip()

    if choice == "1":
        name = input("  Enter name fragment: ").strip()
        search_contacts(name_filter=name)
    elif choice == "2":
        prefix = input("  Enter phone prefix: ").strip()
        search_contacts(phone_prefix=prefix)
    elif choice == "3":
        search_contacts()
    else:
        print("  Invalid choice.")


# ─────────────────────────────────────────────
#  UPDATE
# ─────────────────────────────────────────────

def update_by_name(old_first_name: str, new_first_name: str = None, new_phone: str = None):
    """Update first_name and/or phone for all contacts with the given first_name."""
    if not new_first_name and not new_phone:
        print("  [WARN] Nothing to update.")
        return
    if new_phone and not is_valid_phone(new_phone):
        print(f"  [WARN] Invalid new phone: '{new_phone}'")
        return

    sets, params = [], []
    if new_first_name:
        sets.append("first_name = %s")
        params.append(new_first_name.strip())
    if new_phone:
        sets.append("phone = %s")
        params.append(new_phone.strip())

    params.append(old_first_name.strip())
    sql = f"UPDATE phonebook SET {', '.join(sets)} WHERE first_name = %s;"

    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                count = cur.rowcount
        print(f"  [OK] Updated {count} row(s).")
    except Exception as e:
        print(f"  [ERROR] update_by_name: {e}")
    finally:
        conn.close()


def update_by_phone(old_phone: str, new_first_name: str = None, new_phone: str = None):
    """Update contact identified by current phone number."""
    if not new_first_name and not new_phone:
        print("  [WARN] Nothing to update.")
        return
    if new_phone and not is_valid_phone(new_phone):
        print(f"  [WARN] Invalid new phone: '{new_phone}'")
        return

    sets, params = [], []
    if new_first_name:
        sets.append("first_name = %s")
        params.append(new_first_name.strip())
    if new_phone:
        sets.append("phone = %s")
        params.append(new_phone.strip())

    params.append(old_phone.strip())
    sql = f"UPDATE phonebook SET {', '.join(sets)} WHERE phone = %s;"

    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                count = cur.rowcount
        print(f"  [OK] Updated {count} row(s).")
    except Exception as e:
        print(f"  [ERROR] update_by_phone: {e}")
    finally:
        conn.close()


def console_update():
    """Interactive update menu."""
    print("\n  --- Update Contact ---")
    print("  1. Find by first name")
    print("  2. Find by phone")
    choice = input("  Choice: ").strip()

    if choice == "1":
        old = input("  Current first name: ").strip()
        new_fn = input("  New first name (Enter to skip): ").strip()
        new_ph = input("  New phone (Enter to skip): ").strip()
        update_by_name(old, new_fn or None, new_ph or None)
    elif choice == "2":
        old_ph = input("  Current phone: ").strip()
        new_fn = input("  New first name (Enter to skip): ").strip()
        new_ph = input("  New phone (Enter to skip): ").strip()
        update_by_phone(old_ph, new_fn or None, new_ph or None)
    else:
        print("  Invalid choice.")


# ─────────────────────────────────────────────
#  DELETE
# ─────────────────────────────────────────────

def delete_by_name(first_name: str):
    sql = "DELETE FROM phonebook WHERE first_name = %s;"
    _execute_delete(sql, (first_name.strip(),))


def delete_by_phone(phone: str):
    sql = "DELETE FROM phonebook WHERE phone = %s;"
    _execute_delete(sql, (phone.strip(),))


def _execute_delete(sql: str, params: tuple):
    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                count = cur.rowcount
        print(f"  [OK] Deleted {count} row(s).")
    except Exception as e:
        print(f"  [ERROR] delete: {e}")
    finally:
        conn.close()


def console_delete():
    """Interactive delete menu."""
    print("\n  --- Delete Contact ---")
    print("  1. By first name")
    print("  2. By phone")
    choice = input("  Choice: ").strip()

    if choice == "1":
        name = input("  First name to delete: ").strip()
        confirm = input(f"  Delete all contacts named '{name}'? (y/n): ").strip().lower()
        if confirm == "y":
            delete_by_name(name)
    elif choice == "2":
        phone = input("  Phone to delete: ").strip()
        confirm = input(f"  Delete contact with phone '{phone}'? (y/n): ").strip().lower()
        if confirm == "y":
            delete_by_phone(phone)
    else:
        print("  Invalid choice.")


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

MENU = """
╔══════════════════════════════════╗
║        PhoneBook — Menu          ║
╠══════════════════════════════════╣
║  1. Add contact (console)        ║
║  2. Import from CSV              ║
║  3. Search / Show contacts       ║
║  4. Update contact               ║
║  5. Delete contact               ║
║  0. Exit                         ║
╚══════════════════════════════════╝
"""

def main():
    print("\n  Initialising database table...")
    create_table()

    while True:
        print(MENU)
        choice = input("  Your choice: ").strip()

        if choice == "1":
            console_insert()
        elif choice == "2":
            path = input("  CSV file path [contacts.csv]: ").strip() or "contacts.csv"
            insert_from_csv(path)
        elif choice == "3":
            console_search()
        elif choice == "4":
            console_update()
        elif choice == "5":
            console_delete()
        elif choice == "0":
            print("\n  Goodbye!\n")
            break
        else:
            print("  [WARN] Unknown option, try again.")


if __name__ == "__main__":
    main()
