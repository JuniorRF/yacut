import string
import random

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short is False:
            short = get_unique_short_id()
        if URLMap.query.filter_by(short=short).first() is not None:
            flash('Короткая ссылка занята')
            return render_template('form.html', form=form)
        url = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        flash(f'http://127.0.0.1:5000/{short}')
        return render_template('form.html', form=form)
    return render_template('form.html', form=form)


@app.route('/<string:short>')
def redirect_url(short):
    url = URLMap.query.filter_by(short=short).first()
    return redirect(url.original)
