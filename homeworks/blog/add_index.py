import MySQLdb

args = open('log.cfg', 'r').read().split();
conn = MySQLdb.connect(*args)
cursor = conn.cursor()
cursor.execute('use blog')
""""""""""""
cursor.execute("create INDEX idx_parent_id on comments(parent_id)")   
""""""""""""
conn.commit()
conn.close()



