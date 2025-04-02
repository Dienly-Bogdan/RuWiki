import sqlite3
from article import Article

class Database:
    db_path = "database.db"

    @staticmethod
    def execute(sql_code: str, params: tuple = ()):
        conn = sqlite3.connect(Database.db_path)
        cursor = conn.cursor()
        cursor.execute(sql_code)

        conn.commit()

    @staticmethod
    def create_article_table():
        Database.execute("""
    CREATE TABLE IF NOT EXISTS articles(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        filename TEXT
    )
    """)
        

    @staticmethod
    def get_cursor():
        ...

    @staticmethod
    def save(article: Article):
        Database.execute("""   
    INSERT INTO articles (title, content, filename) VALUES(?, ?, ?)
    """, (article.title, article.content, article.photo ))

    @staticmethod
    def fetchall(sql_code: str):
        conn = sqlite3.connect(Database.db_path)

        cursor = conn.cursor()
        cursor.execute(sql_code)


        return cursor.fetchall()

    
    @staticmethod
    def get_all_articles():
        articles = Database.fetchall("SELECT * FROM articles;")


    @staticmethod
    def find_article_by_title():
        ...



class SimpleDatabase:
    articles = []

    @staticmethod
    def save(article: Article):
        if SimpleDatabase.find_article_by_title(article.title) is not None:
            return False
    
        SimpleDatabase.articles.append(article)
        return True
    
    @staticmethod
    def get_all_articles():
        return SimpleDatabase.articles
    
    @staticmethod
    def find_article_by_title(title: str):
        for article in SimpleDatabase.articles:
            if article.title == title:
                return article
        return None