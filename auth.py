from flask import Blueprint, request, redirect, url_for, session, render_template
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['logged_in'] = True
        session['username'] = username
        session['team1'] = user.team1
        session['team2'] = user.team2
        session['team3'] = user.team3
        session['team4'] = user.team4
        return redirect(url_for('views.home'))
    else:
        return "Login failed. Please try again.", 401
    

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.home'))


@auth.route('/restricted')
def restricted():
    return render_template('login_required.html')