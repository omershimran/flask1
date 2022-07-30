from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import  User
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("logged in!!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('wrong details!!!', category='error')
        else:
            flash('no user found', category='error')

    return render_template("logins/login.html", text="testing", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        print(firstname)
        print(password1)
        print(password2)

        user = User.query.filter_by(email=email).first()

        if user:
            flash('user already exist!!!!',category='error')
        elif len(email) < 3:
            flash("email is too short", category="error")
        elif len(firstname) < 2:
            flash("name is too short", category="error")
        elif len(password1) < 4:
            flash("password is too short", category="error")
        elif password2 != password1:
            flash("password does not match", category="error")
        else:
            new_user = User(first_name=firstname, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("added user")
            return redirect(url_for('views.home'))

    return render_template("logins/sign_up.html", text="testing", user=current_user)

