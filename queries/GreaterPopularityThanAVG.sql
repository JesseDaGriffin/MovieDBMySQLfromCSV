SELECT title, popularity
FROM MovieDBAssign5.Movie
WHERE popularity > (
	SELECT avg(popularity)
    FROM MovieDBAssign5.Movie)
LIMIT 5
 