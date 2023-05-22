from django.shortcuts import render, redirect
import sqlite3

#############
# Main page #
#############
def search(request):    
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    search_keyword = request.GET.get('search_keyword')
    search_author = request.GET.get('search_author')
    search_publisher = request.GET.get('search_publisher')

    if search_keyword:
        all_references = promethee_cursor.execute('''SELECT * FROM Reference WHERE title LIKE ? OR isbn_issn LIKE ?''', ('%{}%'.format(search_keyword), search_keyword,)).fetchall()

    elif search_author:
        all_references_ids = []
        all_authors_ids = promethee_cursor.execute('''SELECT author_id FROM Author WHERE author_lastname LIKE ?''', (search_author,)).fetchall()

        for single_author_id in all_authors_ids:
            author_id = single_author_id[0]
            all_references_ids_for_an_author = promethee_cursor.execute('''SELECT reference_id FROM Author_Reference WHERE author_id = ?''', (author_id,)).fetchall()
            
            for single_reference_id in all_references_ids_for_an_author:
                reference_id = single_reference_id[0]
                
                if reference_id not in all_references_ids: #we only add the reference_id if it's not in the list yet
                    all_references_ids.append(reference_id)
        
        all_references = []
        for reference_id in all_references_ids:
            reference = promethee_cursor.execute('''SELECT * FROM Reference WHERE reference_id = ?''', (reference_id,)).fetchone()
            all_references.append(reference)

    elif search_publisher:
        all_references_ids = []
        all_publishers_ids = promethee_cursor.execute('''SELECT publisher_id FROM Publisher WHERE publisher_name LIKE ?''', ('%{}%'.format(search_publisher),)).fetchall()
        
        for single_publisher_id in all_publishers_ids:
            publisher_id = single_publisher_id[0]
            all_references_ids_for_a_publisher = promethee_cursor.execute('''SELECT reference_id FROM Reference WHERE publisher_reference = ?''', (publisher_id,)).fetchall()
            
            for single_reference_id in all_references_ids_for_a_publisher:
                reference_id = single_reference_id[0]
                
                if reference_id not in all_references_ids:
                    all_references_ids.append(reference_id)
        
        all_references = []
        for reference_id in all_references_ids:
            reference = promethee_cursor.execute('''SELECT * FROM Reference WHERE reference_id = ?''', (reference_id,)).fetchone()
            all_references.append(reference)
                  
    else:
        all_references = promethee_cursor.execute('''SELECT * FROM Reference''').fetchall()
     
    references = []
    for row in all_references:
        reference_id = row[0]
        publisher_id = row[2]
        
        authors_id_position = promethee_cursor.execute('''SELECT author_id, position FROM Author_Reference WHERE reference_id = ?''', (reference_id,)).fetchall()
        author_informations = []
        for single_author_id_position in authors_id_position:
            single_author_id = single_author_id_position[0]
            single_author_position = single_author_id_position[1]
            author_identity = promethee_cursor.execute('''SELECT author_initials, author_lastname FROM Author WHERE author_id = ?''', (single_author_id,)).fetchall()[0]
            single_author_informations = {
                'author_id': single_author_id,
                'author_position': single_author_position,
                'author_initials': author_identity[0],
                'author_lastname': author_identity[1]
            }
            author_informations.append(single_author_informations)

        publisher_name = promethee_cursor.execute('''SELECT publisher_name FROM Publisher WHERE publisher_id = ?''', (publisher_id,)).fetchall()[0][0]

        genre_ids = promethee_cursor.execute('''SELECT keyword_id FROM Genre_Reference WHERE reference_id = ?''', (reference_id,)).fetchall()
        genres_list = []
        for single_genre_id in genre_ids:
            genre_id = single_genre_id[0]
            genres = promethee_cursor.execute('''SELECT keyword FROM Genre WHERE keyword_id = ?''', (genre_id,)).fetchall()
            for single_genre in genres:
                keyword = single_genre[0]
                genres_list.append(keyword)

        reference = {
            "reference_id": row[0],
            "title": row[1],
            "publisher_id": row[2],
            "publisher_name": publisher_name,
            "isbn_issn": row[3],
            "year": row[4],
            "volume": row[5],
            "number": row[6],
            "pages": row[7],
            "type": row[8],
            "authors": author_informations,
            "genres": genres_list
        }
        references.append(reference)
        
    references_quantity = len(references)

    dictionary = {
        'references': references,
        'search_keyword': search_keyword,
        'search_publisher': search_publisher,
        'search_author': search_author,
        'references_quantity': references_quantity
        }
    promethee_cursor.close()
    promethee_conn.close()
    return render(request, 'main_page.html', dictionary)


##########################
# REFERENCE DETAILS PAGE #
##########################
def reference_detail(request, reference_id): #it takes reference_id from URL
    promethee_conn = sqlite3.connect('promethee_project.db')
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()

    genre_ids = promethee_cursor.execute('''SELECT keyword_id FROM Genre_Reference WHERE reference_id = ?''', (reference_id,)).fetchall()
    genres = []
    for single_genre in genre_ids:
        genre_name = promethee_cursor.execute('''SELECT keyword FROM Genre WHERE keyword_id = ?''', (single_genre[0],)).fetchall()[0][0]
        genres.append(genre_name) 

    authors_id_position = promethee_cursor.execute('''SELECT author_id, position FROM Author_Reference WHERE reference_id = ?''', (reference_id,)).fetchall()
    author_informations = []
    for single_author_id_position in authors_id_position:
        single_author_id = single_author_id_position[0]
        single_author_position = single_author_id_position[1]
        author_identity = promethee_cursor.execute('''SELECT author_initials, author_lastname FROM Author WHERE author_id = ?''', (single_author_id,)).fetchall()[0]
        single_author_informations = {
            'author_id': single_author_id,
            'author_position': single_author_position,
            'author_initials': author_identity[0],
            'author_lastname': author_identity[1]
        }
        author_informations.append(single_author_informations)

    reference_information = promethee_cursor.execute('''SELECT reference_id, title, publisher_reference, isbn_issn, year, volume, number, pages, type FROM Reference WHERE reference_id = ?''', (reference_id,)).fetchall()

    for single_information in reference_information:
        publisher_id = single_information[2]
        publisher_name = promethee_cursor.execute('''SELECT publisher_name FROM Publisher WHERE publisher_id = ?''', (publisher_id,)).fetchall()[0][0]
        
        informations = {
        "reference_id": single_information[0],
        "title": single_information[1],
        "authors": author_informations,
        "publisher_id": single_information[2],
        "publisher_name": publisher_name,
        "isbn_issn": single_information[3],
        "year": single_information[4],
        "volume": single_information[5],
        "number": single_information[6],
        "pages": single_information[7],
        "type": single_information[8],
        "genres": genres
        }
        
    dictionary = {
        'informations': informations,
        'reference_id': reference_id
        }
    promethee_cursor.close()
    promethee_conn.close()
    return render(request, 'reference_detail.html', dictionary)

