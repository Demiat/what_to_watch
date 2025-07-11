from marshmallow import Schema, fields, validates_schema, ValidationError


class OpinionValidationSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=lambda s: len(s) > 0)
    text = fields.Str(required=True, validate=lambda s: len(s) > 0)
    source = fields.Str(required=False)
    added_by = fields.Int(required=True)

    # skip_on_field_errors=True - не запускать функцию, если ошибки в
    # базовой валидации полей
    @validates_schema(skip_on_field_errors=True)
    def check_title_and_text_length(self, data, **kwargs):
        """Дополнительный уровень логики валидации к стандартной полей."""
        if len(data['title']) < 3:
            raise ValidationError(
                'Заголовок должен быть не короче 3 символов.'
            )

        if len(data['text']) < 10:
            raise ValidationError(
                'Текст мнения должен быть не короче 10 символов.'
            )
