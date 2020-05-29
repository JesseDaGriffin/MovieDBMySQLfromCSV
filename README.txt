Programmer: Jesse Griffin
Movie Database
3/21/19

Script Description:
    This script will create the necessary tables needed for our database. Then, it will
    read the movie database csv file and iterate through each tuple, adding them to the
    appropriate table as it moves through the file. Finally, it will either perform the
    specified assignment query or perform all five assignment queries, if none is given.

Run Script:
    To run script, use command:
    >python moviedb.py username password <query #>

    If python 3 is not set as default, use command:
    >python3 moviedb.py username password <query #>

    Where <query #> is a number, 1 - 5, that correlates to the queries given in assignment 5,
    ’username’ is the name of the user for the database, and ’password’ is the password

    The csv file must be in the same directory as the py scripts.

Queries:
    1. What is the average budget of all movies? Your output should include just the average
    budget value.

    2. Show only the movies that were produced in the United States. Your output must include
    the movie title and the production company name.

    3. Show the top 5 movies that made the most revenue. Your output must include the movie
    title and how much revenue it brought in.

    4. What movies have both the genre Science Fiction and Mystery. Your output must include
    the movie title and all genres associated with that movie.

    5. Find the movies that have a popularity greater than the average popularity. Your output
    must include the movie title and their popularity.
