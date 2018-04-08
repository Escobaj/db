import app.models.database as _database
from flask import flash


def get_top_rated_movies(nombre, page=0):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, ROUND(AVG(rate), 1) AS moyenne, picture \
					  FROM evaluate_movie \
					    JOIN movies m ON evaluate_movie.movies_id = m.id \
					      GROUP BY id \
					        ORDER BY moyenne DESC \
					          LIMIT %s, %s;"
			cursor.execute(sql, (page * nombre, nombre))
			result = cursor.fetchall()
	except:
		result = ()
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def get_most_commented_movies(nombre, page=0):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, picture \
					  FROM evaluate_movie \
					    JOIN movies m ON evaluate_movie.movies_id = m.id \
					      WHERE comment IS NOT NULL \
					        GROUP BY id \
					          ORDER BY COUNT(*) DESC \
					            LIMIT %s, %s;"
			cursor.execute(sql, (page * nombre, nombre))
			result = cursor.fetchall()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def get_most_interested_movies(nombre, page=0):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, picture, COUNT(*) AS nombre \
					  FROM movies \
					    JOIN wish_list_movies wlm ON movies.id = wlm.movies_id \
					      GROUP BY id \
					        ORDER BY COUNT(*) DESC \
					          LIMIT %s, %s;"
			cursor.execute(sql, (page * nombre, nombre))
			result = cursor.fetchall()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def show_movie(id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT *, avg(rate) as moyenne \
					  FROM movies \
					    JOIN evaluate_movie em ON movies.id = em.movies_id \
					      WHERE id = %s \
					        GROUP BY movies_id;"
			cursor.execute(sql, id)
			result = cursor.fetchone()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def get_countries(id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name \
					  FROM countries \
					    JOIN country_movie cm ON countries.id = cm.countries_id \
					      WHERE movies_id = %s;"
			cursor.execute(sql, id)
			result = cursor.fetchall()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	finally:
		conn.close()
	
	return result


def get_genres(id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name \
					  FROM genres \
					    JOIN genre_movie gm ON genres.id = gm.genres_id \
					      WHERE movies_id = %s;"
			cursor.execute(sql, id)
			result = cursor.fetchall()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	finally:
		conn.close()
	
	return result


def get_casting(id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT fullname, name AS role, picture \
					  FROM character_movie \
					    JOIN characters c ON character_movie.characters_id = c.id \
					    JOIN roles r ON character_movie.roles_id = r.id \
					      WHERE movies_id = %s;"
			cursor.execute(sql, id)
			result = cursor.fetchall()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	finally:
		conn.close()
	
	return result


def get_reviews(id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT username, comment \
					  FROM evaluate_movie \
					    JOIN movies m ON evaluate_movie.movies_id = m.id \
					    JOIN users u ON evaluate_movie.users_id = u.id \
					      WHERE movies_id = %s;"
			cursor.execute(sql, id)
			result = cursor.fetchall()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	finally:
		conn.close()
	
	return result


def get_user_review(id, user_id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT comment, rate \
  					  FROM evaluate_movie \
    					WHERE users_id = %s AND movies_id = %s;"
			cursor.execute(sql, (user_id, id))
			result = cursor.fetchone()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	finally:
		conn.close()
	
	return result
	

def rate_movie(id, user_id, rate):
	conn = _database.connection()

	try:
		with conn.cursor() as cursor:
			sql = " INSERT INTO evaluate_movie (`users_id`, `movies_id`, `comment`, `rate`) VALUE (%s, %s, NULL, %s) \
			        ON DUPLICATE KEY UPDATE `rate` = %s;"
			cursor.execute(sql, (user_id, id, rate, rate))
			cursor.fetchone()
			result = True
	except Exception as e:
		result = False
	finally:
		cursor.close()
		conn.close()
		
	return result