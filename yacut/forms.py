from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, URL, Optional

from .constants import MIN_CHAR_LINK, MAX_CHAR_LINK


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
        validators=[Length(
            MIN_CHAR_LINK, MAX_CHAR_LINK, message='Обязательное поле'
        ), Optional()]
    )
    submit = SubmitField('Создать')
