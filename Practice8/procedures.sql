CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_surname VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, last_name, phone) VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_names VARCHAR[], p_surnames VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    DROP TABLE IF EXISTS invalid_contacts;
    CREATE TEMP TABLE invalid_contacts(name VARCHAR, phone VARCHAR, reason TEXT);

    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] !~ '^\+?[0-9]{7,15}$' THEN
            INSERT INTO invalid_contacts VALUES (p_names[i], p_phones[i], 'bad phone');
        ELSE
            CALL upsert_contact(p_names[i], p_surnames[i], p_phones[i]);
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_name VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
    ELSE
        DELETE FROM phonebook WHERE first_name = p_name;
    END IF;
END;
$$;
