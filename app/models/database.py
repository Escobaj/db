import pymysql.cursors


def connection():
	return pymysql.connect(host='localhost',
	                       user='root',
	                       password='1234',
	                       db='db')


def deconnection(conn):
	conn.close()