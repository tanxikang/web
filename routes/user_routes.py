from flask_login import current_user, logout_user
from forms.delete_article_form import DeleteArticleForm
from forms.login_form import LoginForm
from routes import app
from flask import redirect, render_template, abort, url_for
from services.article_service import ArticleService
from services.user_service import UserService
from flask import Flask, flash

@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def home_page():
    if current_user.is_authenticated:
        delete_article_form = DeleteArticleForm()
        if delete_article_form.validate_on_submit():
                if delete_article_form.validate_on_submit():
                    result, error_msg = ArticleService().delete_article(int(delete_article_form.article_id.data))
                    if result:
                        flash(f'删除文章成功', 'success')
                        return redirect(url_for('home_page'))
                    else:
                        flash(f'删除文章失败:{error_msg}', 'danger')

    articles = ArticleService().get_articles()
    
    if current_user.is_authenticated:
        return render_template('index.html',  articles=articles, delete_article_form=delete_article_form)
    
    return render_template('index.html',  articles=articles)


@app.route('/article/<article_id>.html')
def article_page(article_id):
    article = ArticleService().get_article(article_id)
    if article:
        return render_template('article.html', article=article)
    
    abort(404)
    

@app.route('/about.html')
def about_page():
    return render_template('about.html')

@app.route('/login.html', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        result = UserService().do_login(username=form.username.data, password=form.password.data)
        if result:
            flash(f'欢迎{form.username.data}回来', "success")
            return redirect(url_for('home_page'))
        else:
            flash("用户名或密码错误", "danger")
    return render_template('login.html', form=form)

@app.route('/logout.html')
def logout_page():
    if current_user.is_authenticated:
        logout_user()
        flash('成功注销当前登录', 'success')
    return redirect(url_for('home_page'))
   



