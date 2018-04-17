from flask import abort
import app.models.database as _database


# permet de savoir si un couple utilisateur / password existe
def user_exist(username, password):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT COUNT(*) AS count, id FROM users WHERE username = %s AND password = MD5(%s)"
			cursor.execute(sql, (username, password))
			result = cursor.fetchone()
	
	finally:
		conn.close()
	
	return result


# cree un utilisateur
def create_user(username, password, first_name, last_name, email):
	conn = _database.connection()
	
	with conn.cursor() as cursor:
		sql = "INSERT INTO users (username, email, first_name, last_name, password) VALUE (%s, %s, %s, %s, MD5(%s));"
		cursor.execute(sql, (username, email, first_name, last_name, password))
		result = cursor.fetchone()
		conn.close()
	
	return result


# recupere les informations d'un utilisateur
def get_user(id):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT * FROM users WHERE id = %s"
			cursor.execute(sql, (id))
			result = cursor.fetchone()
			conn.close()
	except:
		abort(404)
	
	return result
