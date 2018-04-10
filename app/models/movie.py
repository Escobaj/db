import app.models.database as _database
from flask import flash


def get_top_rated_movies(nombre, page=0):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, ROUND(AVG(rate), 1) AS moyenne, picture, release_year, description \
					  FROM evaluate_movie \
					    JOIN movies m ON evaluate_movie.movies_id = m.id \
					      GROUP BY id \
					        ORDER BY moyenne DESC \
					          LIMIT %s, %s;"
			cursor.execute(sql, (int(page) * int(nombre), int(nombre)))
			result = cursor.fetchall()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
		flash(e, 'error')
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
			sql = "SELECT *, avg(rate) AS moyenne \
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


def comment_movie(id, user_id, comment):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "INSERT INTO evaluate_movie (`users_id`, `movies_id`, `comment`, `rate`) VALUE (%s, %s, %s, NULL) \
			       ON DUPLICATE KEY UPDATE `comment` = %s;"
			
			cursor.execute(sql, (user_id, id, comment, comment))
			cursor.fetchone()
			result = True
			cursor.close()
	
	except Exception as e:
		result = False
	finally:
		conn.close()
	
	return result


def get_user_wishlist(movie_id, user_id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT COUNT(*) as total \
  						FROM wish_list_movies \
    						WHERE users_id = %s AND movies_id = %s;"
			cursor.execute(sql, (user_id, movie_id))
			row = cursor.fetchone()
			if row['total'] == 1:
				result = True
			else:
				result = False
			cursor.close()
	
	except Exception as e:
		result = False
	finally:
		conn.close()
	
	return result


def wishlist_movie(movie_id, user_id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "INSERT INTO wish_list_movies (users_id, movies_id) VALUES (%s, %s)"
			cursor.execute(sql, (user_id, movie_id))
			cursor.close()
			flash('This movie have been added to your wishlist', 'success')
	
	except Exception as e:
		try:
			with conn.cursor() as cursor:
				sql = "DELETE FROM wish_list_movies WHERE users_id = %s AND movies_id = %s;"
				cursor.execute(sql, (user_id, movie_id))
				cursor.close()
				flash('This movie have been removed from your wishlist', 'success')
		except Exception:
			flash('The database is unavailable', 'error')
			
	finally:
		conn.close()


def get_total_movie_number():
	conn = _database.connection()
	result = 0
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT COUNT(*) as total FROM movies"
			cursor.execute(sql)
			result = cursor.fetchone()['total']
			cursor.close()
	
	except Exception as e:
		flash('The database is unavailable', 'error')
		flash(e, 'error')
		
	
	finally:
		conn.close()

	return result