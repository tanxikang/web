from models.article import Article
from routes import db 
from sqlalchemy import Select, func

class ArticleService:
    def get_article(self, id):
        return db.session.get(Article, id)
    
    def get_articles(self):
       query = Select(Article)
       return db.session.execute(query).scalars().all()
    
    def create_article(self, article:Article):
        existing_article = Article.query.filter_by(title=article.title).first()
        if existing_article:
            raise Exception(f'标题为{article.title}的文章已经存在')
        db.session.add(article)
        db.session.commit()

        return article
    
    def update_article(self, article: Article):
        exist_article = db.session.get(Article, article.id)
        if not exist_article:
            return article, '文章不存在！'
        query = Select(Article).where(Article.title == article.title, Article.id !=article.id)
        same_title_article = db.session.scalar(query)
        if same_title_article:
            return article, '同标题的文章已经存在！'

        exist_article.title = article.title
        exist_article.content = article.content
        exist_article.update_time = func.now()

        db.session.commit()

        return article, None

    def delete_article(self, article_id: int):
        article = db.session.get(Article, article_id)
        if article:
            db.session.delete(article)
            db.session.commit()
            return True, None
        else:
            return False, '要删除的文章不存在!'