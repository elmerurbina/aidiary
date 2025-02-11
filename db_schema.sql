-- Create the 'aidiary' database if it doesn't exist already
CREATE DATABASE IF NOT EXISTS aidiary;

-- Connect to the 'aidiary' database
\c aidiary;

-- Create the 'users' table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,                      -- Auto-incrementing ID for each user
    name VARCHAR(255) NOT NULL,                  -- User's full name
    email VARCHAR(255) UNIQUE NOT NULL,          -- User's email (unique)
    password VARCHAR(255) NOT NULL,              -- User's password
    photo VARCHAR(255),                          -- Optional user photo URL or path
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp for when user created their account
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- Timestamp for when user data was last updated
);

-- Create the 'diary_entries' table
CREATE TABLE IF NOT EXISTS diary_entries (
    id SERIAL PRIMARY KEY,                      -- Auto-incrementing ID for each entry
    user_id INT REFERENCES users(id) ON DELETE CASCADE, -- Foreign key to the 'users' table, cascades on delete
    entry_date DATE NOT NULL,                    -- Date of the diary entry
    message TEXT NOT NULL,                       -- The message/diary content the user writes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp for when the entry was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- Timestamp for when the entry was last updated
);

-- Index for quick lookup of diary entries by date and user
CREATE INDEX IF NOT EXISTS idx_diary_entries_user_date ON diary_entries(user_id, entry_date);

-- Function to Insert a User
CREATE OR REPLACE FUNCTION insert_user(p_name VARCHAR, p_email VARCHAR, p_password VARCHAR, p_photo VARCHAR)
RETURNS VOID AS $$
BEGIN
    INSERT INTO users(name, email, password, photo)
    VALUES (p_name, p_email, p_password, p_photo);
END;
$$ LANGUAGE plpgsql;

-- Function to Update User Profile
CREATE OR REPLACE FUNCTION update_user_profile(
    p_id INT,
    p_name VARCHAR,
    p_email VARCHAR,
    p_password VARCHAR,
    p_photo VARCHAR
) RETURNS VOID AS $$
BEGIN
    UPDATE users
    SET name = p_name,
        email = p_email,
        password = p_password,
        photo = p_photo,
        updated_at = CURRENT_TIMESTAMP
    WHERE users.id = p_id;  -- Qualify the column with the table name
END;
$$ LANGUAGE plpgsql;

-- Function to Retrieve User by ID
CREATE OR REPLACE FUNCTION get_user_by_id(p_id INT)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    email VARCHAR,
    password VARCHAR,
    photo VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT users.id, users.name, users.email, users.password, users.photo, users.created_at, users.updated_at
    FROM users
    WHERE users.id = p_id;  -- Qualify the column with the table name
END;
$$ LANGUAGE plpgsql;

-- Function to Retrieve User by Email
CREATE OR REPLACE FUNCTION get_user_by_email(p_email VARCHAR)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    email VARCHAR,
    password VARCHAR,
    photo VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT users.id, users.name, users.email, users.password, users.photo, users.created_at, users.updated_at
    FROM users
    WHERE users.email = p_email;  -- Qualify the column with the table name
END;
$$ LANGUAGE plpgsql;

-- Function to Retrieve Entries by User
CREATE OR REPLACE FUNCTION get_entries_by_user(p_user_id integer, p_entry_date date)
RETURNS TABLE(id integer, user_id integer, entry_date date, message text, created_at timestamp, updated_at timestamp) AS
$$
BEGIN
    RETURN QUERY
    SELECT
        diary_entries.id,
        diary_entries.user_id,
        diary_entries.entry_date,  -- This should be DATE now
        diary_entries.message,
        diary_entries.created_at,
        diary_entries.updated_at
    FROM diary_entries
    WHERE diary_entries.user_id = p_user_id
    AND diary_entries.entry_date = p_entry_date  -- Direct comparison (no need to cast)
    ORDER BY diary_entries.entry_date DESC;
END;
$$ LANGUAGE plpgsql;


-- Function to Delete User Profile
CREATE OR REPLACE FUNCTION delete_user_profile(p_id INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM users WHERE users.id = p_id;  -- Qualify the column with the table name
END;
$$ LANGUAGE plpgsql;

-- Function to Create a Diary Entry
CREATE OR REPLACE FUNCTION create_diary_entry(
    p_user_id INT,
    p_entry_date DATE,
    p_message TEXT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO diary_entries(user_id, entry_date, message)
    VALUES (p_user_id, p_entry_date, p_message);
END;
$$ LANGUAGE plpgsql;

-- Trigger to Update 'updated_at' field for the 'users' table upon update
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

-- Trigger to Update 'updated_at' field for the 'diary_entries' table upon update
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

-- View to Retrieve User Profile
CREATE OR REPLACE VIEW user_profile_view AS
SELECT id AS user_id, name, email, photo, created_at, updated_at
FROM users;

-- View to Retrieve User Entries
CREATE OR REPLACE VIEW user_entries_view AS
SELECT u.id AS user_id, u.name, de.id AS entry_id, de.message, de.entry_date, de.created_at, de.updated_at
FROM users u
JOIN diary_entries de ON u.id = de.user_id
ORDER BY de.entry_date DESC;

-- Index for quick lookup of diary entries by user_id and entry_date
CREATE INDEX IF NOT EXISTS idx_diary_entries_user_date ON diary_entries(user_id, entry_date);

-- Index for quick lookup of diary entries by user_id
CREATE INDEX IF NOT EXISTS idx_user_id ON diary_entries(user_id);

-- Index for quick lookup of diary entries by entry_date
CREATE INDEX IF NOT EXISTS idx_entry_date ON diary_entries(entry_date);

ALTER TABLE diary_entries
ALTER COLUMN entry_date TYPE DATE USING entry_date::DATE;
