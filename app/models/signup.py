import app.models.database as _database


def user_exist(username, password):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT COUNT(*) AS count FROM users WHERE username = %s AND password = MD5(%s)"
			cursor.execute(sql, (username, password))
			result = cursor.fetchone()[0]
	
	finally:
		conn.close()
	
	return result


def create_user(username, password, first_name, last_name, email):
	conn = _database.connection()
	
	with conn.cursor() as cursor:
		sql = "INSERT INTO users (username, email, first_name, last_name, password) VALUE (%s, %s, %s, %s, MD5(%s));"
		cursor.execute(sql, (username, email, first_name, last_name, password))
		result = cursor.fetchone()
		conn.close()
	
	return result