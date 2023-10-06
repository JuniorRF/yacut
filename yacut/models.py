import re
from datetime import datetime
import random

from . import db
from .constants import (HOST, VALID_SYMBOLS, PATTERN, GENERATE_CHAR_LINK,
                        MAX_CHAR_ORIGINAL, MAX_CHAR_LINK)
from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_CHAR_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_CHAR_LINK), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=HOST + self.short
        )

    @staticmethod
    def from_dict(data):
        return URLMap(original=data['url'], short=data['custom_id'])

    @staticmethod
    def save_api(data):
        if not data.get('custom_id'):
            data['custom_id'] = URLMap.get_unique_short_id()

        if URLMap.get_url(data['custom_id']):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.')

        if not re.fullmatch(PATTERN, data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        url = URLMap.from_dict(data)
        URLMap.save(url)
        return url

    @staticmethod
    def save(data):
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def get_url(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id(length=GENERATE_CHAR_LINK):
        short = ''.join(random.choices(VALID_SYMBOLS, k=length))
        if not URLMap.get_url(short):
            return short
