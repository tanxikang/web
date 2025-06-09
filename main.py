import bcrypt
from routes import app, db
from sqlalchemy import inspect

def init_db():
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('users'):
            from models.user import User
            from models.article import Article
            db.create_all()
            password_hashed = bcrypt.hashpw('123456'.encode(), bcrypt.gensalt())
            user = User(username='root', password=password_hashed.decode('utf-8'), fullname='Root', description='超级管理员2')
            db.session.add(user)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True, port=520)

