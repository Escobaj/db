import app.models.database as _database
from flask import flash


def get_top_rated_games(nombre, page=0):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, ROUND(AVG(rate), 1) AS moyenne, picture, release_year, description \
					  FROM evaluate_game \
					    JOIN games m ON evaluate_game.games_id = m.id \
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


def get_most_commented_games(nombre, page=0):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, picture, release_year, description \
					  FROM evaluate_game \
					    JOIN games m ON evaluate_game.games_id = m.id \
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


def get_most_interested_games(nombre, page=0):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT id, name, picture, COUNT(*) AS nombre, release_year, description \
					  FROM games \
					    JOIN wish_list_games wlm ON games.id = wlm.games_id \
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


def show_game(id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT *, avg(rate) AS moyenne \
					  FROM games \
					     LEFT JOIN evaluate_game em ON games.id = em.games_id \
					      WHERE id = %s \
					        GROUP BY games_id;"
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
					    JOIN country_game cm ON countries.id = cm.countries_id \
					      WHERE games_id = %s;"
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
					    JOIN genre_game gm ON genres.id = gm.genres_id \
					      WHERE games_id = %s;"
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
					  FROM character_game \
					    JOIN characters c ON character_game.characters_id = c.id \
					    JOIN roles r ON character_game.roles_id = r.id \
					      WHERE games_id = %s;"
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
			sql = "SELECT u.id AS id, username, comment \
					  FROM evaluate_game \
					    JOIN games m ON evaluate_game.games_id = m.id \
					    JOIN users u ON evaluate_game.users_id = u.id \
					      WHERE games_id = %s;"
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
  					  FROM evaluate_game \
    					WHERE users_id = %s AND games_id = %s;"
			cursor.execute(sql, (user_id, id))
			result = cursor.fetchone()
	except Exception as e:
		result = ()
		flash('The database is unavailable', 'error')
	finally:
		conn.close()
	
	return result


def rate_game(id, user_id, rate):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = " INSERT INTO evaluate_game (`users_id`, `games_id`, `comment`, `rate`) VALUE (%s, %s, NULL, %s) \
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


def comment_game(id, user_id, comment):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "INSERT INTO evaluate_game (`users_id`, `games_id`, `comment`, `rate`) VALUE (%s, %s, %s, NULL) \
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


def get_user_wishlist(game_id, user_id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT COUNT(*) AS total \
  						FROM wish_list_games \
    						WHERE users_id = %s AND games_id = %s;"
			cursor.execute(sql, (user_id, game_id))
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


def wishlist_game(game_id, user_id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "INSERT INTO wish_list_games (users_id, games_id) VALUES (%s, %s)"
			cursor.execute(sql, (user_id, game_id))
			cursor.close()
			flash('This game have been added to your wishlist', 'success')
	
	except Exception as e:
		try:
			with conn.cursor() as cursor:
				sql = "DELETE FROM wish_list_games WHERE users_id = %s AND games_id = %s;"
				cursor.execute(sql, (user_id, game_id))
				cursor.close()
				flash('This game have been removed from your wishlist', 'success')
		except Exception:
			flash('The database is unavailable', 'error')
	
	finally:
		conn.close()


def get_total_game_number():
	conn = _database.connection()
	result = 0
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT COUNT(*) AS total FROM games"
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
			sql = "SELECT id, name, rate, picture, release_year, 'game' AS type FROM evaluate_game \
					JOIN games m ON evaluate_game.games_id = m.id WHERE users_id = %s AND rate IS NOT NULL \
				   UNION SELECT id, name, rate, picture, release_year, 'game' AS type FROM evaluate_game \
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
			sql = "SELECT id, name, comment, picture, release_year, 'game' AS type FROM evaluate_game \
					JOIN games m ON evaluate_game.games_id = m.id WHERE users_id = %s AND comment IS NOT NULL AND comment != '' \
				   UNION SELECT id, name, comment, picture, release_year, 'game' AS type FROM evaluate_game \
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
			sql = "SELECT id, name, release_year, 'game' AS type, picture FROM wish_list_games \
					JOIN games m ON wish_list_games.games_id = m.id WHERE users_id = %s \
				   UNION SELECT id, name, `release`, 'serie' AS type, picture FROM wish_list_series \
				   JOIN series s ON wish_list_series.series_id = s.id WHERE users_id = %s \
				   UNION SELECT id, name, release_year, 'game' AS type, picture FROM wish_list_games \
				   JOIN games g ON wish_list_games.games_id = g.id WHERE users_id = %s;"
			cursor.execute(sql, (id, id, id))
			result = cursor.fetchall()
			cursor.close()
	
	except Exception as e:
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def delete_comment(game_id, user_id):
	conn = _database.connection()
	result = 0
	
	try:
		with conn.cursor() as cursor:
			sql = "UPDATE evaluate_game SET comment = NULL WHERE games_id = %s AND users_id = %s;"
			cursor.execute(sql, (game_id, user_id))
			result = cursor.fetchall()
			cursor.close()
	
	except Exception as e:
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result


def delete_rate(game_id, user_id):
	conn = _database.connection()
	result = 0
	
	try:
		with conn.cursor() as cursor:
			sql = "UPDATE evaluate_game SET rate = NULL WHERE games_id = %s AND users_id = %s;"
			cursor.execute(sql, (game_id, user_id))
			result = cursor.fetchall()
			cursor.close()
	
	except Exception as e:
		flash('The database is unavailable', 'error')
	
	finally:
		conn.close()
	
	return result
