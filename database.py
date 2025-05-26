import sqlite3
import uuid
import hashlib
import os

class Database:
    def __init__(self, db_location=':memory:'):
        self.db_location = db_location
        self.connection = None
        self.cursor = None
        
        if self.db_location != ':memory:' and not os.path.exists(self.db_location):
            self.create_tables()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_location)
            self.cursor = self.connection.cursor()

        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def close(self):
        if self.connection:
            self.connection.close()

    def create_tables(self):
        try:
            self.connect()
            print("Criando tabelas")
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(50) NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    post_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    visibility TEXT NOT NULL CHECK (visibility IN ('public', 'private', 'banned', 'deleted')),
                    views INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS comments (
                    id TEXT PRIMARY KEY,
                    post_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(post_id) REFERENCES posts(id),
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            self.connection.commit()
            print("Tabelas criadas...")

        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")

        finally:
            self.close()

class User(Database):
    def register_user(self, username, name, email, password):
        user_id = str(uuid.uuid4())
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.connect()
            cmd = """
                INSERT INTO users (id, username, name, email, password_hash) VALUES (?, ?, ?, ?, ?)
            """
            
            self.cursor.execute(cmd, (user_id, username, name, email, password_hash))
            self.connection.commit()
            return True, user_id
        
        except sqlite3.Error as e:
            print(f"Erro ao inserir usuário: {e}")
            return False, e
        
        finally:
            self.close()

    def login_user(self, email, password):
        try:
            self.connect()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cmd = """
                SELECT 
                    id 
                FROM 
                    users
                WHERE
                    email = ? AND
                    password_hash = ?
            """
            self.cursor.execute(cmd, (email, password_hash))
            result = self.cursor.fetchone()

            if result:
                return True, result[0]
            
            return False, None

        except:
            return False, None

        finally:
            self.close()

    def get_username(self, user_id):
        try:
            self.connect()
            cmd = """
                SELECT username FROM users WHERE id = ?
            """
            self.cursor.execute(cmd, (user_id,))
            username = self.cursor.fetchone()
            if username:
                return True, username[0]
            else:
                return False, None
        except Exception as err:
            return False, str(err)
        finally:
            self.close()

class Post(Database):
    def insert_post(self, user_id, title, content, visibility='public'):
        post_id = str(uuid.uuid4())
        try:
            self.connect()
            self.cursor.execute('''
                INSERT INTO posts (post_id, user_id, title, content, visibility) VALUES (?, ?, ?, ?, ?)
            ''', (post_id, user_id, title, content, visibility))
            self.connection.commit()
            return post_id
        
        except sqlite3.Error as e:
            print(f"Erro ao inserir post: {e}")
            return None
        
        finally:
            self.close()

    def get_list_posts(self, db_user, page=1, per_page=20):
        try:
            self.connect()
            offset = (page - 1) * per_page
            cmd = '''
                SELECT 
                    post_id, user_id, title, content, created_at 
                FROM 
                    posts
                WHERE
                    visibility = "public"
                ORDER BY
                    created_at DESC
                LIMIT ? OFFSET ?
            '''
            self.cursor.execute(cmd, (per_page, offset))
            posts = self.cursor.fetchall()

            self.cursor.execute('''
                SELECT COUNT(*) FROM posts WHERE visibility = "public"
            ''')
            total_posts = self.cursor.fetchone()[0]
            total_pages = (total_posts + per_page - 1) // per_page

            data_final = []

            for post in posts:
                data_post = {
                    "id": post[0],
                    "user_id": post[1],
                    "username": db_user.get_username(post[1])[1],
                    "title": post[2],
                    "content": post[3][0:150],
                    "created_at": post[4]
                }
                data_final.append(data_post)

            return {
                "posts": data_final,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
                "total_posts": total_posts
            }
        
        except sqlite3.Error as e:
            print(f"Erro ao obter posts: {e}")
            return {
                "posts": [],
                "page": page,
                "per_page": per_page,
                "total_pages": 0,
                "total_posts": 0
            }
        
        finally:
            self.close()


    def get_post(self, post_id):
        try:
            self.connect()
            cmd = """
                SELECT 
                    user_id, title, content, created_at, update_at, views
                FROM 
                    posts
                WHERE
                    visibility = "public" AND
                    post_id LIKE ?
            """
            self.cursor.execute(cmd, (post_id))
            post = self.cursor.fetchone()

            data_post = {
                "user_id": post[0],
                "title": post[1],
                "content": post[2],
                "created_at": post[3],
                "update_at": post[4],
                "views": post[5]
            }

            return True, data_post

        except Exception as err:
            return False, str(err)
        
        finally:
            self.close()

class Comment(Database):
    def insert_comment(self, post_id, user_id, content):
        comment_id = str(uuid.uuid4())
        try:
            self.cursor.execute('''
                INSERT INTO comments (id, post_id, user_id, content) VALUES (%s, %s, %s, %s)
            ''', (comment_id, post_id, user_id, content))
            self.connection.commit()
            return comment_id
        
        except sqlite3.Error as e:
            print(f"Erro ao inserir comentário: {e}")
            return None
        
        finally:
            self.close()
