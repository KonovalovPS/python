CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(31) NOT NULL UNIQUE,
    password VARCHAR(63) NOT NULL,
    name VARCHAR(31) NOT NULL,
    surname VARCHAR(31) NOT NULL,
    age INTEGER NOT NULL
) ENGINE InnoDB;



INSERT INTO users (login, password, name, surname, age) values ('unknown',
                                                                'unknown',
                                                                'unknown',
                                                                'unknown',
                                                                0);
                                                          
CREATE TABLE IF NOT EXISTS blogs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(31) NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- CREATE TABLE IF NOT EXISTS articles (
    -- id INTEGER PRIMARY KEY AUTO_INCREMENT,
    -- headline VARCHAR(31) NOT NULL,
    -- text VARCHAR(2047)
-- );

-- CREATE TABLE IF NOT EXISTS posts (
    -- id INTEGER PRIMARY KEY AUTO_INCREMENT,
    -- article_id INTEGER NOT NULL,
    -- user_id INTEGER NOT NULL,
    -- blog_id INTEGER NOT NULL,
    -- FOREIGN KEY (article_id) REFERENCES articles(id),
    -- FOREIGN KEY (user_id) REFERENCES users(id),
    -- FOREIGN KEY (blog_id) REFERENCES blogs(id)
-- );

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    headline VARCHAR(31) NOT NULL,
    text VARCHAR(2047)
);

CREATE TABLE IF NOT EXISTS blogs_posts (
    blog_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    PRIMARY KEY (blog_id, post_id),
    FOREIGN KEY (blog_id) REFERENCES blogs(id) ON DELETE CASCADE,    
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    comment_text VARCHAR(511),
    user_id INTEGER,
    parent_id INTEGER,
    parent VARCHAR(7)
);