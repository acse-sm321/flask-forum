from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from utils import constants

db = SQLAlchemy()


class User(db.Model):
    """ User """
    __tablename__ = 'accounts_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
    username = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(64))
    password = db.Column(db.String(256), nullable=False)
    avatar = db.Column(db.String(256))

    status = db.Column(db.SmallInteger,
                       default=constants.UserStatus.USER_ACTIVE.value,
                       comment='User status')
    is_super = db.Column(db.SmallInteger,
                         default=constants.UserRole.COMMON.value)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)
    # profile = db.relationship('UserProfile')


class UserProfile(db.Model):
    """ User profile """
    __tablename__ = 'accounts_user_profile'
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(64), unique=True, nullable=False)
    real_name = db.Column(db.String(64))
    maxim = db.Column(db.String(128))
    sex = db.Column(db.String(16))
    address = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    user = db.relationship('User', backref=db.backref('profile', uselist=False))


class UserLoginHistory(db.Model):
    __tablename__ = 'accounts_login_history'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    username = db.Column(db.String(64), nullable=False)
    login_type = db.Column(db.String(32))
    ip = db.Column(db.String(32))
    ua = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    user = db.relationship('User', backref=db.backref('history_list', lazy='dynamic'))


class Question(db.Model):
    """ Question """
    __tablename__ = 'qa_question'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    title = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(256))
    img = db.Column(db.String(256))
    content = db.Column(db.Text, nullable=False)
    view_count = db.Column(db.Integer, default=0)
    is_valid = db.Column(db.Boolean, default=True)
    reorder = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    user = db.relationship('User', backref=db.backref('question_list', lazy='dynamic'))

    @property
    def comment_count(self):
        """ 评论数量 """
        return self.question_comment_list.filter_by(is_valid=True).count()

    @property
    def follow_count(self):
        """ 关注数量 """
        return self.question_follow_list.filter_by(is_valid=True).count()

    @property
    def answer_count(self):
        return self.answer_list.filter_by(is_valid=True).count()


class QuestionTags(db.Model):
    """ The tags under the question """
    __tablename__ = 'qa_question_tags'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    tag_name = db.Column(db.String(16), nullable=False)
    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    question = db.relationship('Question', backref=db.backref('tag_list', lazy='dynamic'))


class Answer(db.Model):
    """  Answers to the question """
    __tablename__ = 'qa_answer'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    content = db.Column(db.Text, nullable=False)
    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    user = db.relationship('User', backref=db.backref('answer_list', lazy='dynamic'))
    question = db.relationship('Question', backref=db.backref('answer_list', lazy='dynamic'))

    @property
    def love_count(self):
        """ count of likes """
        return self.answer_love_list.count()


class AnswerComment(db.Model):
    """ Comment to the answers"""
    __tablename__ = 'qa_answer_comment'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    content = db.Column(db.String(512), nullable=False)
    love_count = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default=True)
    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    reply_id = db.Column(db.Integer, db.ForeignKey('qa_answer_comment.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))

    user = db.relationship('User', backref=db.backref('answer_comment_list', lazy='dynamic'))
    answer = db.relationship('Answer', backref=db.backref('answer_comment_list', lazy='dynamic'))
    question = db.relationship('Question', backref=db.backref('question_comment_list', lazy='dynamic'))


class AnswerLove(db.Model):
    """ Likes to comments """
    __tablename__ = 'qa_answer_love'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))

    user = db.relationship('User', backref=db.backref('answer_love_list', lazy='dynamic'))
    answer = db.relationship('Answer', backref=db.backref('answer_love_list', lazy='dynamic'))
    question = db.relationship('Question', backref=db.backref('question_love_list', lazy='dynamic'))


class AnswerCollect(db.Model):
    """ Collected Answers """
    __tablename__ = 'qa_answer_collect'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_valid = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))

    user = db.relationship('User', backref=db.backref('answer_collect_list', lazy='dynamic'))
    question = db.relationship('Question', backref=db.backref('question_collect_list', lazy='dynamic'))
    answer = db.relationship('Answer', backref=db.backref('answer_collect_list', lazy='dynamic'))


class QuestionFollow(db.Model):
    """ Followed Questions """
    __tablename__ = 'qa_question_follow'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    created_at = db.Column(db.DateTime)
    is_valid = db.Column(db.Boolean, default=True, comment='Logical delete')
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))

    user = db.relationship('User', backref=db.backref('question_follow_list', lazy='dynamic'))
    question = db.relationship('Question', backref=db.backref('question_follow_list', lazy='dynamic'))
