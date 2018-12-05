import MySQLdb
import uuid
import random
import string
from blog import Community
import datetime

args = open('log.cfg', 'r').read().split();

def func_time(func, s=''):
    def new_func(*args, **kwargs):
        print('`{}{}` started'.format(s, func.__name__))
        time1 = datetime.datetime.now()
        a = func(*args, **kwargs)
        time2 = datetime.datetime.now()
        time_func = (time2 - time1).total_seconds()
        print('`{}{}` finished in {}s'.format(s, func.__name__, time_func))
        return a
    return new_func

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
    
@func_time
def add_users():
    conn, cursor = connect()
    cursor.execute("select count(*) from users")
    count = cursor.fetchone()[0]
    if count >= 1000:
        return
    execute_str = """insert into users (login, password, name, surname, age)
                      values """
    with open('full_names.txt', 'r') as file:
        #insert into users (login, password, name, surname, age)
        #values ('q', 'qweqwe', 'dawd', 'awdawd', 12), ('a', 'z', 'd', 'aaa', 32);
        counter = 0
        for line in file:
            counter += 1
            login = line.strip()
            password = str(uuid.uuid4())
            name, surname = login.split()
            age = random.randint(7, 70)
            execute_str += f"('{login}', '{password}', '{name}', '{surname}', {age}),"
            if counter == 50:
                cursor.execute(execute_str[:-1] + ';')
                counter = 0
                execute_str = """insert into users (login, password, name, surname, age)
                              values """ 
        if counter != 0:
            cursor.execute(execute_str[:-1] + ';')
    close_connect(conn)
    
@func_time    
def add_blogs():
    conn, cursor = connect()
    cursor.execute("select count(*) from blogs")
    count = cursor.fetchone()[0]
    if count >= 100:
        return
    cursor.execute("select count(*) from users")
    count_users = cursor.fetchone()[0]
    execute_str = """insert into blogs (user_id, name)
                      values """
    with open('countries.txt', 'r') as file:
        counter = 0
        for line in file:
            counter += 1
            user_id = random.randint(0, count_users)
            name = line.strip()
            execute_str += f"('{user_id}', '{name}'),"
            if counter == 25:
                cursor.execute(execute_str[:-1] + ';')
                counter = 0
                execute_str = """insert into blogs (user_id, name)
                      values """
        if counter != 0:
            cursor.execute(execute_str[:-1] + ';')                        
    close_connect(conn)

@func_time    
def add_posts():
    conn, cursor = connect()
    cursor.execute("select count(*) from posts")
    count = cursor.fetchone()[0]
    if count >= 1000:
        return
    posts_execute_str = """insert into posts (headline, text)
                      values """
    bp_execute_str = """ insert into blogs_posts (blog_id, post_id)
                        values """

    for index in range(10000):
        headline = random_headline()
        text = random_article()
        blog_id = random.randint(1, 100)
        cursor.execute("SELECT user_id FROM blogs WHERE id = %s" % blog_id)
        user_id = cursor.fetchone()[0]
        posts_execute_str += f"('{headline}','{text}'),"
        bp_execute_str += f"('{blog_id}', '{index + 1}'),"
        if (index + 1) % 200 == 0:
            cursor.execute(posts_execute_str[:-1] + ';')
            cursor.execute(bp_execute_str[:-1] + ';')
            posts_execute_str = """insert into posts (headline, text)
                      values """
            bp_execute_str = """ insert into blogs_posts (blog_id, post_id)
                        values """
    if (index + 1) % 200 != 0:
        cursor.execute(posts_execute_str[:-1] + ';')
        cursor.execute(bp_execute_str[:-1] + ';')
    close_connect(conn)
        
@func_time
def add_comments():
    conn, cursor = connect()
    cursor.execute("select count(*) from comments")
    count = cursor.fetchone()[0]
    if count >= 1000:
        return
    cursor.execute("SELECT COUNT(*) from posts")
    count_posts = cursor.fetchone()[0]

    execute_str = """INSERT INTO comments 
        (comment_text, user_id, parent_id, parent)
        values """
    for index in range(30000): 
        text = random_headline()
        parent_id = random.randint(1, 10000)
        user_id = random.randint(1, 1000)
        #Community().create_comment(text, parent_id, 'post', user_id)
        execute_str += f"('{text}', '{user_id}', {parent_id}, 'post'),"
        if (index + 1) % 500 == 0:
            cursor.execute(execute_str[:-1] + ';')
            execute_str = """INSERT INTO comments
                          (comment_text, user_id, parent_id, parent)
                          values """
    if (index + 1) % 500 != 0:
        cursor.execute(execute_str[:-1] + ';')
        execute_str = """INSERT INTO comments 
        (comment_text, user_id, parent_id, parent)
        values """
    count_comments = 30000
    
    for index in range(70000):
        text = random_headline()
        parent_id = random.randint(1, count_comments)
        user_id = random.randint(1, 1000)
        count_comments += 1
        execute_str += f"('{text}', '{user_id}', {parent_id}, 'post'),"
        if (index + 1) % 500 == 0:
            cursor.execute(execute_str[:-1] + ';')
            execute_str = """INSERT INTO comments
                          (comment_text, user_id, parent_id, parent)
                          values """       
    if (index + 1) % 500 != 0:
        cursor.execute(execute_str[:-1] + ';')
    close_connect(conn)
    
add_users()
add_blogs()
add_posts()
add_comments()