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
