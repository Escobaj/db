import app.models.database as _database
from flask import flash


def get_character(id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT fullname, picture \
					  FROM characters \
					    WHERE id = %s;"
			cursor.execute(sql, (id))
			result = cursor.fetchone()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	finally:
		conn.close()
	
	return result


def get_all_elements(id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, 'serie' AS type, picture \
					FROM series \
					  JOIN character_serie cs ON series.id = cs.series_id \
					WHERE characters_id = %s \
					UNION \
					SELECT id, name, 'movie' AS type, picture \
					FROM movies \
					  JOIN character_movie m ON movies.id = m.movies_id \
					WHERE characters_id = %s;"
			cursor.execute(sql, (id, id))
			result = cursor.fetchall()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	finally:
		conn.close()
	
	return result
