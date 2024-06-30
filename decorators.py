from flask import session, redirect, url_for
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('auth.restricted'))
        return f(*args, **kwargs)
    return decorated_function


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('auth.login'))
            if not session.get('team4') and not session.get(permission):
                return redirect(url_for('auth.restricted'))  # Oder eine spezifische Fehlerseite
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Spezifische Decorators für jede Berechtigung


def team1_required(f):
    return permission_required('team1')(f)


def team2_required(f):
    return permission_required('team2')(f)


def team3_required(f):
    return permission_required('team3')(f)


def team4_required(f):
    return permission_required('team4')(f)