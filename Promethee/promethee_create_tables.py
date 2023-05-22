import sqlite3

promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
promethee_conn.execute("PRAGMA foreign_keys = 1")
promethee_cursor = promethee_conn.cursor()
print("Database opened")

#0 Errors
promethee_cursor.execute(''' CREATE TABLE IF NOT EXISTS Errors (
    error_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL,
    authors TEXT NOT NULL,
    year INT NOT NULL,
    title TEXT NOT NULL,
    publisher TEXT NOT NULL,
    volume_number TEXT,
    pages TEXT,
    doc_type TEXT NOT NULL,
    keywords TEXT
    ) ''')

#1 Author
promethee_cursor.execute(''' CREATE TABLE IF NOT EXISTS Author (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_firstnames TEXT,
    author_initials TEXT,
    author_lastname TEXT NOT NULL,
    country_code TEXT,
    affiliation TEXT,
    author_email TEXT
    ) ''')

#2 Publisher
promethee_cursor.execute(''' CREATE TABLE IF NOT EXISTS Publisher (
    publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    publisher_name TEXT NOT NULL UNIQUE
    ) ''')

#3 Reference
promethee_cursor.execute(''' CREATE TABLE IF NOT EXISTS Reference (
    reference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    publisher_reference INT,
    isbn_issn INT,
    year INT NOT NULL,
    volume TEXT,
    number TEXT,
    pages TEXT,
    type TEXT NOT NULL,
    FOREIGN KEY (publisher_reference) REFERENCES Publisher(publisher_id)
    ) ''')

#4 Country
promethee_cursor.execute(''' CREATE TABLE IF NOT EXISTS Country (
    country_code TEXT PRIMARY KEY NOT NULL,
    population_in_millions INT,
    continent TEXT NOT NULL,
    researchers INT
    ) ''')

#5 Genre
promethee_cursor.execute(''' CREATE TABLE IF NOT EXISTS Genre (
    keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL
    ) ''')

#6 Author_Reference
promethee_cursor.execute(''' CREATE TABLE IF NOT EXISTS Author_Reference (
    author_id INT NOT NULL,
    reference_id INT NOT NULL,
    position INT NOT NULL,
    PRIMARY KEY (author_id, reference_id),
    FOREIGN KEY (author_id) REFERENCES Author(author_id),
    FOREIGN KEY (reference_id) REFERENCES Reference(reference_id) 
    ) ''')

#7 Genre_Reference
promethee_cursor.execute(''' CREATE TABLE IF NOT EXISTS Genre_Reference (
    keyword_id INT NOT NULL,
    reference_id INT NOT NULL,
    PRIMARY KEY (keyword_id, reference_id),
    FOREIGN KEY (keyword_id) REFERENCES Genre(keyword_id),
    FOREIGN KEY (reference_id) REFERENCES Reference(reference_id)
    ) ''')

promethee_cursor.close()

print("Database closed")