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
			sql = "SELECT id, name, picture, COUNT(*) as nombre \
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
			sql = "SELECT * \
					  FROM movies \
					      WHERE id = %s;"
			cursor.execute(sql, id)
			result = cursor.fetchone()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result
