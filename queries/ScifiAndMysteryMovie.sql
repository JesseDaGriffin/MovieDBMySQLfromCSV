SELECT title, MovieDBAssign5.Genre.gen_name
FROM MovieDBAssign5.Movie
JOIN MovieDBAssign5.Movie_has_Genre
ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Genre.id
JOIN MovieDBAssign5.Genre
ON MovieDBAssign5.Movie_has_Genre.genre_id =  MovieDBAssign5.Genre.genre_id
WHERE MovieDBAssign5.Movie.id = any(
	SELECT MovieDBAssign5.Movie.id
	FROM MovieDBAssign5.Movie
	JOIN MovieDBAssign5.Movie_has_Genre
	ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Genre.id
	JOIN MovieDBAssign5.Genre
	ON MovieDBAssign5.Movie_has_Genre.genre_id =  MovieDBAssign5.Genre.genre_id
	WHERE MovieDBAssign5.Genre.gen_name = "Science Fiction")
and MovieDBAssign5.Movie.id = any(
	SELECT MovieDBAssign5.Movie.id
	FROM MovieDBAssign5.Movie
	JOIN MovieDBAssign5.Movie_has_Genre
	ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Genre.id
	JOIN MovieDBAssign5.Genre
	ON MovieDBAssign5.Movie_has_Genre.genre_id =  MovieDBAssign5.Genre.genre_id
	WHERE MovieDBAssign5.Genre.gen_name = "Mystery")
LIMIT 5