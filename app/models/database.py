import pymysql.cursors


def connection():
	return pymysql.connect(host='localhost',
	                       user='root',
	                       password='1234',
	                       db='db',
	                       cursorclass=pymysql.cursors.DictCursor,  # pour avoir le nom des champs
	                       autocommit=True)  # permet d'ajouter apres un insert


def deconnection(conn):
	conn.close()
