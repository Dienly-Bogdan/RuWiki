from flask import Flask, render_template

app = Flask(__name__)

database = {
    "spacex": {"article_title": "SpaceX", "article_text": "SpaceX Crew-10 — планируемый десятый пилотируемый полёт американского космического корабля Crew Dragon компании SpaceX в рамках программы NASA Commercial Crew Program. Корабль доставит четырёх членов экипажа миссии Crew-10 и космических экспедиций МКС-72/73 на Международную космическую станцию (МКС). Запуск планируется провести 14 марта 2025 года[1].", "article_image": "spacex.jpg"},
    "enigma": {"article_title": "Enigma", "article_text": "**«Энигма»** (от нем. Änigma — загадка) — **переносная шифровальная машина**, использовавшаяся для шифрования и расшифрования секретных сообщений. 1 Первую версию роторной шифровальной машины запатентовал в 1918 году Артур Шербиус. 1 На основе конструкции первоначальной модели было создано целое семейство электромеханических роторных машин под тем же названием, которые применялись с 1920-х годов в сфере коммерческой и военной связи во многих странах мира, но наибольшее распространение получили в гитлеровской Германии во время Второй мировой войны. 1 Также существует **музыкальный проект Enigma**, созданный Мишелем Крету в 1990 году. 2 Музыка представляет собой форму музыки нью-эйдж с выраженными добавками эмбиента, пост-индастриала и духовной европейской музыки. 2 Кроме того, существует **телепрограмма «Энигма»**, которую с 2016 года ведёт Ирина Никитина на канале «Культура», где интервьюирует ведущих деятелей классической музыки", "article_image": "Enigma.jpg"},
    "redbull": {"article_title": "Red Bull GmbH", 
               "article_text": "Red Bull GmbH (рус. Ред Булл; red bull в переводе с англ. — «красный бык») — австрийская компания, производитель энергетических напитков (самым известным из них является одноимённый газированный напиток «Red Bull»). Широко известна как спонсор и организатор многочисленных спортивных соревнований в автоспорте, велоспорте, сноубординге, мотоспорте, киберспорте, футболе и других видах.", 
               "article_image": "redbull.jpg"}
}

@app.route("/article/<name>")
def get_article(name):
    
    if name not in database:
        return "<h1>Такой статьи не существует</h1>"

    article_details = database[name]
    return render_template("article.html", 
                           article_title=article_details["article_title"],
                           article_text=article_details["article_text"],
                           article_image=article_details["article_image"])

@app.route("/create_artical")
def created_article():
    return render_template("created_article.html")


@app.route("/")
@app.route("/index")
def get_index():
    return render_template("index.html")

app.run(debug=True, port=8080)