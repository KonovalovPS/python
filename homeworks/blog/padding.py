import MySQLdb
import uuid
import random
import string
from blog import Community

args = open('log.cfg', 'r').read().split();

def connect():
    conn = MySQLdb.connect(*args)
    cursor = conn.cursor()
    cursor.execute('use blog')
    return conn, cursor
    
def close_connect(connection):
    connection.commit()
    connection.close()
    
def random_article():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters + ' '*20) for i in range(120))
   
def random_headline():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(25))

def add_users():
    conn, cursor = connect()
    cursor.execute("select count(*) from users")
    count = cursor.fetchone()[0]
    if count >= 1000:
        return
    with open('full_names.txt', 'r') as file:
        for line in file:
            login = line.strip()
            password = str(uuid.uuid4())
            name, surname = login.split()
            age = random.randint(7, 70)
            Community().add_user(login, password, name, surname, age)
    close_connect(conn)
    
def add_blogs():
    conn, cursor = connect()
    cursor.execute("select count(*) from blogs")
    count = cursor.fetchone()[0]
    if count >= 100:
        return
    cursor.execute("select count(*) from users")
    count_users = cursor.fetchone()[0]
    with open('countries.txt', 'r') as file:
        for line in file:
            name = line.strip()
            user_id = random.randint(0, count_users)
            Community().create_blog(name, user_id)
    
    close_connect(conn)
    
def add_posts():
    conn, cursor = connect()
    cursor.execute("select count(*) from posts")
    count = cursor.fetchone()[0]
    if count >= 1000:
        return
    for i in range(10000):
        headline = random_headline()
        text = random_article()
        blog_id = random.randint(1, 100)
        cursor.execute("SELECT user_id FROM blogs WHERE id = %s" % blog_id)
        user_id = cursor.fetchone()[0]        
        Community().create_post(headline, text, (blog_id,), user_id)
    close_connect(conn)
        
def add_comments():
    conn, cursor = connect()
    cursor.execute("select count(*) from comments")
    count = cursor.fetchone()[0]
    if count >= 1000:
        return
    cursor.execute("SELECT COUNT(*) from posts")
    count_posts = cursor.fetchone()[0]  
    for i in range(30000): 
        #create_comment(self, text, parent_id, parent, session_id=1):
        text = random_headline()
        parent_id = random.randint(1, 10000)
        user_id = random.randint(1, 1000)
        Community().create_comment(text, parent_id, 'post', user_id)
    count_comments = 30000
    for i in range(70000):
        text = random_headline()
        parent_id = random.randint(1, count_comments)
        user_id = random.randint(1, 1000)
        Community().create_comment(text, parent_id, 'comment', user_id)
        count_comments += 1
    close_connect(conn)
    
add_users()
add_blogs()
add_posts()
add_comments()