##########################
# PUBLISHER DETAILS PAGE #
##########################
def publisher_detail(request, publisher_id):
    promethee_conn = sqlite3.connect('promethee_project.db')
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    publisher_name = promethee_cursor.execute('''SELECT publisher_name FROM Publisher WHERE publisher_id = ?''', (publisher_id,)).fetchall()[0][0]

    all_references = promethee_cursor.execute('''SELECT reference_id, title, year, volume, number, pages, type FROM Reference WHERE publisher_reference = ?''', (publisher_id,)).fetchall()
    
    references = []
    for single_reference in all_references:
        reference_id = single_reference[0]
        author_ids = promethee_cursor.execute('''SELECT author_id FROM Author_Reference WHERE reference_id = ?''', (reference_id,)).fetchall()
        authors_list = []
        
        for single_author_id in author_ids:
            authors = promethee_cursor.execute('''SELECT author_initials, author_lastname FROM Author WHERE author_id = ?''', (reference_id,)).fetchall()
            for single_author in authors:
                author = {
                    'author_id': single_author_id[0],
                    'author_initials': single_author[0],
                    'author_lastname': single_author[1]
                }
                authors_list.append(author)
        genre_ids = promethee_cursor.execute('''SELECT keyword_id FROM Genre_Reference WHERE reference_id = ?''', (reference_id,)).fetchall()
        genres_list = []
        for single_genre_id in genre_ids:
            genre_id = single_genre_id[0]
            genres = promethee_cursor.execute('''SELECT keyword FROM Genre WHERE keyword_id = ?''', (genre_id,)).fetchall()
            for single_genre in genres:
                keyword = single_genre[0]
                genres_list.append(keyword)
            
        reference = {
            "reference_id": single_reference[0],
            "title": single_reference[1],
            "year": single_reference[2],
            "volume": single_reference[3],
            "number": single_reference[4],
            "pages": single_reference[5],
            "type": single_reference[6],
            "authors": authors_list,
            "genres": genres_list
            }
        references.append(reference)
    
    references_quantity = len(references)
    
    dictionary = {
        'publisher_name': publisher_name,
        'references': references,
        'references_quantity': references_quantity,
        'publisher_id': publisher_id
        }
    promethee_cursor.close()
    promethee_conn.close()
    return render(request, 'publisher_detail.html', dictionary)

########################
# AUTHOR DETAILS PAGES #
########################
def author_detail(request, author_id):
    promethee_conn = sqlite3.connect('promethee_project.db')
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()

    all_informations = promethee_cursor.execute('''SELECT author_firstnames, author_initials, author_lastname, country_code, affiliation, author_email FROM Author WHERE author_id = ?''', (author_id,)).fetchall()[0]
    author_informations = {
        'author_firstnames': all_informations[0],
        'author_initials':all_informations[1],
        'author_lastname': all_informations[2],
        'country_code': all_informations[3],
        'affiliation': all_informations[4],
        'author_email': all_informations[5]
    }

    country_code = all_informations[3]
    country_informations = promethee_cursor.execute('''SELECT population_in_millions, continent, researchers FROM Country WHERE country_code = ?''', (country_code,)).fetchall()[0]
    country_infos = {
        'population_in_millions': country_informations[0],
        'continent': country_informations[1],
        'researchers': country_informations[2]
    }

    reference_ids = promethee_cursor.execute('''SELECT reference_id FROM Author_Reference WHERE author_id = ?''', (author_id,)).fetchall()
    references = []
    
    for single_reference_id in reference_ids:
        reference_id = single_reference_id[0]
        genre_ids = promethee_cursor.execute('''SELECT keyword_id FROM Genre_Reference WHERE reference_id = ?''', (reference_id,)).fetchall()
        genres_list = []
        
        for single_genre_id in genre_ids:
            genre_id = single_genre_id[0]
            genres = promethee_cursor.execute('''SELECT keyword FROM Genre WHERE keyword_id = ?''', (genre_id,)).fetchall()
            for single_genre in genres:
                genres_list.append(single_genre[0])

        authors_id_position = promethee_cursor.execute('''SELECT author_id, position FROM Author_Reference WHERE reference_id = ?''', (reference_id,)).fetchall()
        all_authors_informations = []
        for single_author_id_position in authors_id_position:
            single_author_id = single_author_id_position[0]
            single_author_position = single_author_id_position[1]
            author_identity = promethee_cursor.execute('''SELECT author_initials, author_lastname FROM Author WHERE author_id = ?''', (single_author_id,)).fetchall()[0]
            single_author_informations = {
                'author_id': single_author_id,
                'author_position': single_author_position,
                'author_initials': author_identity[0],
                'author_lastname': author_identity[1]
            }
            all_authors_informations.append(single_author_informations)

        single_reference = promethee_cursor.execute('''SELECT title, publisher_reference, year, volume, number, pages, type FROM Reference WHERE reference_id = ?''', (single_reference_id[0],)).fetchall()
        for information in single_reference:
            reference_id = single_reference_id[0]
            publisher_id = information[1]
            publisher_name = promethee_cursor.execute('''SELECT publisher_name FROM Publisher WHERE publisher_id = ?''', (publisher_id,)).fetchall()[0][0]
            reference ={
                'reference_id': reference_id,
                'title': information[0],
                'publisher_id': publisher_id,
                'publisher_name': publisher_name,
                'year': information[2],
                'volume': information[3],
                'number': information[4],
                'pages': information[5],
                'type': information[6],
                'genres': genres_list,
                'authors': all_authors_informations
            }
        references.append(reference)
    
    references_quantity = len(references)
    
    dictionary = {
        'author_informations': author_informations,
        'country_infos': country_infos,
        'references': references,
        'author_id': author_id,
        'references_quantity': references_quantity
        }
    promethee_cursor.close()
    promethee_conn.close()
    return render(request, 'author_detail.html', dictionary)

