from flask import render_template, jsonify

from . import app, db


class InvalidAPIUsage(Exception):
    """Класс исключения для API."""

    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(self)
        self.message = message,
        if status_code is not None:
            self.status_code = status_code

    def mess_to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_usage(error):
    return jsonify(error.mess_to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
