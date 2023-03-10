from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create-article', methods=['POST', 'GET']) # создаем запросы пост гет
def create_article():
    if request.method == "POST": #запрос пост
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)  # c охранение данных

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При дополнении возникла ошибка"  # ошибка а не черный экран
    else:
        return render_template("create-article.html")


@app.route('/posts')   # для просмотра всех даных в таблице
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articls=article)


@app.route('/posts/<int:id>')
def post_detail(id):
    acticle = Article.query.get(id)
    return render_template("post-detail.html", articls=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    acticle = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "При удалении возникла ошибка"


    @app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
    def post_update(id):
        article = Article.query.get(id)
        if request.method == "POST":
            title = request.form['title']
            intro = request.form['intro']
            text = request.form['text']

            try:
                db.session.commit()
                return redirect('/posts')
            except:
                return "При дополнении возникла ошибка"
        else:
            return render_template("post-update.html", article=article)


if __name__ == '__main__':
    app.run(debug=True)
