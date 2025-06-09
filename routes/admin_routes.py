from flask import Flask, flash, request
from flask import redirect, render_template, url_for
from forms.article_form import ArticleForm
from routes import app
from flask_login import login_required
from models.article import Article
from services.article_service import ArticleService
from sqlalchemy.exc import IntegrityError

@app.route('/createarticle.html', methods=['GET', 'POST'])
@login_required
def create_article_page():
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = Article()
        new_article.title = form.title.data
        new_article.content = form.content.data

        try:
            ArticleService().create_article(new_article)
            flash(f'发布文章完成', 'success')
            return redirect(url_for('home_page'))
        except IntegrityError as ie:
            flash(f'发布文章失败:文章标题已经存在', 'danger')
        except Exception as error:
            flash(f'发布文章失败:{error}', 'danger')


    return render_template('editarticle.html', form=form, is_edit=False)




@app.route('/editarticle/<article_id>.html', methods=['GET', 'POST'])
@login_required
def edit_article_page(article_id: str):
    form = ArticleForm()
    if request.method == 'GET':
        try:
            article = ArticleService().get_article(int(article_id))
            if not article:
                flash(f'获取文章信息失败:文章不存在', 'danger')
                return redirect(url_for('home_page'))
            else:
                form.title.data = article.title
                form.content.data = article.content
        except Exception as error:
            flash(f'获取文章信息失败:{error}', 'danger')
            return redirect(url_for('home_page'))

    if form.validate_on_submit():
        try:
            update_article = Article()
            update_article.id = int(article_id)
            update_article.title = form.title.data
            update_article.content = form.content.data

            article, error_msg = ArticleService().update_article(update_article)
            if error_msg:
                flash(f'修改文章失败:{error_msg}', 'danger')
            else:
                flash(f'修改文章完成', 'success')
                return redirect(url_for('home_page'))
        except Exception as error:
            flash(f'修改文章失败:{error}', 'danger')


    return render_template('editarticle.html', form=form, is_edit=True)
