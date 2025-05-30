from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    abort,
    flash,
    session)
import os
from article import Article
from database import Database


app = Flask(__name__)
app.config["SECRET_KEY"] = "dekou"
Database.create_tables()

# Создаем по умолчанию папку 'uploads/' для загрузки картинок
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html', error=request.args.get("error"))
    

    user_name = request.form.get("user_name")
    email = request.form.get("email")
    password = request.form.get("password")
    password_reapt = request.form.get("password_reapt")

    if not user_name:
        flash("Имя пользователя не может быть пустым!")
        return redirect(request.url)

    if not email:
        flash("Email не может быть пустым!")
        return redirect(request.url)

    if not password:
        flash("Password не может быть пустым!")
        return redirect(request.url)

    if not password_reapt:
        flash("Password не может быть пустым!")
        return redirect(request.url)

    if password != password_reapt:
        flash("Пароли не совпадают!")
        return redirect(request.url)
    
    saved = Database.register_user(user_name, email, password)
    if not saved:
        flash("Пользователем с таким user_name или почтой есть!!")
        return redirect(request.url)
    
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html', error=request.args.get("error"))
    user_name = request.form.get("user_name")
    password = request.form.get("password")

    if not Database.can_be_logged_in(user_name,password):
        flash("Такой пользователь не существует или нет такого пользователя")
        return redirect(request.url)
    
    session['user_id'] = Database.find_user_id_by_name_or_email(user_name)
    return redirect(url_for('index'))

@app.route("/logout", methods=["POST"])
def logout():
    if 'user_id' in session:
        session.clear()
    return redirect(url_for("index"))

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static/img'),
        'favicon.ico',
        mimetype="image/vnd.microsoft.icon"
    )


@app.route("/article/<title>")
def get_article(title):
    article = Database.find_article_by_title(title)
    if article is None:
        return "<h1>Такой статьи не существует!</h1>"

    return render_template(
        "article.html",
        article=article
        )


@app.route("/create_article", methods=["GET", "POST"])
def create_article():
    if request.method == "GET":
        return render_template('create_article.html', error=request.args.get("error"))
    
    # Далее обработка POST-запроса
    title = request.form.get("title")
    content = request.form.get("content")
    image = request.files.get("photo")
    
    if image is not None and image.filename:
        image_path = image.filename
        # Костыль: может вызвать проблемы с сохранением
        # картинок в папку
        image.save(app.config["UPLOAD_FOLDER"] + image_path)
    else:
        image_path = None

    auhtor = Database.find_user_by_id(session['user_id'])
    saved = Database.save(
        Article(title, content, image_path, auhtor=auhtor)
    )
    if not saved:
        return redirect(url_for('create_article', error=True))

    return redirect(url_for('index'))


@app.route("/delete_article/<id>", methods=["POST"])
def delete_article(id):
    if not Database.delete(id):
        abort(404, f"Article id {id} doesn't exist")
    
    return redirect(url_for('index'))


@app.route("/update_article/<id>", methods=["GET", "POST"])
def update_article(id):
    article = Database.find_article_by_id(id)
    if article is None:
        abort(404, f"Article id {id} doesn't exist")

    if request.method == "GET":
        return render_template("update_article.html", article=article)
    
    # Обработка POST-запроса
    title = request.form.get("title")
    if title is None:
        title = article.title

    content = request.form.get("content")
    if content is None:
        content = article.content

    image = request.files.get("photo")
    if image is not None and image.filename:
        # Если мы задали новую картинку для статьи,
        # ее надо сохранить в отдельную папку
        image_path = image.filename
        image.save(app.config["UPLOAD_FOLDER"] + image_path)

        filename = image_path
    else:
        # Если мы не задавали картинку для статьи,
        # то надо взять старую из объекта article
        filename = article.image

    Database.update(id, title, content, filename)
    return redirect(url_for('get_article', title=title))


@app.route("/")
@app.route("/index")
def index():
    articles = Database.get_all_articles()

    count_in_group = 4
    groups = []
    for i in range(0, len(articles), count_in_group): # 0, 4, 8, 12, ...
        groups.append(articles[i:i+count_in_group]) # [0:4], [4:8], [8:12], ...

    return render_template("index.html", groups=groups, user_count=Database.count_users())


@app.route('/uploads/<filename>')
def uploaded_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


app.run(debug=True, port=8088)
