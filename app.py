from flask import Flask

from models import db
from accounts.views import accounts
from qa.views import qa
from utils.filters import number_split

app = Flask(__name__, static_folder='assets')
# load the configuration
app.config.from_object('conf.Config')

# init database
db.init_app(app)

# register the BluePrint
app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(qa, url_prefix='/')

# register the filter
app.jinja_env.filters['number_split'] = number_split

