from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, URL, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Ссылка',
        validators=(
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректный URL')
        )
    )
    custom_id = StringField(
        'Предложить свою',
        validators=[Length(1, 16, message='Обязательное поле'), Optional()]
    )
    submit = SubmitField('Создать')
