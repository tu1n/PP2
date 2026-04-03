CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_surname VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name AND last_name = p_surname) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name AND last_name = p_surname;
    ELSE
        INSERT INTO phonebook(first_name, last_name, phone) VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_names VARCHAR[], p_surnames VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    n VARCHAR;
    s VARCHAR;
    p VARCHAR;
BEGIN
    DROP TABLE IF EXISTS invalid_contacts;
    CREATE TEMP TABLE invalid_contacts(name VARCHAR, surname VARCHAR, phone VARCHAR, reason TEXT);
    FOR i IN 1..array_length(p_names, 1) LOOP
        n := TRIM(p_names[i]);
        s := TRIM(p_surnames[i]);
        p := TRIM(p_phones[i]);
        IF n = '' OR n IS NULL THEN
            INSERT INTO invalid_contacts VALUES (n, s, p, 'empty name');
            CONTINUE;
        END IF;
        IF p !~ '^\+?[0-9]{7,15}$' THEN
            INSERT INTO invalid_contacts VALUES (n, s, p, 'bad phone');
            CONTINUE;
        END IF;
        CALL upsert_contact(n, s, p);
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_name VARCHAR DEFAULT NULL, p_surname VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
    ELSIF p_name IS NOT NULL AND p_surname IS NOT NULL THEN
        DELETE FROM phonebook WHERE first_name = p_name AND last_name = p_surname;
    ELSE
        RAISE EXCEPTION 'need phone or name+surname';
    END IF;
END;
$$;
