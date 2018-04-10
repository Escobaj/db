import app.models.database as _database


def search(query='', limit=3):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT * FROM elements_search WHERE name LIKE %s ORDER BY RAND() LIMIT %s;"
			cursor.execute(sql, ('%' + query + '%', limit))
			result = cursor.fetchall()
	
	finally:
		conn.close()
	
	return result
