from flask import jsonify, request
from marshmallow import ValidationError

from . import app, db
from .models import Opinion
from .validators import OpinionValidationSchema
from .views import get_random_opinion
from .error_handlers import InvalidAPIUsage


def get_opinion_from_id(id):
    opinion = Opinion.query.get(id)
    if not opinion:
        raise InvalidAPIUsage(
            'Мнение с таким id не найдено!',
            status_code=404
        )
    return opinion


# Явно разрешить метод GET.
@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    # Конвертировать данные в JSON и вернуть JSON-объект и HTTP-код ответа.
    return jsonify({'opinion': get_opinion_from_id(id).to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    opinion = get_opinion_from_id(id)

    try:
        valid_data = OpinionValidationSchema().load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

    for key, value in valid_data.items():
        setattr(opinion, key, value)

    db.session.commit()

    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    opinion = get_opinion_from_id(id)
    db.session.delete(opinion)
    db.session.commit()
    # При удалении принято возвращать только код ответа 204.
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    # Запросить список объектов.
    opinions = Opinion.query.all()
    if not opinions:
        raise InvalidAPIUsage('Нет мнений!')
    # Поочерёдно сериализовать каждый объект,
    # а потом все объекты поместить в список opinions_list.
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():

    try:
        valid_data = OpinionValidationSchema().load(request.json)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

    # Добавить новую запись в сессию.
    db.session.add(Opinion(**valid_data))
    # Сохранить изменения.
    db.session.commit()
    return jsonify({'opinion': valid_data}), 201


@app.route('/api/opinions/random/', methods=['GET'])
def random_opinion():
    opinion = get_random_opinion()
    if not opinion:
        raise InvalidAPIUsage('Нет мнений!')
    return jsonify({'opinion': opinion.to_dict()}), 200
