import app.models.database as _database


# recupere les elements qui match avec la requete
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


# recupere un nombre d'element de facon random entre tous les elements
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


# recupere les derniers elements qui on été noté.
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

