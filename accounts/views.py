from flask import Blueprint, render_template, flash, redirect, url_for

from accounts.forms import RegisterForm

accounts = Blueprint('accounts', __name__,
                     template_folder='templates',
                     static_folder='../assets')


@accounts.route('/login')
def login():
    """ Login Page """
    return render_template('login.html')


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
