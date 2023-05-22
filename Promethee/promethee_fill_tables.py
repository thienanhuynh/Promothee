import sqlite3
import csv

promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
print('Database opened')
promethee_conn.execute("PRAGMA foreign_keys = 1")
promethee_cursor = promethee_conn.cursor()

##################
#0 DELETE TABLES #
##################
def delete_table(table):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor.execute(f''' DELETE FROM {table}
            '''
            )
    print(str(table) + " successfully deleted")
    promethee_cursor.close()
    promethee_conn.close()
# delete_table("Country_Author")


##################################
#0 CHECK ERRORS AND DELETE IF SO #
##################################
def manage_Errors():
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    print('Database opened')
    print('CHECK ERROR')
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    with open('BiblioPrometheeMaster_References.csv', 'r', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)
        data = list(reader)
        position = 0
        for row in data:
            authors = row[1]
            
            author_list = [authors.strip() for author in authors.split(", ") if author.split()] 
            
            size = len(author_list)
            if size % 2 == 1:
                country = row[0]
                authors = row[1]
                year = row[2]
                title = row[3]
                publisher = row[4].strip()
                volume_number = row[5].strip()
                pages = row[6].strip()
                
                dico_type = {
                    7 : 'Theory',
                    8 : 'Practice'
                }
                for type_row_position, type_choice in dico_type.items():
                    if row[type_row_position] == "1":
                        doc_type = type_choice

                dico_genre = {
                    9 : 'Water',
                    10 : 'Energy',
                    11 : 'Financial',
                    12 : 'Environment',
                    13 : 'Mining',
                    14 : 'Industrial',
                    15 : 'Services/Public',
                    16 : 'Procurement',
                    17 : 'Health',
                    18 : 'Transport',
                    19 : 'Other'
                }
                
                keywords = []
                for genre_row_position, genre_choice in dico_genre.items():
                    if row[genre_row_position] == "1":
                        keywords.append(genre_choice)
                if len(keywords) == 0:
                    keywords = "Missing"
                        
                promethee_cursor.execute(''' INSERT INTO Errors (country, authors, year, title, publisher, volume_number, pages, doc_type, keywords)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (country, authors, year, title, publisher, volume_number, pages, doc_type, str(keywords),)
                            )
            
                del data[position]
            position += 1
            
        with open('BiblioPrometheeMaster_References_corrected.csv', 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(header)
            writer.writerows(data)
    promethee_cursor.close()
    promethee_conn.close()
    print('CHECK ERROR DONE')
    print('Database closed')
       
# manage_Errors()


############################
#2 INSERT AUTHORS FROM CSV #
############################

def add_Author():
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    print('Database opened')
    print('ADD AUTHORS')
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    with open('BiblioPrometheeMaster_Authors.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            author_firstnames = row[1]
            author_firstnames_split = author_firstnames.split(' ')
            firstnames_list = []
            for firstname in author_firstnames_split:
                if '.' in firstname:
                    dot_split_name = firstname.split('.')
                    for dot_name in dot_split_name:
                        if len(dot_name) > 0:
                            firstnames_list.append(dot_name)
                else:
                    if len(firstname) > 0:
                        firstnames_list.append(firstname)
                            
            initials = [word[0].upper() for word in firstnames_list]
            author_initials = ''.join(single_initial + '.' for single_initial in initials)
            author_lastname = row[0]
            affiliation = row[2]
            country_code = row[3]
            author_email = row[4]
            promethee_cursor.execute(''' INSERT INTO Author (author_firstnames, author_initials, author_lastname, country_code, affiliation, author_email)
                        VALUES (?, ?, ?, ?, ?, ?)
                        ''', (author_firstnames, author_initials, author_lastname, country_code, affiliation, author_email)
                        )
    promethee_cursor.close()
    promethee_conn.close()
    print('ADD AUTHORS DONE')
    print('Database closed')

#add_Author()


#################
#3 INSERT GENRE #
#################

def insert_Genre(keyword):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    print('Database opened')
    print('ADD GENRES')
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    check_if_already_exists = promethee_cursor.execute("SELECT * FROM Genre WHERE keyword=?", (keyword,)).fetchall()
    if not check_if_already_exists:
        promethee_cursor.execute('''INSERT INTO Genre(keyword)
                VALUES(?)
                    ''', (keyword,)
                    )
    promethee_cursor.close()
    promethee_conn.close()
    print('ADD GENRES DONE')
    print('Database closed')

# insert_Genre("Water")
# insert_Genre("Energy")
# insert_Genre("Financial")
# insert_Genre("Environment")
# insert_Genre("Mining")
# insert_Genre("Industrial")
# insert_Genre("Services/Public")
# insert_Genre("Procurement")
# insert_Genre("Health")
# insert_Genre("Transport")
# insert_Genre("Other")


##############################
#4 INSERT PUBLISHER FROM CSV #
##############################

def add_Publisher():
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    print('Database opened')
    print('ADD PUBLISHERS')
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    with open('BiblioPrometheeMaster_References_corrected.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            publisher_name = row[4].strip()
            
            result = promethee_cursor.execute("SELECT * FROM Publisher WHERE publisher_name = ?", (publisher_name,))
            if not result.fetchone():
                promethee_cursor.execute(''' INSERT INTO Publisher (publisher_name)
                              VALUES (?)
                              ''', (publisher_name,)
                            )
    promethee_cursor.close()
    promethee_conn.close()
    print('ADD PUBLISHER DONE')
    print('Database closed')

#add_Publisher()

############################
#5 INSERT COUNTRY FROM CSV #
############################

def add_Country():
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    print('Database opened')
    print('ADD COUNTRIES')
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    with open('BiblioPrometheeMaster_Country.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) #skip header row

        for row in reader:
            country_code = row[1]
            population_in_millions = row[2]
            continent = row[0]
            researchers = row[3]
            
            promethee_cursor.execute(''' INSERT INTO Country (country_code, population_in_millions, continent, researchers)
                        VALUES (?, ?, ?, ?)
                        ''', (country_code, population_in_millions, continent, researchers)
                        )
    promethee_cursor.close()
    promethee_conn.close()
    print('ADD COUNTRIES DONE')
    print('Database closed')

#add_Country()


###############################
#6 INSERT REFERENCES FROM CSV #
###############################

def add_Reference():
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    print('Database opened')
    print('ADD REFERENCES')
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()

    with open('BiblioPrometheeMaster_References_corrected.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            title = row[3]
            publisher_name = row[4].strip()
            publisher_reference = promethee_cursor.execute("SELECT publisher_id FROM Publisher WHERE publisher_name = ?", (publisher_name,)).fetchone()[0]
            year = row[2]
            pages = row[6].strip()
            
            dico_type = {
                7 : 'Theory',
                8 : 'Practice'
            }
            for type_row_position, type_choice in dico_type.items():
                if row[type_row_position] == "1":
                    type = type_choice
            
            volume_number_isbn_issn = (row[5].strip()).split(' ')
            for word in volume_number_isbn_issn:
                str(word)
                if 'ISBN' in volume_number_isbn_issn or 'ISSN' in volume_number_isbn_issn:
                    isbn_issn = volume_number_isbn_issn[1]
                    volume = None
                    number = None
                    break
                
                elif '(' in volume_number_isbn_issn:
                    number = word[word.find('(')+1:word.find(')')]
                    volume =  word[:word.find('(')]
                    isbn_issn = None
                    break
                    
                else:
                    volume = row[5].strip() 
                    isbn_issn = None
                    number = None
                    
            promethee_cursor.execute(''' INSERT INTO Reference (title, publisher_reference, isbn_issn, year, volume, number, pages, type)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (title, publisher_reference, isbn_issn, year, volume, number, pages, type,)
                        )
    promethee_cursor.close()
    promethee_conn.close()
    print('ADD REFERENCES DONE')
    print('Database closed')


