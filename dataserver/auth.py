import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from db import users

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return 'fail'

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    pass


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    pass


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    name = request.args.get('name')
    passwd = request.args.get('passwd')
    user = users.find_one({'name': name, 'passwd': passwd})
    if user:
        session.clear()
        session['user_id'] = user['id']
        return 'yes'
    else:
        return 'Incorrect'

    return 'ok'


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return 'ok'


