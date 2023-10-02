import re

from flask import jsonify, request

from . import app, db
from .constants import PATTERN
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    if len(data['custom_id']) > 16:
        raise InvalidAPIUsage('Больше 16 символов')
    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage('Уже существует короткая ссылка')
    if data.get('custom_id') is None:
        data['custom_id'] = get_unique_short_id()
    if not re.fullmatch(PATTERN, data['custom_id']):
        raise InvalidAPIUsage('Неудачные символы')
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify({'url': url.to_dict()}), 201


@app.route('/api/id/<string:short_id>', methods=['GET'])
def get_short_id(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден')
    return jsonify({"url": url.original}), 200
