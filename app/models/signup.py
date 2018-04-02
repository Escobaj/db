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