#################
# GENRE SECTION #
#################
def genres(request):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    all_genres = promethee_cursor.execute('''SELECT keyword_id, keyword FROM Genre ORDER BY keyword ASC''').fetchall()
    genres = []
    for single_genre in all_genres:
        genre = {
            'keyword_id': single_genre[0],
            'keyword': single_genre[1]
        }
        genres.append(genre)
        
    searched_keyword_id = request.GET.get('choice') #return keyword_id
    if searched_keyword_id:
        choice_name = promethee_cursor.execute('''SELECT keyword FROM Genre WHERE keyword_id = ?''', (searched_keyword_id,)).fetchall()[0][0]
     
        references_ids = promethee_cursor.execute('''SELECT reference_id FROM Genre_Reference WHERE keyword_id = ?''', (searched_keyword_id,)).fetchall()
        
        references_ids_list = [] #We will store all references_ids link to the keyword_id chosen
        references = [] #We store reference informations based on each reference_id
        for single_reference_id in references_ids:
            reference_id = single_reference_id[0]
            references_ids_list.append(reference_id)

            authors_id_position = promethee_cursor.execute('''SELECT author_id, position
                                                           FROM Author_Reference
                                                           WHERE reference_id = ?''', (reference_id,)).fetchall()
            
            author_informations = []
            for single_author_id_position in authors_id_position:
                single_author_id = single_author_id_position[0]
                single_author_position = single_author_id_position[1]
                author_identity = promethee_cursor.execute('''SELECT author_initials, author_lastname
                                                           FROM Author
                                                           WHERE author_id = ?''', (single_author_id,)).fetchall()[0]
                
                single_author_informations = {
                    'author_id': single_author_id,
                    'author_position': single_author_position,
                    'author_initials': author_identity[0],
                    'author_lastname': author_identity[1]
                    }
                author_informations.append(single_author_informations)

            specific_reference = promethee_cursor.execute('''SELECT *
                                                          FROM Reference
                                                          WHERE reference_id = ?''', (reference_id,)).fetchall()[0]
            publisher_id = specific_reference[2]
            publisher_name = promethee_cursor.execute('''SELECT publisher_name
                                                      FROM Publisher
                                                      WHERE publisher_id = ?''', (publisher_id,)).fetchall()[0][0]
            reference = {
                "reference_id": specific_reference[0],
                "title": specific_reference[1],
                "publisher_id": specific_reference[2],
                "publisher_name": publisher_name,
                "isbn_issn": specific_reference[3],
                "year": specific_reference[4],
                "volume": specific_reference[5],
                "number": specific_reference[6],
                "pages": specific_reference[7],
                "type": specific_reference[8],
                "authors": author_informations
                }
            references.append(reference)
            
        references_quantity = len(references)
            
        dictionary = {
            'genres': genres,
            'searched_keyword_id': searched_keyword_id,
            'references': references,
            'choice_name': choice_name,
            'references_quantity': references_quantity
            }
        promethee_cursor.close()
        promethee_conn.close()
        return render(request, 'genres.html', dictionary)
    
    if request.method == "POST":
        new_genre = request.POST.get('new_genre')
        check_if_exists_already = promethee_cursor.execute('''SELECT keyword
                                                           FROM Genre
                                                           WHERE keyword LIKE ?''', (new_genre,)).fetchall()
        
        if check_if_exists_already:
            error = f"{new_genre} already exists in the database"
            dictionary = {
                'genres': genres,
                'searched_keyword_id': searched_keyword_id,
                'new_genre': new_genre,
                'error': error
                }
            promethee_cursor.close()
            promethee_conn.close()
            return render(request, 'genres.html', dictionary)
        
        else:
            promethee_cursor.execute('''INSERT INTO Genre (keyword)
                                    VALUES (?)''', (new_genre,))
            promethee_cursor.close()
            promethee_conn.close()
            return redirect ('/genres')
    dictionary = {
        'genres': genres,
        'searched_keyword_id': searched_keyword_id
        }
    promethee_cursor.close()
    promethee_conn.close()
    return render(request, 'genres.html', dictionary)

