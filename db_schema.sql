-- Crear la base de datos si no existe
CREATE DATABASE aidiary;

-- Conectarse a la base de datos
\c aidiary;

-- Crear la tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    photo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear la tabla de entradas de diario
CREATE TABLE IF NOT EXISTS diary_entries (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    entry_date DATE NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Procedimiento para insertar un usuario
CREATE OR REPLACE PROCEDURE insert_user(
    IN p_name VARCHAR,
    IN p_email VARCHAR,
    IN p_password VARCHAR,
    IN p_photo VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO users(name, email, password, photo)
    VALUES (p_name, p_email, p_password, p_photo);
END;
$$;

-- Procedimiento para actualizar un usuario
CREATE OR REPLACE PROCEDURE update_user_profile(
    IN p_id INT,
    IN p_name VARCHAR,
    IN p_email VARCHAR,
    IN p_password VARCHAR,
    IN p_photo VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users
    SET name = p_name,
        email = p_email,
        password = p_password,
        photo = p_photo,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = p_id;
END;
$$;

-- Procedimiento para eliminar un usuario
CREATE OR REPLACE PROCEDURE delete_user_profile(
    IN p_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM users WHERE id = p_id;
END;
$$;

-- Procedimiento para insertar una entrada en el diario
CREATE OR REPLACE PROCEDURE create_diary_entry(
    IN p_user_id INT,
    IN p_message TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO diary_entries(user_id, entry_date, message)
    VALUES (p_user_id, CURRENT_DATE, p_message);
END;
$$;

-- Procedimiento para eliminar una entrada del diario
CREATE OR REPLACE PROCEDURE delete_diary_entry(
    IN p_entry_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM diary_entries WHERE id = p_entry_id;
END;
$$;

-- Procedimiento para actualizar una entrada del diario
CREATE OR REPLACE PROCEDURE update_diary_entry(
    IN p_entry_id INT,
    IN p_message TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE diary_entries
    SET message = p_message,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = p_entry_id;
END;
$$;

-- Trigger para actualizar la fecha de actualización en la tabla 'users'
CREATE OR REPLACE FUNCTION update_updated_at_column_user()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column_user();

-- Trigger para actualizar la fecha de actualización en la tabla 'diary_entries'
CREATE OR REPLACE FUNCTION update_updated_at_column_diary()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_diary_entries_updated_at
BEFORE UPDATE ON diary_entries
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column_diary();

-- Crear vistas para consultar usuarios y sus entradas
CREATE OR REPLACE VIEW user_profile_view AS
SELECT id AS user_id, name, email, photo, created_at, updated_at
FROM users;

CREATE OR REPLACE VIEW user_entries_view AS
SELECT u.id AS user_id, u.name, de.id AS entry_id, de.message, de.entry_date, de.created_at, de.updated_at
FROM users u
JOIN diary_entries de ON u.id = de.user_id
ORDER BY de.entry_date DESC;

-- Crear índices para mejorar el rendimiento de las consultas
CREATE INDEX IF NOT EXISTS idx_diary_entries_user_date ON diary_entries(user_id, entry_date);
CREATE INDEX IF NOT EXISTS idx_user_id ON diary_entries(user_id);
CREATE INDEX IF NOT EXISTS idx_entry_date ON diary_entries(entry_date);

-- Asegurar que la columna entry_date sea de tipo DATE
ALTER TABLE diary_entries
ALTER COLUMN entry_date TYPE DATE USING entry_date::DATE;
