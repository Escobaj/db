import app.models.database as _database


def search(query='', limit=3):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT * FROM elements_search WHERE name LIKE %s LIMIT %s;"
			cursor.execute(sql, ('%' + query + '%', limit))
			result = cursor.fetchall()
	
	finally:
		conn.close()
	
	return result


def getRandomElements(nb):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT * FROM elements WHERE picture IS NOT NULL ORDER BY RAND() LIMIT %s;"
			cursor.execute(sql, (nb))
			result = cursor.fetchall()
	
	finally:
		conn.close()
	
	return result


def getLastReview(nb):
	conn = _database.connection()
	
	try:
		with conn.cursor() as cursor:
			sql = "SELECT * FROM elements_evaluate ORDER BY created DESC LIMIT %s;"
			cursor.execute(sql, (nb))
			result = cursor.fetchall()
	
	finally:
		conn.close()
	
	return result

