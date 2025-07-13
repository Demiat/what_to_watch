from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import OpinionForm
from .models import Opinion
from .dropbox import async_upload_files_to_dropbox


def get_random_opinion():
    quantity = Opinion.query.count()
    if not quantity:
        abort(500)
    offset_value = randrange(quantity)
    return Opinion.query.offset(offset_value).first()


@app.route('/')
def index_view():
    return render_template('opinion.html', opinion=get_random_opinion())


@app.route('/add', methods=['GET', 'POST'])
async def add_opinion_view():
    import time
    start = time.time()
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first() is not None:
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            title=form.title.data,
            text=text,
            source=form.source.data,
            images=await async_upload_files_to_dropbox(form.images.data)
        )
        db.session.add(opinion)
        db.session.commit()
        print('end: ', time.time() - start)
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)


@app.route('/opinions/<int:id>')
def opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)