###################
# COUNTRY SECTION #
###################
def country_detail(request):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    all_countries = promethee_cursor.execute('''SELECT country_code, population_in_millions, continent, researchers
                                             FROM Country
                                             ORDER BY country_code ASC''').fetchall()
    countries = []
    for single_country in all_countries:
        country = {
            'country_code': single_country[0],
            'population_in_millions': single_country[1],
            'continent': single_country[2],
            'researchers': single_country[3]
        }
        
        countries.append(country)

    searched_country_code = request.GET.get('choice') #return country_code
    show_update_form = request.GET.get('update_form')
    if searched_country_code:

        if not show_update_form:
            all_authors_for_country = promethee_cursor.execute('''SELECT author_id, author_firstnames, author_initials, author_lastname, affiliation, author_email
                                                FROM Author
                                                WHERE country_code = ?''', (searched_country_code,)).fetchall()
            authors_informations = []
            for single_information in all_authors_for_country:
                single_author_informations = {
                    'author_id': single_information[0],
                    'author_firstnames': single_information[1],
                    'author_initials': single_information[2],
                    'author_lastname': single_information[3],
                    'affiliation': single_information[4],
                    'author_email': single_information[5]
                }
                authors_informations.append(single_author_informations)
            
            authors_quantity = len(authors_informations)
                
            dictionary = {
                'searched_country_code': searched_country_code,
                'countries': countries,
                'authors_informations': authors_informations,
                'authors_quantity': authors_quantity
                }
            promethee_cursor.close()
            promethee_conn.close()
            return render(request, 'country_detail.html', dictionary)

        elif show_update_form:
            country_informations = promethee_cursor.execute('''SELECT country_code, population_in_millions, continent, researchers
                                                            FROM Country
                                                            WHERE country_code = ?''', (searched_country_code,)).fetchone()
            country_details = {
                'country_code': country_informations[0],
                'population_in_millions': country_informations[1],
                'continent': country_informations[2],
                'researchers': country_informations[3]
            }

            if request.method == "POST":
                updated_country_code = request.POST.get('updated_country_code')
                updated_population_in_millions = request.POST.get('updated_population_in_millions')
                updated_continent = request.POST.get('updated_continent')
                updated_researchers = request.POST.get('updated_researchers')
                print(updated_country_code)
                print(updated_population_in_millions)
                print(updated_continent)
                print(updated_researchers)
                
                promethee_cursor.execute('''UPDATE Country
                                    SET country_code = ?, population_in_millions = ?, continent = ?, researchers = ?
                                    WHERE country_code = ?''',
                        (updated_country_code, updated_population_in_millions, updated_continent, updated_researchers, searched_country_code))
                
                return redirect('/countries?choice={}'.format(updated_country_code))
            
            dictionary = {
                'country_details': country_details,
                'show_update_form': show_update_form,
                'countries': countries
            }
            return render(request, 'country_detail.html', dictionary)

    if request.method == "POST":
        new_country_code = request.POST.get('new_country_code')
        new_population_in_millions = request.POST.get('new_population_in_millions')
        new_continent = request.POST.get('new_continent')
        new_researchers = request.POST.get('new_researchers')
        check_if_exists_already = promethee_cursor.execute('''SELECT country_code
                                                           FROM Country
                                                           WHERE country_code = ?''', (new_country_code,)).fetchall()

        if check_if_exists_already:
            error = f"{new_country_code} already exists in the database"
            dictionary = {
                'searched_country_code': searched_country_code,
                'countries': countries,
                'error': error
                }
            promethee_cursor.close()
            promethee_conn.close()
            return render(request, 'country_detail.html', dictionary)
        
        else:
            promethee_cursor.execute('''INSERT INTO Country (country_code, population_in_millions, continent, researchers)
                                    VALUES (?, ?, ?, ?)''', (new_country_code, new_population_in_millions, new_continent, new_researchers,))
            promethee_cursor.close()
            promethee_conn.close()
            return redirect ('/countries?choice={}'.format(new_country_code))
    dictionary = {
        'countries': countries,
        'searched_country_code': searched_country_code,
        'show_update_form': show_update_form
        }
    promethee_cursor.close()
    promethee_conn.close()
    return render(request, 'country_detail.html', dictionary)