###############################
#7 LINK REFERENCES TO AUTHORS #
###############################

def link_ReferencesAuthors():    
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    print('Database opened')
    print('LINK REFERENCES TO AUTHORS')
    with open('BiblioPrometheeMaster_References_corrected.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        
        current_reference_id = 1
        for row in reader:
            current_reference_country = row[0]
            authors = row[1]
            author_list = [author.strip() for author in authors.split(",")]
            size = len(author_list)
            authors_quantity = int(size/2)
            
            position_in_list = 0
            for author_position in range(1, authors_quantity + 1):
                current_author_lastname = author_list[2*position_in_list]
                current_author_initials = author_list[2*position_in_list + 1].replace("-", "")
                
                check_author_id = promethee_cursor.execute("SELECT author_id FROM Author WHERE author_lastname = ? AND author_initials = ?", (current_author_lastname, current_author_initials)).fetchall()
                if check_author_id:
                    single_author_id = check_author_id[0][0]
                    
                    check_if_author_reference_exists = promethee_cursor.execute("SELECT * FROM Author_Reference WHERE author_id = ? AND reference_id = ?", (single_author_id, current_reference_id)).fetchall()
                    
                    if check_if_author_reference_exists:
                        print("This combination author_id = {} and reference_id = {} already exists".format(single_author_id, current_reference_id))
                    else:
                        promethee_cursor.execute(''' INSERT INTO Author_Reference (author_id, reference_id, position)
                                        VALUES (?, ?, ?)
                                            ''', (single_author_id, current_reference_id, author_position)
                                            )
                else:
                    promethee_cursor.execute(''' INSERT INTO Author (author_initials, author_lastname, country_code)
                                  VALUES (?, ?, ?)
                                  ''', (current_author_initials, current_author_lastname, current_reference_country))
                    
                    last_author_id = promethee_cursor.execute('''SELECT last_insert_rowid()''').fetchone()[0]

                    promethee_cursor.execute(''' INSERT INTO Author_Reference (author_id, reference_id, position)
                                    VALUES (?, ?, ?)
                                        ''', (last_author_id, current_reference_id, author_position)
                                        )
                position_in_list += 1
            current_reference_id += 1
    promethee_cursor.close()
    promethee_conn.close()
    print('LINK REFERENCES TO AUTHORS DONE')
    print("Database closed")


#############################
#8 LINK GENRE TO REFERENCES #
#############################
def link_GenreReferences():
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    print('Database opened')
    print('LINK GENRES TO REFERENCES')
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    with open('BiblioPrometheeMaster_References_corrected.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        
        dico_genre = {
        9 : 'Water',
        10 : 'Energy',
        11 : 'Financial',
        12 : 'Environment',
        13 : 'Mining',
        14 : 'Industrial',
        15 : 'Services/Public',
        16 : 'Procurement',
        17 : 'Health',
        18 : 'Transport',
        19 : 'Other'
        }
        
        current_reference_id = 1
        for row in reader:
            
            for genre_row_position, genre_choice in dico_genre.items():
                if row[genre_row_position] == "1":
                    current_keyword = genre_choice
                    current_keyword_id = promethee_cursor.execute("SELECT keyword_id FROM Genre WHERE keyword = ?", (current_keyword,)).fetchone()[0]
            
                    check_if_genre_reference_exists = promethee_cursor.execute("SELECT * FROM Genre_Reference WHERE keyword_id = ? AND reference_id = ?", (current_keyword_id, current_reference_id)).fetchall()
                    
                    if check_if_genre_reference_exists:
                        print("This combination genre_id = {} and reference_id = {} already exists".format(current_keyword_id, current_reference_id))
                    else:
                        promethee_cursor.execute(''' INSERT INTO Genre_Reference (keyword_id, reference_id)
                                      VALUES (?, ?)
                                      ''', (current_keyword_id, current_reference_id,)
                                      )
            current_reference_id += 1
    promethee_cursor.close()
    promethee_conn.close()
    print('Database closed')


def fill_table():
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    print('Database opened')
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    promethee_cursor.execute(''' INSERT INTO Country (country_code, population_in_millions, continent, researchers)
                VALUES (?, ?, ?, ?)
                ''', ("QA", None, "ASIA", None)
                )
    promethee_cursor.execute(''' INSERT INTO Country (country_code, population_in_millions, continent, researchers)
                VALUES (?, ?, ?, ?)
                ''', ("VN", None, "ASIA", None)
                )
    promethee_cursor.execute(''' INSERT INTO Country (country_code, population_in_millions, continent, researchers)
                VALUES (?, ?, ?, ?)
                ''', ("PG", None, "OCE", None)
                )
    promethee_cursor.execute(''' INSERT INTO Country (country_code, population_in_millions, continent, researchers)
                VALUES (?, ?, ?, ?)
                ''', ("UY", None, "SAM", None)
                )
    promethee_cursor.execute(''' INSERT INTO Country (country_code, population_in_millions, continent, researchers)
                VALUES (?, ?, ?, ?)
                ''', ("AE", None, "ASIA", None)
                )
    promethee_cursor.execute(''' INSERT INTO Country (country_code, population_in_millions, continent, researchers)
                VALUES (?, ?, ?, ?)
                ''', ("NZ", None, "OCE", None)
                )
    promethee_cursor.execute(''' INSERT INTO Country (country_code, population_in_millions, continent, researchers)
                VALUES (?, ?, ?, ?)
                ''', ("NA", None, "AFR", None)
                )
    promethee_cursor.close()
    promethee_conn.close()
    print('LINK GENRES TO REFERENCES DONE')
    print('Database closed')


# manage_Errors()

# fill_table()

# insert_Genre("Water")
# insert_Genre("Energy")
# insert_Genre("Financial")
# insert_Genre("Environment")
# insert_Genre("Mining")
# insert_Genre("Industrial")
# insert_Genre("Services/Public")
# insert_Genre("Procurement")
# insert_Genre("Health")
# insert_Genre("Transport")
# insert_Genre("Other")

# add_Author()
# add_Country()
# add_Publisher()
# add_Reference()
# link_ReferencesAuthors()
# link_GenreReferences()


# delete_table("Author")
# delete_table("Author_Reference")
# delete_table("Genre_Reference")
# delete_table("Reference")

