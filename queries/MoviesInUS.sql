SELECT title, prodComp_name, MovieDBAssign5.Production_country.iso3166_id
FROM MovieDBAssign5.Movie
JOIN MovieDBAssign5.Movie_has_Production_company
ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Production_company.id
JOIN MovieDBAssign5.Production_company
ON MovieDBAssign5.Movie_has_Production_company.prodComp_id = MovieDBAssign5.Production_company.prodComp_id
JOIN MovieDBAssign5.Movie_has_Production_country
ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Production_country.id
JOIN MovieDBAssign5.Production_country
ON MovieDBAssign5.Movie_has_Production_country.iso3166_id = MovieDBAssign5.Production_country.iso3166_id
WHERE MovieDBAssign5.Production_country.iso3166_id = "US" and not MovieDBAssign5.Movie.id = any(
	SELECT MovieDBAssign5.Movie.id
	FROM MovieDBAssign5.Movie
	JOIN MovieDBAssign5.Movie_has_Production_company
	ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Production_company.id
	JOIN MovieDBAssign5.Production_company
	ON MovieDBAssign5.Movie_has_Production_company.prodComp_id = MovieDBAssign5.Production_company.prodComp_id
	JOIN MovieDBAssign5.Movie_has_Production_country
	ON MovieDBAssign5.Movie.id = MovieDBAssign5.Movie_has_Production_country.id
	JOIN MovieDBAssign5.Production_country
	ON MovieDBAssign5.Movie_has_Production_country.iso3166_id = MovieDBAssign5.Production_country.iso3166_id
	WHERE MovieDBAssign5.Production_country.iso3166_id != "US")
LIMIT 5