
-- первое процедура: добавить телефон контакту
CREATE OR REPLACE PROCEDURE add_phone(
    p_name  VARCHAR,   -- имя контакта
    p_phone VARCHAR,   -- номер телефона
    p_type  VARCHAR    -- тип: home, work, mobile
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    -- ищем id контакта по имени
    SELECT id INTO v_id FROM contacts WHERE first_name = p_name LIMIT 1;

    -- Если не нашли — ошибка
    IF v_id IS NULL THEN
        RAISE EXCEPTION 'Контакт % не найден', p_name;
    END IF;

    --вставляем телефон
    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_name  VARCHAR,   -- имя контакта
    p_group VARCHAR    -- название группы
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    -- Ищем группу
    SELECT id INTO v_group_id FROM groups WHERE name = p_group;

    -- Если группы нет — создаём
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group) RETURNING id INTO v_group_id;
    END IF;

    --ищем контакт
    SELECT id INTO v_contact_id FROM contacts WHERE first_name = p_name LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Контакт % не найден', p_name;
    END IF;

    -- Обновляем группу у контакта
    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;


--  умный поиск по всем полям

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INTEGER, first_name VARCHAR, last_name VARCHAR,
    email VARCHAR, birthday DATE, grp VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id, c.first_name, c.last_name,
        c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE
        c.first_name ILIKE '%' || p_query || '%'   -- поиск по имени
        OR c.last_name  ILIKE '%' || p_query || '%' -- по фамилии
        OR c.email      ILIKE '%' || p_query || '%' -- по email
        OR p.phone      ILIKE '%' || p_query || '%'; -- по телефону
END;
$$;


--  (страницы)
CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INTEGER, p_offset INTEGER)
RETURNS TABLE(
    id INTEGER, first_name VARCHAR, last_name VARCHAR,
    email VARCHAR, birthday DATE, grp VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    ORDER BY c.first_name
    LIMIT p_limit OFFSET p_offset;
END;
$$;