def add_reference(request):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    authors_count = request.GET.get('authors_count')

    all_authors = promethee_cursor.execute('''SELECT author_id, author_firstnames, author_initials,
                                           author_lastname, country_code, affiliation, author_email
                                           FROM Author
                                           ORDER BY author_lastname ASC''').fetchall()
    authors = []
    for single_author in all_authors:
        author = {
            'author_id': single_author[0],
            'author_firstnames': single_author[1],
            'author_initials': single_author[2],
            'author_lastname': single_author[3],
            'country_code': single_author[4],
            'affiliation': single_author[5],
            'author_email': single_author[6]
        }
        authors.append(author)

    all_publishers = promethee_cursor.execute('''SELECT publisher_id, publisher_name
                                              FROM Publisher
                                              ORDER BY publisher_name ASC''').fetchall()
    publishers = []
    for single_publisher in all_publishers:
        publisher = {
            'publisher_id': single_publisher[0],
            'publisher_name': single_publisher[1]
        }
        publishers.append(publisher)

    all_genres = promethee_cursor.execute('''SELECT keyword_id, keyword
                                          FROM Genre
                                          ORDER BY keyword ASC''').fetchall()
    genres = []
    for single_genre in all_genres:
        genre = {
            'keyword_id': single_genre[0],
            'keyword': single_genre[1]
        }
        genres.append(genre)

    if authors_count and not request.method == 'POST':
        loop = range(1, int(authors_count)+1)
        dictionary = {
            'authors': authors,
            'publishers': publishers,
            'genres': genres,
            'authors_count': authors_count,
            'loop': loop
            }
        promethee_cursor.close()
        promethee_conn.close()
        return render(request, 'add_reference.html', dictionary)

    if request.method == 'POST' and authors_count:
        title = request.POST.get('title')
        publisher_select_id = request.POST.get('publisher_select')
        isbn_issn = request.POST.get('isbn_issn')
        year = request.POST.get('year')
        volume = request.POST.get('volume')
        number = request.POST.get('number')
        pages = request.POST.get('pages')
        type = request.POST.get('type')
        selected_genres_ids = request.POST.getlist('selected_genres')
        
        publisher_id = publisher_select_id
        promethee_cursor.execute('''INSERT INTO Reference (title, publisher_reference, isbn_issn, year, volume, number, pages, type)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                    (title, publisher_id, isbn_issn, year, volume, number, pages, type))
        reference_id = promethee_cursor.execute('''SELECT last_insert_rowid()''').fetchone()[0]

        i = 1
        loop = range(1, int(authors_count)+1) #as many loop as we have authors
        authors_ids_and_position = []
        for position in loop: #as long as there is another author
            author_id = request.POST.get('selected_author{}'.format(i)) #to retrieve value from a QueryDict
            single_author_id_and_position = {
                'author_id': int(author_id),
                'position': position
                }
            authors_ids_and_position.append(single_author_id_and_position)
            i += 1
        
        for author_id_and_position in authors_ids_and_position:
            single_author_id = author_id_and_position['author_id']
            single_author_position = author_id_and_position['position']
            promethee_cursor.execute('''INSERT INTO Author_Reference (author_id, reference_id, position)
                                        VALUES (?, ?, ?)''',
                                        (single_author_id, reference_id, single_author_position))

        for single_genre_id in selected_genres_ids:
            promethee_cursor.execute('''INSERT INTO Genre_Reference (keyword_id, reference_id)
                                VALUES (?, ?)''',
                                (single_genre_id, reference_id))
            promethee_cursor.close()
            promethee_conn.close()
            return redirect('/reference/{}'.format(reference_id))
        
    else:
        dictionary = {
            'authors': authors,
            'publishers': publishers,
            'genres': genres
            }
        promethee_cursor.close()
        promethee_conn.close()
        return render(request, 'add_reference.html', dictionary)

#####################
# ADD NEW PUBLISHER #
#####################
def add_publisher(request):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    all_publishers = promethee_cursor.execute('''SELECT publisher_id, publisher_name
                                              FROM Publisher
                                              ORDER BY publisher_name ASC''').fetchall()
    publishers = []
    for single_publisher in all_publishers:
        publisher = {
            'publisher_id': single_publisher[0],
            'publisher_name': single_publisher[1]  
        }
        publishers.append(publisher)

    if request.method == 'POST':
        new_publisher_name = request.POST.get('new_publisher_name')
        check_if_already_exists = promethee_cursor.execute('''SELECT publisher_name
                                                           FROM Publisher
                                                           WHERE publisher_name = ?''', (new_publisher_name,)).fetchall()

        if check_if_already_exists:
            error = f"{new_publisher_name} already exists"
            dictionary = {
                'publishers': publishers,
                'error': error
                }
            promethee_cursor.close()
            promethee_conn.close()
            return render(request, 'add_publisher.html', dictionary)
        
        else:
            promethee_cursor.execute(''' INSERT INTO Publisher (publisher_name)
                            VALUES (?)''',
                            (new_publisher_name,))
            
            publisher_id = promethee_cursor.execute('''SELECT last_insert_rowid()''').fetchone()[0]
            
            return redirect('/publisher/{}'.format(publisher_id))
        
    dictionary = {
        'publishers': publishers
        }
    promethee_cursor.close()
    promethee_conn.close()
    return render(request, 'add_publisher.html', dictionary)

##################
# ADD NEW AUTHOR #
##################
def add_author(request):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()

    all_authors = promethee_cursor.execute('''SELECT author_id, author_firstnames, author_initials,
                                           author_lastname, country_code, affiliation, author_email
                                           FROM Author
                                           ORDER BY author_lastname ASC''').fetchall()
    authors = []
    for single_author in all_authors:
        author = {
            'author_id': single_author[0],
            'author_firstnames': single_author[1],
            'author_initials': single_author[2],
            'author_lastname': single_author[3],
            'country_code': single_author[4],
            'affiliation': single_author[5],
            'author_email': single_author[6]
        }
        authors.append(author)

    if request.method == 'POST':
        firstnames = request.POST.get('firstnames')
        lastname = request.POST.get('lastname')
        country_code = request.POST.get('country_code')
        affiliation = request.POST.get('affiliation')
        email = request.POST.get('email')

        firstnames_split = firstnames.split(' ')
        firstnames_list = []
        for firstname in firstnames_split:
            if '.' in firstnames_split:
                dot_split_name = firstnames_split.split('.')
                for dot_name in dot_split_name:
                    if len(dot_name) > 0:
                        firstnames_list.append(dot_name)
            else:
                if len(firstname) > 0:
                    firstnames_list.append(firstname)
        initials = [word[0].upper() for word in firstnames_list]
        author_initials = ''.join(single_initial + '.' for single_initial in initials)
        
        check_if_author_already_exists = promethee_cursor.execute('''SELECT author_id FROM Author
                                                                  WHERE author_firstnames = ? AND author_initials = ? AND author_lastname = ?
                                                                  AND country_code = ? AND  affiliation = ? AND author_email = ?''',
                                                                  (firstnames, author_initials, lastname, country_code, affiliation, email,)).fetchall()

        if check_if_author_already_exists:
            error = "This author already exists in the database"
            dictionary = {
                'authors': authors,
                'error': error
                }
            promethee_cursor.close()
            promethee_conn.close()
            return render(request, 'add_author.html', dictionary)
        
        else:
            promethee_cursor.execute('''INSERT INTO Author (author_firstnames, author_initials,
                                    author_lastname, country_code, affiliation, author_email)
                                    VALUES (?, ?, ?, ?, ?, ?)''',
                                    (firstnames, author_initials, lastname, country_code, affiliation, email))
            
            author_id = promethee_cursor.execute('''SELECT last_insert_rowid()''').fetchone()[0]

            check_country_code = promethee_cursor.execute('''SELECT country_code
                                                        FROM Country
                                                        WHERE country_code = ?''', (country_code,)).fetchall()
            if not check_country_code:
                promethee_cursor.execute('''INSERT INTO Author (author_firstnames, author_intials,
                                        author_lastname, country_code, affiliation, author_email)
                                    VALUES (?, ?, ?, ?, ?, ?)''', (firstnames, lastname, author_initials, country_code, affiliation, email))
            promethee_cursor.close()
            promethee_conn.close()
            return redirect('/author/{}'.format(author_id))
    
    dictionary = {
        'authors': authors,
        }
    promethee_cursor.close()
    promethee_conn.close()
    return render(request, 'add_author.html', dictionary)

####################
# UPDATE REFERENCE #
####################
def update_reference(request, reference_id):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()

    all_authors = promethee_cursor.execute('''SELECT author_id, author_firstnames, author_initials,
                                           author_lastname, country_code, affiliation, author_email
                                           FROM Author
                                           ORDER BY author_lastname ASC''').fetchall()
    authors = []
    for single_author in all_authors:
        author = {
            'author_id': single_author[0],
            'author_firstnames': single_author[1],
            'author_initials': single_author[2],
            'author_lastname': single_author[3],
            'country_code': single_author[4],
            'affiliation': single_author[5],
            'author_email': single_author[6]
        }
        authors.append(author)

    all_publishers = promethee_cursor.execute('''SELECT publisher_id, publisher_name
                                              FROM Publisher
                                              ORDER BY publisher_name ASC''').fetchall()
    publishers = []
    for single_publisher in all_publishers:
        publisher = {
            'publisher_id': single_publisher[0],
            'publisher_name': single_publisher[1]
        }
        publishers.append(publisher)

    genres = promethee_cursor.execute('''SELECT keyword_id, keyword
                                      FROM Genre
                                      ORDER BY keyword ASC''').fetchall()
    all_genres = []
    for single_genre in genres:
        genre = {
            'keyword_id': single_genre[0],
            'keyword': single_genre[1]
        }
        all_genres.append(genre)

    genre_ids = promethee_cursor.execute('''SELECT keyword_id
                                         FROM Genre_Reference
                                         WHERE reference_id = ?''', (reference_id,)).fetchall()
    specific_genres = []
    for single_genre_id in genre_ids:
        genre_name = promethee_cursor.execute('''SELECT keyword
                                              FROM Genre
                                              WHERE keyword_id = ?''', (single_genre_id[0],)).fetchall()[0][0]
        single_genre = {
            'genre_id': single_genre_id[0],
            'genre_name': genre_name
        }
        specific_genres.append(single_genre)

    authors_id_position = promethee_cursor.execute('''SELECT author_id, position
                                                   FROM Author_Reference
                                                   WHERE reference_id = ?''', (reference_id,)).fetchall()
    author_informations = []
    for single_author_id_position in authors_id_position:
        single_author_id = single_author_id_position[0]
        single_author_position = single_author_id_position[1]
        author_identity = promethee_cursor.execute('''SELECT author_firstnames, author_initials, author_lastname, country_code, affiliation, author_email
                                                   FROM Author
                                                   WHERE author_id = ?''', (single_author_id,)).fetchall()[0]
        single_author_informations = {
            'author_id': single_author_id,
            'author_position': single_author_position,
            'author_firstnames': author_identity[0],
            'author_initials': author_identity[1],
            'author_lastname': author_identity[2],
            'author_country_code': author_identity[3],
            'author_affiliation': author_identity[4],
            'author_email': author_identity[5]
        }
        author_informations.append(single_author_informations)

    current_reference = promethee_cursor.execute('''SELECT reference_id, title, publisher_reference, isbn_issn, year, volume, number, pages, type
                                                 FROM Reference
                                                 WHERE reference_id = ?''', (reference_id,)).fetchall()[0]

    publisher_name = promethee_cursor.execute('''SELECT publisher_name
                                              FROM Publisher
                                              WHERE publisher_id = ?''', (current_reference[2],)).fetchall()[0][0]
    
    informations = {
    "reference_id": current_reference[0],
    "title": current_reference[1],
    "authors": author_informations,
    "publisher_id": current_reference[2],
    "publisher_name": publisher_name,
    "isbn_issn": current_reference[3],
    "year": current_reference[4],
    "volume": current_reference[5],
    "number": current_reference[6],
    "pages": current_reference[7],
    "type": current_reference[8],
    "genres": specific_genres
    }

    if request.method == "POST":
        new_title = request.POST.get('new_title')
        new_publisher_selected = int(request.POST.get('new_publisher_selected'))
        new_isbn_issn = request.POST.get('new_isbn_issn')
        new_year = request.POST.get('new_year')
        new_volume = request.POST.get('new_volume')
        new_number = request.POST.get('new_number')
        new_pages = request.POST.get('new_pages')
        new_type = request.POST.get('new_type')

        promethee_cursor.execute('''UPDATE Reference
                                 SET title = ?, publisher_reference = ?, isbn_issn = ?, year = ?, volume = ?, number = ?, pages = ?, type = ?
                                 WHERE reference_id = ?''',
                        (new_title, new_publisher_selected, new_isbn_issn, new_year, new_volume, new_number, new_pages, new_type, reference_id))

        i = 1
        loop_size = len(author_informations)
        loop = range(1, loop_size+1)
        
        authors_ids_and_position = []
        for position in loop: #as long as there is another author
            new_author_id = request.POST.get('selected_author{}'.format(i)) #to retrieve value from a QueryDict
            single_author_id_and_position = {
                'author_id': int(new_author_id),
                'position': position
                }
            authors_ids_and_position.append(single_author_id_and_position)
            i += 1
            promethee_cursor.execute('''UPDATE Author_Reference
                                     SET author_id = ?, reference_id = ?, position = ?
                                     WHERE reference_id = ? AND position = ?''',
                    (new_author_id, reference_id, position, reference_id, position))

        selected_genres_ids = request.POST.getlist('new_selected_genres')
        promethee_cursor.execute('''DELETE FROM Genre_Reference
                                 WHERE reference_id = ?''', (reference_id,))
        
        for single_genre_id in selected_genres_ids:
            promethee_cursor.execute('''INSERT INTO Genre_Reference (keyword_id, reference_id)
                                VALUES (?, ?)''', (single_genre_id, reference_id))
        promethee_cursor.close()
        promethee_conn.close()
        return redirect('/reference/{}'.format(reference_id))

    dictionary = {
    'informations': informations,
    'specific_genres': specific_genres,
    'authors_informations': author_informations,
    'authors': authors, 'all_genres': all_genres,
    'reference_id': reference_id,
    'publishers': publishers
    }
    promethee_cursor.close()
    promethee_conn.close()
    return render(request, 'update_reference.html', dictionary)

####################
# UPDATE PUBLISHER #
####################
def update_publisher(request, publisher_id):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    publisher_name = promethee_cursor.execute('''SELECT publisher_name
                                              FROM Publisher
                                              WHERE publisher_id = ?''', (publisher_id,)).fetchall()[0][0]

    if request.method == "POST":
        new_publisher_name = request.POST.get('new_publisher_name')

        promethee_cursor.execute('''UPDATE Publisher
                                 SET publisher_name = ?
                                 WHERE publisher_id = ?''',
                                 (new_publisher_name, publisher_id))
        promethee_cursor.close()
        promethee_conn.close()
        return redirect('/publisher/{}'.format(publisher_id))

    dictionary = {
        'publisher_name': publisher_name
    }
    promethee_cursor.close()
    promethee_cursor.close()
    return render(request, 'update_publisher.html', dictionary)

#################
# UPDATE AUTHOR #
#################
def update_author(request, author_id):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()

    all_informations = promethee_cursor.execute('''SELECT author_firstnames, author_initials, author_lastname, country_code, affiliation, author_email
                                                FROM Author
                                                WHERE author_id = ?''', (author_id,)).fetchall()[0]
    author_informations = {
        'author_firstnames': all_informations[0],
        'author_initials':all_informations[1],
        'author_lastname': all_informations[2],
        'country_code': all_informations[3],
        'affiliation': all_informations[4],
        'author_email': all_informations[5]
    }
    
    country_code = all_informations[3]
    country_informations = promethee_cursor.execute('''SELECT population_in_millions, continent, researchers
                                                    FROM Country
                                                    WHERE country_code = ?''', (country_code,)).fetchall()[0]
    country_infos = {
        'population_in_millions': country_informations[0],
        'continent': country_informations[1],
        'researchers': country_informations[2]
    }

    if request.method == "POST":
        new_firstnames = request.POST.get('new_firstnames')
        new_lastname = request.POST.get('new_lastname')
        new_country_code = request.POST.get('new_country_code')
        new_affiliation = request.POST.get('new_affiliation')
        new_email = request.POST.get('new_email')

        new_firstnames_split = new_firstnames.split(' ')
        firstnames_list = []
        for firstname in new_firstnames_split:
            if '.' in new_firstnames_split:
                dot_split_name = new_firstnames_split.split('.')
                for dot_name in dot_split_name:
                    if len(dot_name) > 0:
                        firstnames_list.append(dot_name)
            else:
                if len(firstname) > 0:
                    firstnames_list.append(firstname)
        initials = [word[0].upper() for word in firstnames_list]
        author_initials = ''.join(single_initial + '.' for single_initial in initials)

        promethee_cursor.execute('''UPDATE Author
                                 SET author_firstnames = ?, author_initials = ?, author_lastname = ?, country_code = ?, affiliation = ?, author_email = ?
                                 WHERE author_id = ?''',
                                 (new_firstnames, author_initials, new_lastname, new_country_code, new_affiliation, new_email, author_id))
        promethee_cursor.close()
        promethee_conn.close()
        return redirect('/author/{}'.format(author_id))
    
    dictionary = {
        'author_informations': author_informations,
        'country_infos': country_infos
        }
    promethee_cursor.close()
    promethee_cursor.close()
    return render(request, 'update_author.html', dictionary)

######################
# DELETE A REFERENCE #
######################
def delete_reference(request, reference_id):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    promethee_cursor.execute('''DELETE FROM Author_Reference
                             WHERE reference_id = ?''',(reference_id,))
    promethee_cursor.execute('''DELETE FROM Genre_Reference
                             WHERE reference_id = ?''',(reference_id,))
    promethee_cursor.execute('''DELETE FROM Reference
                             WHERE reference_id = ?''',(reference_id,))
    
    promethee_cursor.close()
    promethee_conn.close()
    return redirect('/search')

####################
# DELETE PUBLISHER #
####################
def delete_publisher(request, publisher_id):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()
    
    publisher_name = promethee_cursor.execute('''SELECT publisher_name
                                              FROM Publisher
                                              WHERE publisher_id = ?''', (publisher_id,)).fetchall()[0][0]

    all_references = promethee_cursor.execute('''SELECT reference_id, title, year, volume, number, pages, type
                                              FROM Reference
                                              WHERE publisher_reference = ?''', (publisher_id,)).fetchall()
    
    references = []
    for single_reference in all_references:
        reference_id = single_reference[0]
        author_ids = promethee_cursor.execute('''SELECT author_id
                                              FROM Author_Reference
                                              WHERE reference_id = ?''', (reference_id,)).fetchall()
        authors_list = []
        for single_author_id in author_ids:
            authors = promethee_cursor.execute('''SELECT author_initials, author_lastname
                                               FROM Author 
                                               WHERE author_id = ?''', (reference_id,)).fetchall()
            for single_author in authors:
                author = {
                    'author_id': single_author_id[0],
                    'author_initials': single_author[0],
                    'author_lastname': single_author[1]
                }
                authors_list.append(author)
        genre_ids = promethee_cursor.execute('''SELECT keyword_id
                                             FROM Genre_Reference
                                             WHERE reference_id = ?''', (reference_id,)).fetchall()
        genres_list = []
        for single_genre_id in genre_ids:
            genre_id = single_genre_id[0]
            genres = promethee_cursor.execute('''SELECT keyword
                                              FROM Genre
                                              WHERE keyword_id = ?''', (genre_id,)).fetchall()
            for single_genre in genres:
                keyword = single_genre[0]
                genres_list.append(keyword)
            
        reference = {
            "reference_id": single_reference[0],
            "title": single_reference[1],
            "year": single_reference[2],
            "volume": single_reference[3],
            "number": single_reference[4],
            "pages": single_reference[5],
            "type": single_reference[6],
            "authors": authors_list,
            "genres": genres_list
            }
        references.append(reference)
    
    references_quantity = len(references)

    check_if_publisher_has_references = promethee_cursor.execute('''SELECT reference_id
                                                                 FROM Reference
                                                                 WHERE publisher_reference = ?''', (publisher_id,)).fetchall()
    if check_if_publisher_has_references:
        error = "This author is still linked to references and thus cannot be deleted"
        
        dictionary = {
            'publisher_name': publisher_name,
            'references': references,
            'references_quantity': references_quantity,
            'publisher_id': publisher_id,
            'error': error
            }
        promethee_cursor.close()
        promethee_conn.close()
        return render(request, 'publisher_detail.html', dictionary)
    else:
        promethee_cursor.execute('''DELETE FROM Publisher
                                 WHERE publisher_id = ?''', (publisher_id,))
        promethee_cursor.close()
        promethee_conn.close()
        return redirect('/search')

####################
# DELETE AN AUTHOR #
####################
def delete_author(request, author_id):
    promethee_conn = sqlite3.connect('promethee_project.db', isolation_level=None)
    promethee_conn.execute("PRAGMA foreign_keys = 1")
    promethee_cursor = promethee_conn.cursor()

    all_informations = promethee_cursor.execute('''SELECT author_firstnames, author_initials, author_lastname, country_code, affiliation, author_email
                                                FROM Author
                                                WHERE author_id = ?''', (author_id,)).fetchall()[0]
    author_informations = {
        'author_firstnames': all_informations[0],
        'author_initials':all_informations[1],
        'author_lastname': all_informations[2],
        'country_code': all_informations[3],
        'affiliation': all_informations[4],
        'author_email': all_informations[5]
    }

    country_code = all_informations[3]
    country_informations = promethee_cursor.execute('''SELECT population_in_millions, continent, researchers
                                                    FROM Country
                                                    WHERE country_code = ?''', (country_code,)).fetchall()[0]
    country_infos = {
        'population_in_millions': country_informations[0],
        'continent': country_informations[1],
        'researchers': country_informations[2]
    }

    reference_ids = promethee_cursor.execute('''SELECT reference_id
                                             FROM Author_Reference
                                             WHERE author_id = ?''', (author_id,)).fetchall()
    references = []
    
    for single_reference_id in reference_ids:
        reference_id = single_reference_id[0]
        genre_ids = promethee_cursor.execute('''SELECT keyword_id
                                             FROM Genre_Reference
                                             WHERE reference_id = ?''', (reference_id,)).fetchall()
        genres_list = []
        for single_genre_id in genre_ids:
            genre_id = single_genre_id[0]
            genres = promethee_cursor.execute('''SELECT keyword
                                              FROM Genre
                                              WHERE keyword_id = ?''', (genre_id,)).fetchall()
            for single_genre in genres:
                genres_list.append(single_genre[0])

        authors_id_position = promethee_cursor.execute('''SELECT author_id, position
                                                       FROM Author_Reference
                                                       WHERE reference_id = ?''', (reference_id,)).fetchall()
        all_authors_informations = []
        for single_author_id_position in authors_id_position:
            single_author_id = single_author_id_position[0]
            single_author_position = single_author_id_position[1]
            author_identity = promethee_cursor.execute('''SELECT author_initials, author_lastname
                                                       FROM Author
                                                       WHERE author_id = ?''', (single_author_id,)).fetchall()[0]
            single_author_informations = {
                'author_id': single_author_id,
                'author_position': single_author_position,
                'author_initials': author_identity[0],
                'author_lastname': author_identity[1]
            }
            all_authors_informations.append(single_author_informations)

        single_reference = promethee_cursor.execute('''SELECT title, publisher_reference, year, volume, number, pages, type
                                                    FROM Reference
                                                    WHERE reference_id = ?''', (single_reference_id[0],)).fetchall()
        for information in single_reference:
            reference_id = single_reference_id[0]
            publisher_id = information[1]
            publisher_name = promethee_cursor.execute('''SELECT publisher_name
                                                      FROM Publisher
                                                      WHERE publisher_id = ?''', (publisher_id,)).fetchall()[0][0]
            reference ={
                'reference_id': reference_id,
                'title': information[0],
                'publisher_id': publisher_id,
                'publisher_name': publisher_name,
                'year': information[2],
                'volume': information[3],
                'number': information[4],
                'pages': information[5],
                'type': information[6],
                'genres': genres_list,
                'authors': all_authors_informations
            }
        references.append(reference)
    
    references_quantity = len(references)
    
    
    check_if_author_has_references = promethee_cursor.execute('''SELECT reference_id
                                                              FROM Author_Reference
                                                              WHERE author_id = ?''', (author_id,)).fetchall()
    if check_if_author_has_references:
        error = "This author is still linked to references and thus cannot be deleted"
        
        dictionary = {
            'error': error,
            'author_id': author_id,
            'author_informations': author_informations,
            'country_infos': country_infos,
            'references': references,
            'references_quantity': references_quantity
            
            }
        promethee_cursor.close()
        promethee_conn.close()
        return render(request, 'author_detail.html', dictionary)
    else:
        promethee_cursor.execute('''DELETE FROM Author
                                 WHERE author_id = ?''', (author_id,))
        promethee_cursor.close()
        promethee_conn.close()
        return redirect('/search')
