import sys
import pymysql
import csv
import json


def main():
    # Gather username, password, and specified query (if any) from command line
    username = sys.argv[1]
    password = sys.argv[2]
    queries = [0, 0, 0, 0, 0]

    # If 4 arguments, use last a query number
    if len(sys.argv) == 4:
        # Exit if specified query is not between 1 and 5
        if int(sys.argv[3]) > 5 or int(sys.argv[3]) < 1:
            sys.exit("Query number must be between 1 and 5")

        # Flag specified query
        queries[int(sys.argv[3]) - 1] = 1

    # Mark all queries to be ran if none specified in command line
    else:
        for i in range(0, 5):
            queries[i] = 1

    # Open csv file to read and fill tables
    with open('tmdb_5000_movies.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        conn = pymysql.connect(host='localhost', port=3306, user=username, passwd=password, db='MovieDBAssign5')
        cur = conn.cursor()

        # Create all tables needed in database
        createRel(conn, cur)

        # Fill tables with tuples from csv file
        parseInto(conn, cur, csv_reader)

        """Query 1: Average budget"""
        if queries[0] == 1:
            # What is the average budget of all movies? Your output should include just the average budget value.
            cur.execute("""SELECT\
                AVG(budget)\
                FROM MovieDBAssign5.Movie""")

            tuples = cur.fetchall()
            print("--- Average Budget ---")
            for t in tuples:
                print(t[0])

        """Query 2: 5 Movies Produced in the US"""
        if queries[1] == 1:
            # Show only the movies that were produced in the United States. Your output must include the movie title and
            # the production company name.
            cur.execute("""SELECT title, prodComp_name\
                FROM MovieDBAssign5.Movie\
                JOIN MovieDBAssign5.Movie_has_Production_company\
                ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Production_company.id\
                JOIN MovieDBAssign5.Production_company\
                ON MovieDBAssign5.Movie_has_Production_company.prodComp_id = MovieDBAssign5.Production_company.prodComp_id\
                JOIN MovieDBAssign5.Movie_has_Production_country\
                ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Production_country.id\
                JOIN MovieDBAssign5.Production_country\
                ON MovieDBAssign5.Movie_has_Production_country.iso3166_id = MovieDBAssign5.Production_country.iso3166_id\
                WHERE MovieDBAssign5.Production_country.iso3166_id = "US"\
                LIMIT 5""")

            tuples = cur.fetchall()
            print("--- 5 Movies Made in the US ---")
            for t in tuples:
                print(t)

        """Query 3: Top 5 highest revenue"""
        if queries[2] == 1:
            # Show the top 5 movies that made the most revenue. Your output must include the movie title and how much
            # revenue it brought in.
            cur.execute("""SELECT title, revenue\
                FROM MovieDBAssign5.Movie\
                ORDER BY revenue\
                DESC\
                LIMIT 5""")

            tuples = cur.fetchall()
            print("--- Top 5 Highest Revenue ---")
            for t in tuples:
                print(t)

        """Query 4: 5 Movies in SciFi and Mystery Genre"""
        if queries[3] == 1:
            # What movies have both the genre Science Fiction and Mystery. Your output must include the movie title and
            # all genres associated with that genre.
            cur.execute("""SELECT title, MovieDBAssign5.Genre.gen_name\
                FROM MovieDBAssign5.Movie\
                JOIN MovieDBAssign5.Movie_has_Genre\
                ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Genre.id\
                JOIN MovieDBAssign5.Genre\
                ON MovieDBAssign5.Movie_has_Genre.genre_id =  MovieDBAssign5.Genre.genre_id\
                WHERE MovieDBAssign5.Movie.id = any(\
                SELECT MovieDBAssign5.Movie.id\
                FROM MovieDBAssign5.Movie\
                JOIN MovieDBAssign5.Movie_has_Genre\
                ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Genre.id\
                JOIN MovieDBAssign5.Genre\
                ON MovieDBAssign5.Movie_has_Genre.genre_id =  MovieDBAssign5.Genre.genre_id\
                WHERE MovieDBAssign5.Genre.gen_name = "Science Fiction")\
                and MovieDBAssign5.Movie.id = any(\
                SELECT MovieDBAssign5.Movie.id\
                FROM MovieDBAssign5.Movie\
                JOIN MovieDBAssign5.Movie_has_Genre\
                ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Genre.id\
                JOIN MovieDBAssign5.Genre\
                ON MovieDBAssign5.Movie_has_Genre.genre_id =  MovieDBAssign5.Genre.genre_id\
                WHERE MovieDBAssign5.Genre.gen_name = "Mystery")\
                LIMIT 5""")

            tuples = cur.fetchall()
            print("--- 5 Movies in SciFi and Mystery Genre ---")
            for t in tuples:
                print(t)

        """Query 5: 5 Movies With Greater Popularity Than Average"""
        if queries[4] == 1:
            # Find the movies that have a popularity greater than the average popularity. Your output must include the
            # movie title and their popularity.
            cur.execute("""SELECT title, popularity\
                FROM MovieDBAssign5.Movie\
                WHERE popularity > (\
                SELECT avg(popularity)\
                FROM MovieDBAssign5.Movie)\
                LIMIT 5""")

            tuples = cur.fetchall()
            print("--- 5 Movies With Greater Popularity Than Average ---")
            for t in tuples:
                print(t)

        conn.close()
        cur.close()


def createRel(conn, cur):
    # Drop tables if they already exist
    cur.execute("""DROP TABLE IF EXISTS `Movie_has_Genre`""")
    cur.execute("""DROP TABLE IF EXISTS `Movie_has_Keywords`""")
    cur.execute("""DROP TABLE IF EXISTS `Movie_has_Production_company`""")
    cur.execute("""DROP TABLE IF EXISTS `Movie_has_Production_country`""")
    cur.execute("""DROP TABLE IF EXISTS `Movie_has_Spoken_language`""")
    cur.execute("""DROP TABLE IF EXISTS `Movie`""")
    cur.execute("""DROP TABLE IF EXISTS `Genre`""")
    cur.execute("""DROP TABLE IF EXISTS `Keyword`""")
    cur.execute("""DROP TABLE IF EXISTS `Production_Company`""")
    cur.execute("""DROP TABLE IF EXISTS `Production_country`""")
    cur.execute("""DROP TABLE IF EXISTS `Spoken_language`""")

    # Table holds all movie information
    cur.execute("""CREATE TABLE `Movie` (`id` int(11) NOT NULL,\
        `budget` bigint(10) DEFAULT NULL,\
        `homepage` varchar(255) DEFAULT NULL,\
        `original_language` char(2) DEFAULT NULL,\
        `original_title` varchar(100) DEFAULT NULL,\
        `overview` mediumblob,`popularity` float DEFAULT NULL,\
        `release_date` varchar(10) DEFAULT NULL,\
        `revenue` bigint(12) DEFAULT NULL,\
        `runtime` int(11) DEFAULT NULL,\
        `status` varchar(45) DEFAULT NULL,\
        `tagline` blob,`title` varchar(100) DEFAULT NULL,\
        `vote_average` float DEFAULT NULL,\
        `vote_count` int(11) DEFAULT NULL,\
        PRIMARY KEY (`id`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8""")

    # Table holds all genres
    cur.execute("""CREATE TABLE `Genre` (\
        `genre_id` int(11) NOT NULL,\
        `gen_name` varchar(45) DEFAULT NULL,\
        PRIMARY KEY (`genre_id`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8""")

    # Table holds all movie keywords
    cur.execute("""CREATE TABLE `Keyword` (\
        `keyword_id` int(11) NOT NULL,\
        `keyword_name` varchar(45) DEFAULT NULL,\
        PRIMARY KEY (`keyword_id`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8""")

    # Table holds all production companies
    cur.execute("""CREATE TABLE `Production_company` (\
        `prodComp_id` int(11) NOT NULL,\
        `prodComp_name` varchar(45) DEFAULT NULL,\
        PRIMARY KEY (`prodComp_id`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8""")

    # Table holds all production countries
    cur.execute("""CREATE TABLE `Production_country` (\
        `iso3166_id` char(2) NOT NULL,\
        `prodCountry_name` varchar(45) DEFAULT NULL,\
        PRIMARY KEY (`iso3166_id`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8""")

    # Table holds all spoken languages
    cur.execute("""CREATE TABLE `Spoken_language` (\
        `iso639_id` char(2) NOT NULL,\
        `lang_name` varchar(45) DEFAULT NULL,\
        PRIMARY KEY (`iso639_id`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8""")

    # Join table between movies and genres
    cur.execute("""CREATE TABLE `Movie_has_Genre` (\
        `relationship_id` int(11) NOT NULL AUTO_INCREMENT,\
        `id` int(11) DEFAULT NULL,\
        `genre_id` int(11) DEFAULT NULL,\
        PRIMARY KEY (`relationship_id`),\
        KEY `fk_Movie_has_Genre_Genre1_idx` (`genre_id`),\
        KEY `fk_Movie_has_Genre_Movie1_idx` (`id`),\
        CONSTRAINT `fk_Movie_has_Genre_Genre1` FOREIGN KEY (`genre_id`) REFERENCES `genre` (`genre_id`),\
        CONSTRAINT `fk_Movie_has_Genre_Movie1` FOREIGN KEY (`id`) REFERENCES `movie` (`id`)\
        ) ENGINE=InnoDB AUTO_INCREMENT=12161 DEFAULT CHARSET=utf8""")

    # Join table between movies and keywords
    cur.execute("""CREATE TABLE `Movie_has_Keywords` (\
        `relationship_id` int(11) NOT NULL AUTO_INCREMENT,\
        `id` int(11) DEFAULT NULL,\
        `keyword_id` int(11) DEFAULT NULL,\
        PRIMARY KEY (`relationship_id`),\
        KEY `fk_Movie_has_Keywords_Keywords1_idx` (`keyword_id`),\
        KEY `fk_Movie_has_Keywords_Movie1` (`id`),\
        CONSTRAINT `fk_Movie_has_Keywords_Keywords1` FOREIGN KEY (`keyword_id`) REFERENCES `keyword` (`keyword_id`) ON DELETE CASCADE ON UPDATE CASCADE,\
        CONSTRAINT `fk_Movie_has_Keywords_Movie1` FOREIGN KEY (`id`) REFERENCES `movie` (`id`) ON DELETE CASCADE ON UPDATE CASCADE\
        ) ENGINE=InnoDB AUTO_INCREMENT=36195 DEFAULT CHARSET=utf8""")

    # Join table between movies and production companies
    cur.execute("""CREATE TABLE `Movie_has_Production_company` (\
        `relationship_id` int(11) NOT NULL AUTO_INCREMENT,\
        `id` int(11) DEFAULT NULL,\
        `prodComp_id` int(11) DEFAULT NULL,\
        PRIMARY KEY (`relationship_id`),\
        KEY `fk_Movie_has_Production_company_Production_company1_idx` (`prodComp_id`),\
        KEY `fk_Movie_has_Production_company_Movie1_idx` (`id`),\
        CONSTRAINT `fk_Movie_has_Production_company_Movie1` FOREIGN KEY (`id`) REFERENCES `movie` (`id`),\
        CONSTRAINT `fk_Movie_has_Production_company_Production_company1` FOREIGN KEY (`prodComp_id`) REFERENCES `production_company` (`prodComp_id`)\
        ) ENGINE=InnoDB AUTO_INCREMENT=13678 DEFAULT CHARSET=utf8""")

    # Join table between movies and production countries
    cur.execute("""CREATE TABLE `Movie_has_Production_country` (\
        `relationship_id` int(11) NOT NULL AUTO_INCREMENT,\
        `id` int(11) DEFAULT NULL,\
        `iso3166_id` char(2) DEFAULT NULL,\
        PRIMARY KEY (`relationship_id`),\
        KEY `fk_Movie_has_Production_country1_Production_country1_idx` (`iso3166_id`),\
        KEY `fk_Movie_has_Production_country1_Movie1_idx` (`id`),\
        CONSTRAINT `fk_Movie_has_Production_country1_Movie1` FOREIGN KEY (`id`) REFERENCES `movie` (`id`),\
        CONSTRAINT `fk_Movie_has_Production_country1_Production_country1` FOREIGN KEY (`iso3166_id`) REFERENCES `production_country` (`iso3166_id`)\
        ) ENGINE=InnoDB AUTO_INCREMENT=6437 DEFAULT CHARSET=utf8""")

    # Join table between movies and spoken languages
    cur.execute("""CREATE TABLE `Movie_has_Spoken_language` (\
        `relationship_id` int(11) NOT NULL AUTO_INCREMENT,\
        `id` int(11) DEFAULT NULL,\
        `iso639_id` char(2) DEFAULT NULL,\
        PRIMARY KEY (`relationship_id`),\
        KEY `fk_Movie_has_Spoken_language_Spoken_language1_idx` (`iso639_id`),\
        KEY `fk_Movie_has_Spoken_language_Movie1_idx` (`id`),\
        CONSTRAINT `fk_Movie_has_Spoken_language_Movie1` FOREIGN KEY (`id`) REFERENCES `movie` (`id`),\
        CONSTRAINT `fk_Movie_has_Spoken_language_Spoken_language1` FOREIGN KEY (`iso639_id`) REFERENCES `spoken_language` (`iso639_id`)\
        ) ENGINE=InnoDB AUTO_INCREMENT=6938 DEFAULT CHARSET=utf8""")

    conn.commit()


def parseInto(conn, cur, csv_reader):
    # Iterate through each tuple in the csv file
    for line in csv_reader:
        # For messed up lines with empty string as runtime
        if line['runtime'] == '':
            runtime = None
        else:
            runtime = line['runtime']

        values = (line['budget'], line['homepage'], line['id'], line['original_language'], line['original_title'], line['overview'], line['popularity'], line['release_date'], line['revenue'], runtime, line['status'], line['tagline'], line['title'], line['vote_average'], line['vote_count'])

        """Insert movie info into movie table"""
        try:
            cur.execute("""INSERT INTO Movie (budget, homepage, id, original_language, original_title, overview, popularity, release_date, revenue, runtime, status, tagline, title, vote_average, vote_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", values)
        except Exception as e:
            print(e)
            print(line)
            print("-----------------------------------------------------")
            continue

        """Gather genre info for table and join"""
        genres = json.loads(line['genres'])

        for genre in genres:
            try:
                cur.execute("""INSERT INTO Genre (genre_id, gen_name) VALUES (%s, %s)""", (genre['id'], genre['name']))
            except:
                continue

        for genre in genres:
            try:
                cur.execute("""INSERT INTO Movie_has_Genre (id, genre_id) VALUES (%s, %s)""", (line['id'], genre['id']))
            except:
                continue

        """Gather keyword info for table and join"""
        keys = json.loads(line['keywords'])

        for key in keys:
            try:
                cur.execute("""INSERT INTO Keyword (keyword_id, keyword_name) VALUES (%s, %s)""", (key['id'], key['name']))
            except:
                continue

        for key in keys:
            try:
                cur.execute("""INSERT INTO Movie_has_Keywords (id, keyword_id) VALUES (%s, %s)""", (line['id'], key['id']))
            except:
                continue

        """Gather production companies info for table and join"""
        prodComps = json.loads(line['production_companies'])

        for prodComp in prodComps:
            try:
                cur.execute("""INSERT INTO Production_company (prodComp_id, prodComp_name) VALUES (%s, %s)""", (prodComp['id'], prodComp['name']))
            except:
                continue

        for prodComp in prodComps:
            try:
                cur.execute("""INSERT INTO Movie_has_Production_company (id, prodComp_id) VALUES (%s, %s)""", (line['id'], prodComp['id']))
            except:
                continue

        """Gather production countries info for table and join"""
        prodCountries = json.loads(line['production_countries'])

        for prodCountry in prodCountries:
            try:
                cur.execute("""INSERT INTO Production_country (iso3166_id, prodCountry_name) VALUES (%s, %s)""", (prodCountry['iso_3166_1'], prodCountry['name']))
            except:
                continue

        for prodCountry in prodCountries:
            try:
                cur.execute("""INSERT INTO Movie_has_Production_country (id, iso3166_id) VALUES (%s, %s)""", (line['id'], prodCountry['iso_3166_1']))
            except:
                continue

        """Gather spoken languages info for table and join"""
        langs = json.loads(line['spoken_languages'])

        for lang in langs:
            try:
                cur.execute("""INSERT INTO Spoken_language (iso639_id, lang_name) VALUES (%s, %s)""", (lang['iso_639_1'], lang['name']))
            except:
                continue

        for lang in langs:
            try:
                cur.execute("""INSERT INTO Movie_has_Spoken_language (id, iso639_id) VALUES (%s, %s)""", (line['id'], lang['iso_639_1']))
            except:
                continue
    conn.commit()


main()
