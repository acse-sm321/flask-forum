from flask import Blueprint, render_template

accounts = Blueprint('accounts', __name__,
                     template_folder='templates',
                     static_folder='../assets')


@accounts.route('/login')
def login():
    """ Login Page """
    return render_template('login.html')


@accounts.route('/register')
def register():
    """ Register """
    return render_template('register.html')


@accounts.route('/mine')
def mine():
    """ Personal Space """
    return render_template('mine.html')

