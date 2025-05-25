import sqlite3
import uuid
import hashlib

class Database:
    def __init__(self, db_name=':memory:'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def connect(self):
        try:
            self.connection = sqlite3.connect('database.db')
            self.cursor = self.connection.cursor()

        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def close(self):
        if self.connection:
            self.connection.close()

    def create_tables(self):
        try:
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
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    visibility TEXT NOT NULL CHECK (visibility IN ('public', 'private', 'banned', 'deleted')),
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
            self.cursor.execute('''
                INSERT INTO users (id, username, name, email, password_hash) VALUES (%s, %s, %s, %s, %s)
            ''', (user_id, username, name, email, password_hash))
            self.connection.commit()
            return user_id
        
        except sqlite3.Error as e:
            print(f"Erro ao inserir usuário: {e}")
            return None
        
        finally:
            self.close()

    def login_user(self, email, password):
        try:
            self.connect()
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            cmd = '''
                SELECT 
                    user_id 
                FROM 
                    users
                WHERE
                    email = %s,
                    password_hash %s
            '''
            self.cursor.execute(cmd, (email, password_hash,))
            result = self.cursor.fetchone()

            if result:
                return True, result[0]
            
            return False, None

        except:
            return True, None

        finally:
            self.close()

class Post(Database):
    def insert_post(self, user_id, title, content, visibility='public'):
        post_id = str(uuid.uuid4())
        try:
            self.cursor.execute('''
                INSERT INTO posts (id, user_id, title, content, visibility) VALUES (%s, %s, %s, %s, %s)
            ''', (post_id, user_id, title, content, visibility))
            self.connection.commit()
            return post_id
        
        except sqlite3.Error as e:
            print(f"Erro ao inserir post: {e}")
            return None
        
        finally:
            self.close()

    def get_list_posts(self, page=1, per_page=20):
        try:
            self.connect()
            offset = (page - 1) * per_page
            cmd = '''
                SELECT 
                    user_id, title, content, created_at 
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

            return {
                "posts": posts,
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
