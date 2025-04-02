from article import Article

class Database:
    articles = []

    @staticmethod
    def save(article: Article):
        if Database.find_article_by_title(article.title) is not None:
            return False
    
        Database.articles.append(article)
        return True
    
    @staticmethod
    def get_all_articles():
        return Database.articles
    
    @staticmethod
    def find_article_by_title(title: str):
        for article in Database.articles:
            if article.title == title:
                return article
        return None