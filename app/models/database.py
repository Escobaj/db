import pymysql.cursors


def connection():
	return pymysql.connect(host='localhost',
	                       user='root',
	                       password='1234',
	                       db='db',
	                       cursorclass=pymysql.cursors.DictCursor,
	                       autocommit=True)


def deconnection(conn):
	conn.close()