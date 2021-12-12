import os


class Config(object):
    """ Project configuration file """
    # URI to MySQL database
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/flask_qa'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # flash, form wtf
    SECRET_KEY = 'abcdsacb12312'
    # upload root path
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'medias')
