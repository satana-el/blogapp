import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/change_password", methods=("GET", "POST"))
def change_password():
    if request.method == "POST":
        old = request.form["old"]
        new = request.form["new"]
        confirmation = request.form["confirmation"]
        error = None

        if not (old or new or confirmation):
            error = "Please fill the required fields"

        if error is None:
            db = get_db()
            user = db.execute(
                "SELECT * FROM users WHERE id = ?", (g.user['id'],)
            ).fetchone()

            if check_password_hash(user["password"], old):
                if new == confirmation:
                    db.execute(
                        "UPDATE users SET password = ? WHERE id = ?",
                        (generate_password_hash(new), g.user['id']),
                    )
                    db.commit()
                else:
                    error = "Passwords do not match."
            else:
                error = "Incorrect password."

        if error:
            flash(error)
            return redirect(url_for('auth.change_password'))

        return redirect(url_for('account.profile'))
    else:
        return render_template('auth/change_password.html')


@bp.route("/change_username", methods=("GET", "POST"))
def change_username():
    if request.method == "POST":
        password = request.form["password"]
        n_username = request.form["username"]
        error = None

        if not n_username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        db = get_db()

        if error is None:
            user = db.execute(
                "SELECT * FROM users WHERE id = ?", (g.user['id'],)
            ).fetchone()

            if check_password_hash(user["password"], password):
                try:
                    db.execute(
                        "UPDATE users SET username = ? WHERE id = ?",
                        (n_username, g.user['id']),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"User {n_username} is already registered."
            else:
                error = "Incorrect password."

        if error:
            flash(error)
            return redirect(url_for('auth.change_username'))

        return redirect(url_for('account.profile'))

    return render_template('auth/change_username.html')



@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username/password."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect username/password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")

