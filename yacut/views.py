import re


from flask import abort, flash, redirect, render_template

from . import app
from .constants import HOST, PATTERN
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()

    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data

        if not custom_id:
            custom_id = URLMap.get_unique_short_id()

        elif not re.fullmatch(PATTERN, custom_id) and not None:
            flash('Неудачный символ в короткой')
            return render_template('form.html', form=form)

        if URLMap.get_url(custom_id):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('form.html', form=form)

        url = URLMap(original=original, short=custom_id)
        URLMap.save(url)
        flash(f'{HOST}{custom_id}', 'url')
        return render_template('form.html', form=form)
    return render_template('form.html', form=form)


@app.route('/<string:short>')
def redirect_url(short):
    url = URLMap.get_url(short)
    if url is None:
        abort(404)
    return redirect(url.original)
