import MySQLdb
from os import system

args = open('log.cfg', 'r').read().split(); 
conn = MySQLdb.connect(*args)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS blog")
cursor.execute("USE blog")

USERNAME = "root"
PASSWORD = "password"
DBNAME = "blog"
HOST = args[0]
FILE = "blog_database.sql"
command = """mysql -u %s -p"%s" --host %s %s < %s""" %(args[1], args[2], HOST, DBNAME, FILE)
system(command)

conn.commit()
conn.close()