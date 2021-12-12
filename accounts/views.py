from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user

from accounts.forms import RegisterForm, LoginForm
from models import db, User, UserLoginHistory

accounts = Blueprint('accounts', __name__,
                     template_folder='templates',
                     static_folder='../assets')


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    """ Login Page """
    form = LoginForm()
    next_url = request.values.get('next', url_for('qa.index'))
    if form.validate_on_submit():
        print('now loading content ...')
        user = form.do_login()

        if user:
            # return to the home page
            flash('{}, welcome back'.format(user.nickname), 'success')
            return redirect(next_url)
        else:
            flash('Failed to login, please retry later','danger')

    # else:
    #     print(form.errors)
    return render_template('login.html', form=form, next_url=next_url)


@accounts.route('/logout')
def logout():
    """logout"""
    # The logic we used before
    # session['user_id'] = ''
    # g.current_user = None
    logout_user()
    flash('See you next time', 'success')
    return redirect(url_for('accounts.login'))


@accounts.route('/register', methods=['GET', 'POST'])
def register():
    """ Register """
    form = RegisterForm()
    if form.validate_on_submit():
        user_obj = form.register();
        if user_obj:
            flash('Registered, please login', 'success')
            return redirect(url_for('accounts.login'))
        else:
            flash('Fail to register', 'fail')

    return render_template('register.html', form=form)


@accounts.route('/mine')
def mine():
    """ Personal Space """
    return render_template('mine.html')
