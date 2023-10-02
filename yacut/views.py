import re
import string
import random

from flask import abort, flash, redirect, render_template

from . import app, db
from .constants import HOST, PATTERN
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id(length=6):
    characters = string.ascii_letters + string.digits
    short = ''.join(random.choice(characters) for _ in range(length))
    if not URLMap.query.filter_by(short=short).first():
        return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()

    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data
        if len(custom_id) == 0:
            custom_id = get_unique_short_id()
        if not re.fullmatch(PATTERN, custom_id):
            flash('Неудачный символ в короткой')
            return render_template('form.html', form=form)
        if URLMap.query.filter_by(short=custom_id).first():
            flash(f'Короткая ссылка занята {custom_id}')
            return render_template('form.html', form=form)
        url = URLMap(
            original=original,
            short=custom_id,
        )
        db.session.add(url)
        db.session.commit()
        flash(f'{HOST}{custom_id}')
        return render_template('form.html', form=form)
    return render_template('form.html', form=form)


@app.route('/<string:short>')
def redirect_url(short):
    url = URLMap.query.filter_by(short=short).first()
    if url is None:
        abort(404)
    return redirect(url.original)
