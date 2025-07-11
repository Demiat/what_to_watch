from flask import jsonify, request
from marshmallow import ValidationError

from . import app, db
from .models import Opinion
from .validators import OpinionValidationSchema


# Явно разрешить метод GET.
@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    # Конвертировать данные в JSON и вернуть JSON-объект и HTTP-код ответа.
    return jsonify({'opinion': Opinion.query.get_or_404(id).to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    opinion = Opinion.query.get_or_404(id)

    try:
        valid_data = OpinionValidationSchema().load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in valid_data.items():
        setattr(opinion, key, value)

    db.session.commit()

    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    opinion = Opinion.query.get_or_404(id)
    db.session.delete(opinion)
    db.session.commit()
    # При удалении принято возвращать только код ответа 204.
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    # Запросить список объектов.
    opinions = Opinion.query.all()
    # Поочерёдно сериализовать каждый объект,
    # а потом все объекты поместить в список opinions_list.
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    # Получить данные из запроса в виде словаря.
    data = request.get_json()
    # Создать новый пустой экземпляр модели.
    opinion = Opinion()
    # Наполнить экземпляр данными из запроса.
    opinion.from_dict(data)
    # Добавить новую запись в сессию.
    db.session.add(opinion)
    # Сохранить изменения.
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201
