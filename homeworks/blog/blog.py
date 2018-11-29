import MySQLdb

class Community:
        
    args = open('log.cfg', 'r').read().split();
    
    def connect(self):
        conn = MySQLdb.connect(*self.args)
        cursor = conn.cursor()
        cursor.execute('use blog')
        return conn, cursor
        
    def close_connect(self, connection):
        connection.commit()
        connection.close()
        
    def add_user(self, login, password, name, surname, age):
        """Добавить пользователя"""
        conn, cursor = self.connect()
        cursor.execute("""SELECT EXISTS (SELECT * FROM users
                       WHERE login = '%s')""" % login)
        match = cursor.fetchone()
        if match[0] == True:
            print('Логин занят, попробуйте другой')
            return
        cursor.execute("""INSERT INTO users (login, password, name, surname, age)
                          values ('%s', '%s', '%s', '%s', %s)
                          """ % (login, password, name, surname, age) )
                       
        self.close_connect(conn)      
       
    def log_in(self, login, password):
        """Авторизоваться"""
        conn, cursor = self.connect()
        cursor.execute("""SELECT * FROM users
                       WHERE login = '%s' and password = '%s'""" % (login, password))
        result = cursor.fetchone()
        if result == None:
            print('Такого пользователя с таким паролем не существует')
            return
        print('Здравствуйте, {}'.format(result[3]))
        #self.user_id = int(result[0])
        #self.autorized_users.append(int(result[0]))
        self.close_connect(conn)
        session_id = int(result[0])
        return session_id
        
    def users_list(self):
        """Добавить пользователя"""
        conn, cursor = self.connect()
        cursor.execute('select name, surname from users')
        a = (cursor.fetchall())
        user_list = []
        for each in a:
            user_list.append('{} {}'.format(each[0], each[1]))
        print(user_list)
        self.close_connect(conn)
        return user_list
             
    def create_blog(self, name, session_id = 1):
        """Создать блог"""
        # if user_id == None:
            # print('Для создания блога вы должны авторизоваться')
            # return      
        conn, cursor = self.connect()
        cursor.execute("""SELECT EXISTS (SELECT * FROM blogs 
                       WHERE name = '%s')""" % name)
        match = cursor.fetchone()
        if match[0] == True:
            print('Название блога занято {}, попробуйте другой'.format(name))
            self.close_connect(conn)
            return
        cursor.execute("""INSERT INTO blogs (user_id, name) 
                       values('%s', '%s')
                       """ % (session_id, name))
        print('Блог {} создан'.format(name)) 
        self.close_connect(conn)
    
    def delete_blog(self, name, session_id=1):
        """Удалить блог"""
        conn, cursor = self.connect()
        if session_id == 1:
            print('Авторизуйтесь, чтобы удалить блог')
            self.close_connect(conn)
            return
            
        cursor.execute("SELECT name FROM blogs WHERE user_id = '%s'" % session_id)
        blog_names = []
        row = cursor.fetchone()
        while row != None:
            blog_names.append(row[0])
            row = cursor.fetchone()
        if name not in blog_names:
            print('У вас нет такого блога')
            self.close_connect(conn)
            return 
        cursor.execute("DELETE from blogs WHERE name = '%s'" % name)
        print('Блог {} удалён'.format(name))
        self.close_connect(conn)
        
    def show_blogs(self, session_id=None):
        """1. Получить список неудалённых блогов при session_id=None.
        2. Получить список неудалённых блогов,
        созданных авторизованным пользователем
        при соответствующем session_id"""
        conn, cursor = self.connect()
        if session_id == None:
            cursor.execute("SELECT name FROM blogs")
        elif type(session_id) is int:
            cursor.execute("""SELECT name FROM blogs
                           WHERE user_id = '%s'""" % session_id)
        else:
            print('Неподдерживаемый вид аргумента')
            self.close_connect(conn)
            return
        blog_names = []
        row = cursor.fetchone()
        while row != None:
            blog_names.append(row[0])
            row = cursor.fetchone()      
        print(blog_names)
        self.close_connect(conn)
        return blog_names
        
        
    def create_post(self, headline, text, tuple_blog_id, session_id=1):
        """Создать пост, связнный с одним или несколькими блогами"""
        conn, cursor = self.connect()
        cursor.execute("""INSERT INTO posts (headline, text)
                          values('%s', '%s')""" % (headline, text))
        for blog_id in tuple_blog_id:
            cursor.execute("""SELECT * FROM blogs WHERE id = %s and
                            user_id = '%s'""" % (blog_id, session_id))
            match = cursor.fetchone()
            if match == None:
                print('У вас нет такого блога')
            else:
                cursor.execute("""select * from posts
                                  where id = (select max(id) from posts)""")
                post_id = cursor.fetchone()[0]
                cursor.execute("""INSERT INTO blogs_posts (blog_id, post_id) values('%s', '%s')""" % (blog_id, post_id))
                print('Пост {} опубликован'.format(headline))
        self.close_connect(conn)
        
    def edit_post(self, post_id, session_id=1, new_headline=None, new_text=None):
        """Изменить Пост"""
        conn, cursor = self.connect()
        cursor.execute("""select bp.post_id
                       FROM users u JOIN blogs b ON u.id = b.user_id 
                       JOIN blogs_posts bp ON b.id = bp.blog_id 
                       JOIN posts p ON bp.post_id = p.id 
                       WHERE user_id = %s and post_id = %s""" % (session_id, post_id))
        match = cursor.fetchone()
        if match == None:
            print('У вас нет такого поста')
        else:
            if new_headline != None:
                cursor.execute("""UPDATE posts SET headline = '%s'
                               WHERE id = %s""" % (new_headline, post_id))
            if new_text != None:
                cursor.execute("""UPDATE posts SET text = '%s'
                               WHERE id = %s""" % (new_text, post_id))
        self.close_connect(conn)
        
    def delete_post(self, post_id, session_id=1):
        """Удалить пост"""
        conn, cursor = self.connect()
        cursor.execute("""select bp.post_id
               FROM users u 
               JOIN blogs b ON u.id = b.user_id 
               JOIN blogs_posts bp ON b.id = bp.blog_id 
               JOIN posts p ON bp.post_id = p.id 
               WHERE user_id = %s and post_id = %s""" % (session_id, post_id))
        match = cursor.fetchone()       
        if match == None:
            print('У вас нет такого поста')    
        else:
            cursor.execute("""DELETE from posts
                           WHERE id = %s""" % (post_id))    
        self.close_connect(conn)
        
    def create_comment(self, text, parent_id, parent, session_id=1):
        """Создать коммент"""
        conn, cursor = self.connect()
        if parent == 'post':
            cursor.execute("""select * from posts where id = %s""" % parent_id)
            post_exist = cursor.fetchone()
            if post_exist == None:
                print('Вы пытаетесь прокомментировать несуществующий пост')
        elif parent == 'comment':
            cursor.execute("""select * from comments where id = %s""" % parent_id)
            comment_exist = cursor.fetchone()
            if comment_exist == None:
                print('Вы пытаетесь прокомментировать несуществующий комментарий')
                self.close_connect(conn)
                return
        else:
            print('недопустимый вид родителя')
            self.close_connect(conn)
            return
        if session_id == 1:
            print('Авторизуйтесь, чтобы писать комментарии')
        else:
            cursor.execute("""select * from users where id = %s""" % session_id)
            user_exist = cursor.fetchone()
            if user_exist == None:
                print('Несуществующий пользователь')
            else:
                cursor.execute("""INSERT INTO comments 
                                (comment_text, user_id, parent_id, parent)
                                values('%s', %s, %s, '%s')
                                """ % (text, session_id, parent_id, parent))
        self.close_connect(conn)
        
    def show_user_comments(self, post_id, session_id):
        """получить список всех комментариев пользователя к посту"""
        conn, cursor = self.connect()
        cursor.execute("""SELECT * from comments WHERE parent_id = %s and parent = '%s'""" % (post_id, 'post'))
        comments_arr = []
        row = cursor.fetchone()
        while row != None:
            comments_arr.append(row[1])
            row = cursor.fetchone()
        self.close_connect(conn)
        print(comments_arr)
        return comments_arr
        
        
hl = 'AAAAOOOOOOuu'
text = '!!!!!!MOYA OBORONAAA'
comment_text = 'COMMMMMENT TEXT'

co = Community()
co.create_blog('Miami')
co.add_user('aaa', '0000','Pavel','Petrov', 23)
co.add_user('qqqqq', '0000','Pavel','Ivanov', 23)
session = co.log_in('aaa', '0000')
co.create_blog('Tashkent', session)
co.create_blog('Abidzhan', session)
#co.delete_blog('Adventures', session)
print('-'*70)
co.create_post(hl, text, (4, 3), session)
print('-'*70)
# co.edit_post(13, session, 'new_headline', 'NEW_TEXT')
# co.delete_post(13, session)
#co.users_list()
# print('-'*70)
#co.create_comment('MMMMMM', 4, 'comment', session)
co.show_user_comments(3, session)