from flask import (Flask, 
                   render_template, 
                   request,
                   redirect,
                   url_for,
                   send_from_directory)
import os
from article import Article
from database import Database

app = Flask(__name__)
# Создаем по умолчани. папку uploads для загрузки картинок 
app.config['UPLOAD_FOLDER'] = "uploads/"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/article/<title>")
def get_article(title):
    
    article = Database.find_article_by_title(title)

    if article is None:
        return "<h1>Такой статьи не существует</h1>"

    return render_template("article.html", article=article)


@app.route("/create_article", methods=["GET", "POST"])
def create_article():
    if request.method == "GET":
        return render_template("created_article.html", error=request.args.get("error"))
    
    # Далее пост запрос
    title = request.form.get("title")
    content = request.form.get("content")
    photo = request.files.get("photo")


    if photo is not None and photo.filename:
        photo_path = photo.filename
        photo.save(app.config["UPLOAD_FOLDER"] + photo_path)
    else:
        photo_path = None

    saved = Database.save(Article(title, content, photo_path))
    if not saved:
        return redirect(url_for('create_article', error=True))

    return redirect(url_for("get_index"))


@app.route("/")
@app.route("/index")
def get_index():
    return render_template("index.html", articles=Database.get_all_articles())


@app.route("/uploads/<filename>")
def uploaded_photo(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


app.run(debug=True, port=8080)
