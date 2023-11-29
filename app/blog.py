from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

import bleach

bp = Blueprint('blog', __name__)

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM posts p JOIN users u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/')
def index():
    db = get_db()
    posts = [dict(row) for row in db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM posts p JOIN users u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()]

    for post in posts:
        post['body'] = bleach.clean(post['body'], tags=['p', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'br', 'span', 'ol', 'ul', 'li'], attributes={'*': ['class']})

    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO posts (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('account.blogs'))


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()

    if post is None:
        abort(404)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['hiddenBody']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        elif post['author_id'] != g.user['id']:
            flash('You do not have permission to edit this post.', 'error')
        else:
            db.execute(
                'UPDATE posts SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('account.blogs'))

    elif post['author_id'] != g.user['id']:
        abort(403)

    return render_template('blog/edit.html', post=post)


@bp.route('/post/<int:post_id>')
def post(post_id):
    post = get_post(post_id, check_author=False)
    
    if post:
        return render_template('blog/post.html', post=post)
    else:
        return render_template('blog/not_found.html')


