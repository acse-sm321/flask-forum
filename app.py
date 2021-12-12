from flask import Flask, session, g
from flask_login import LoginManager

from accounts.views import accounts
from models import db, User
from qa.views import qa
from utils.filters import number_split

app = Flask(__name__, static_folder='assets')
# load the configuration
app.config.from_object('conf.Config')

# init database
db.init_app(app)

# init the login form
login_manager = LoginManager()
login_manager.login_view = "accounts.login"
login_manager.login_message = "Please login"
login_manager.login_message_category = "danger"
login_manager.init_app(app)

# register the BluePrint
app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(qa, url_prefix='/')

# register the filter
app.jinja_env.filters['number_split'] = number_split


@app.before_request
def before_request():
    "If there is an user ID,then we map it to global"
    user_id = session.get('user_id', None)
    if user_id:
        user = User.query.get(user_id)
        # print(user)
        g.current_user = user


# use the Flask-login as new login method

@login_manager.user_loader()
def load_user(user_id):
    return User.query.get(user_id)
