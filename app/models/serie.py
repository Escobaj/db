import app.models.database as _database
from flask import flash


def get_top_rated_series(nombre, page=0):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, ROUND(AVG(rate), 1) AS moyenne, picture, `release`, description \
					  FROM evaluate_serie \
					    JOIN series m ON evaluate_serie.series_id = m.id \
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


def get_most_commented_series(nombre, page=0):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, picture, `release`, description \
					  FROM evaluate_serie \
					    JOIN series m ON evaluate_serie.series_id = m.id \
					      WHERE comment IS NOT NULL \
					        GROUP BY id \
					          ORDER BY COUNT(*) DESC \
					            LIMIT %s, %s;"
			cursor.execute(sql, (page * nombre, nombre))
			result = cursor.fetchall()
	except Exception as e:
		result = ()
		flash(e, 'error')
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def get_most_interested_series(nombre, page=0):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, picture, COUNT(*) AS nombre, `release`, description \
					  FROM series \
					    JOIN wish_list_series wlm ON series.id = wlm.series_id \
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


def show_serie(id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT *, avg(rate) AS moyenne \
					  FROM series \
					     LEFT JOIN evaluate_serie em ON series.id = em.series_id \
					      WHERE id = %s \
					        GROUP BY series_id;"
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
					    JOIN country_serie cm ON countries.id = cm.countries_id \
					      WHERE series_id = %s;"
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
					    JOIN genre_serie gm ON genres.id = gm.genres_id \
					      WHERE series_id = %s;"
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
			sql = "SELECT characters_id as id, fullname, name AS role, picture \
					  FROM character_serie \
					    JOIN characters c ON character_serie.characters_id = c.id \
					    JOIN roles r ON character_serie.roles_id = r.id \
					      WHERE series_id = %s;"
			cursor.execute(sql, id)
			result = cursor.fetchall()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	finally:
		conn.close()
	
	return result


def get_reviews(id, nombre, page):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT u.id AS id, username, comment \
					  FROM evaluate_serie \
					    JOIN series m ON evaluate_serie.series_id = m.id \
					    JOIN users u ON evaluate_serie.users_id = u.id \
					      WHERE series_id = %s LIMIT %s, %s;"
			cursor.execute(sql, (id, int(page) * int(nombre), int(nombre)))
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
  					  FROM evaluate_serie \
    					WHERE users_id = %s AND series_id = %s;"
			cursor.execute(sql, (user_id, id))
			result = cursor.fetchone()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	finally:
		conn.close()
	
	return result


def rate_serie(id, user_id, rate):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = " INSERT INTO evaluate_serie (`users_id`, `series_id`, `comment`, `rate`) VALUE (%s, %s, NULL, %s) \
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


def comment_serie(id, user_id, comment):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "INSERT INTO evaluate_serie (`users_id`, `series_id`, `comment`, `rate`) VALUE (%s, %s, %s, NULL) \
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


def get_user_wishlist(serie_id, user_id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT COUNT(*) AS total \
  						FROM wish_list_series \
    						WHERE users_id = %s AND series_id = %s;"
			cursor.execute(sql, (user_id, serie_id))
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


def wishlist_serie(serie_id, user_id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "INSERT INTO wish_list_series (users_id, series_id) VALUES (%s, %s)"
			cursor.execute(sql, (user_id, serie_id))
			cursor.close()
			flash('This serie have been added to your wishlist', 'success')
	
	except Exception as e:
		try:
			with conn.cursor() as cursor:
				sql = "DELETE FROM wish_list_series WHERE users_id = %s AND series_id = %s;"
				cursor.execute(sql, (user_id, serie_id))
				cursor.close()
				flash('This serie have been removed from your wishlist', 'success')
		except Exception:
			flash('The database is unavailable', 'error')
	
	finally:
		conn.close()


def get_total_serie_number():
	conn = _database.connection()
	result = 0
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT COUNT(*) AS total FROM series"
			cursor.execute(sql)
			result = cursor.fetchone()['total']
			cursor.close()
	
	except Exception as e:
		flash('The database is unavailable', 'error')
		flash(e, 'error')
	
	finally:
		conn.close()
	
	return result


def get_all_rates(id):
	conn = _database.connection()
	result = 0
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, rate, picture, `release`, 'serie' AS type FROM evaluate_serie \
					JOIN series m ON evaluate_serie.series_id = m.id WHERE users_id = %s AND rate IS NOT NULL \
				   UNION SELECT id, name, rate, picture, `release`, 'game' AS type FROM evaluate_game \
				    JOIN games m ON evaluate_game.games_id = m.id WHERE users_id = %s AND rate IS NOT NULL \
				   UNION SELECT id, name, rate, picture, `release`, 'serie' AS type FROM evaluate_serie \
				    JOIN series m ON evaluate_serie.series_id = m.id WHERE users_id = %s AND rate IS NOT NULL"
			cursor.execute(sql, (id, id, id))
			result = cursor.fetchall()
			cursor.close()
	
	except Exception as e:
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def get_all_comment(id):
	conn = _database.connection()
	result = 0
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, comment, picture, `release`, 'serie' AS type FROM evaluate_serie \
					JOIN series m ON evaluate_serie.series_id = m.id WHERE users_id = %s AND comment IS NOT NULL AND comment != '' \
				   UNION SELECT id, name, comment, picture, `release`, 'game' AS type FROM evaluate_game \
				    JOIN games m ON evaluate_game.games_id = m.id WHERE users_id = %s AND comment IS NOT NULL AND comment != '' \
				   UNION SELECT id, name, comment, picture, `release`, 'serie' AS type FROM evaluate_serie \
				    JOIN series m ON evaluate_serie.series_id = m.id WHERE users_id = %s AND comment IS NOT NULL AND comment != ''"
			cursor.execute(sql, (id, id, id))
			result = cursor.fetchall()
			cursor.close()
	
	except Exception as e:
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def get_all_wishlisted(id):
	conn = _database.connection()
	result = 0
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, `release`, 'serie' AS type, picture FROM wish_list_series \
					JOIN series m ON wish_list_series.series_id = m.id WHERE users_id = %s \
				   UNION SELECT id, name, `release`, 'serie' AS type, picture FROM wish_list_series \
				   JOIN series s ON wish_list_series.series_id = s.id WHERE users_id = %s \
				   UNION SELECT id, name, `release`, 'game' AS type, picture FROM wish_list_games \
				   JOIN games g ON wish_list_games.games_id = g.id WHERE users_id = %s;"
			cursor.execute(sql, (id, id, id))
			result = cursor.fetchall()
			cursor.close()
	
	except Exception as e:
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def delete_comment(serie_id, user_id):
	conn = _database.connection()
	result = 0
	
	try:
		with conn.cursor() as cursor:
			sql = "UPDATE evaluate_serie SET comment = NULL WHERE series_id = %s AND users_id = %s;"
			cursor.execute(sql, (serie_id, user_id))
			result = cursor.fetchall()
			cursor.close()
	
	except Exception as e:
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def delete_rate(serie_id, user_id):
	conn = _database.connection()
	result = 0
	
	try:
		with conn.cursor() as cursor:
			sql = "UPDATE evaluate_serie SET rate = NULL WHERE series_id = %s AND users_id = %s;"
			cursor.execute(sql, (serie_id, user_id))
			result = cursor.fetchall()
			cursor.close()
	
	except Exception as e:
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def get_nb_comments(identifiant):
	conn = _database.connection()
	result = 0
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT count(*) as total FROM evaluate_serie WHERE comment IS NOT NULL AND series_id = %s;"
			cursor.execute(sql, identifiant)
			result = cursor.fetchone()['total']
			cursor.close()
	
	except Exception as e:
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result