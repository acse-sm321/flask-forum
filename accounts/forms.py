import hashlib

from flask import flash, request
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from models import User, db, UserProfile, UserLoginHistory
from utils import constants
from utils.validators import phone_required


class RegisterForm(FlaskForm):
    """ User registration"""
    username = StringField(label='Username',
                           render_kw={'class': 'form-control input-lg', 'placeholder': 'Please enter username'},
                           validators=[DataRequired('Please enter username'), phone_required])
    nickname = StringField(label='Nickname',
                           render_kw={'class': 'form-control input-lg', 'placeholder': 'Please enter nickname'},
                           validators=[DataRequired('Please enter nickname'),
                                       Length(min=2, max=20, message='Nickname length is between 2 to 20')])
    password = PasswordField(label='Password',
                             render_kw={'class': 'form-control input-lg', 'placeholder': 'Please enter password'},
                             validators=[DataRequired('Please enter password')])
    confirm_password = PasswordField(label='Confirm Password', render_kw={'class': 'form-control input-lg',
                                                                          'placeholder': 'Please confirm the password'},
                                     validators=[DataRequired('Please confirm password'),
                                                 EqualTo('password', message='Wrong password')])

    def validate_username(self, field):
        """check whether a duplicated username"""
        user = User.query.filer_by(username=field.data).first()
        if user:
            raise ValidationError('This username has been occupied.')
        return field

    def register(self):
        """ Registration """
        # get form info,add to db session, jump to success page
        username = self.username.data
        password = self.password.data
        nickname = self.nickname.data

        try:
            # encryption
            password = hashlib.sha256(password.encode()).hexdigest()
            user_obj = User(username=username, password=password, nickname=nickname)
            db.session.add(user_obj)
            profile = UserProfile(username=username, user=user_obj)
            db.session.add(profile)
            db.session.commit()
            # jump to new page
            flash('Registered, please login', 'success')
            return user_obj
        except Exception as e:
            print(e)
            return None


class LoginForm(FlaskForm):
    """ User Login"""
    username = StringField(label='Username',
                           render_kw={'class': 'form-control input-lg', 'placeholder': 'Please enter username'},
                           validators=[DataRequired('Please enter username'), phone_required])
    password = PasswordField(label='Password',
                             render_kw={'class': 'form-control input-lg', 'placeholder': 'Please enter password'},
                             validators=[DataRequired('Please enter password')])

    def validate(self):
        result = super().validate()
        username = self.username.data
        password = self.password.data
        if result:
            user = User.query.filer_by(username=username, password=password).first()
            if user is None:
                result = False
                self.username.errors = ['Wrong username or wrong password']
            elif user.status == constants.UserStatus.USER_IN_ACTIVE.value:
                result = False
                self.username.errors = ['Accuount is invalid due to some reason']
        return result

    def do_login(self):
        """Perform the user login process"""
        try:
            username = self.username.data
            password = self.passwor.data

            user = User.query.filer_by(username=username, password=password).first()
            # add this to the session, simulate the login
            # session['user_id'] = user.id
            login_user(user)
            # make log
            ip = request.remote_addr
            ua = request.headers.get('user-agent', None)
            obj = UserLoginHistory(username=username, ip=ip, ua=ua, user=user)
            db.session.add(obj)
            db.session.commit()
            return user
        except Exception as e:
            print(e)
            return None
