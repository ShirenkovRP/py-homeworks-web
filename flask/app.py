from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Создаем приложение
app = Flask(__name__)

# Иницилизация БД
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB")
db = SQLAlchemy(app)


# Создаем модель
class Advertisement(db.Model):
    __tablename__ = 'advertisement'

    advert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<advert_id %r>' % self.advert_id


# Добавляем модель в базу данных
db.create_all()


# Создаем routes
@app.route('/')
def home():
    return 'Домашнее задание к лекции «Flask»'


@app.route('/advert', methods=['POST'])
def post_advert():
    body = request.json
    advert = Advertisement(title=body.get("title"),
                           description=body.get("description"),
                           author=body.get("author"))
    db.session.add(advert)
    db.session.commit()
    return {'status': 201}


@app.route('/advert/<int:get_id>', methods=['GET'])
def get_advert(get_id):
    advert = Advertisement.query.filter_by(advert_id=get_id).first_or_404()
    return {"id": advert.advert_id,
            "title": advert.title,
            "description": advert.description,
            "created": advert.created,
            "author": advert.author
            }, {'status': 201}


@app.route('/advert/<int:patch_id>', methods=['PATCH'])
def patch_advert(patch_id):
    title = request.json
    Advertisement.query.filter_by(advert_id=patch_id).update(title)
    db.session.commit()
    advert_new = Advertisement.query.filter_by(advert_id=patch_id).first_or_404()
    return {"id": advert_new.advert_id,
            "title": advert_new.title,
            "description": advert_new.description,
            "created": advert_new.created,
            "author": advert_new.author
            }, {'status': 201}


@app.route('/advert/<int:del_id>', methods=['DELETE'])
def delete_advert(del_id):
    advert = Advertisement.query.filter_by(advert_id=del_id).first_or_404()
    db.session.delete(advert)
    db.session.commit()
    return {'status': 204}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
