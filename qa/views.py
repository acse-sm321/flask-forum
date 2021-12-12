from flask import Blueprint, render_template, request, abort
from flask_login import login_required

from models import Question

qa = Blueprint('qa', __name__,
               template_folder='templates',
               static_folder='../assets')


@qa.route('/')
def index():
    """ Home Page """
    return render_template('index.html')


@qa.route('/follow')
def follow():
    """ Following """
    per_page = 20  # 20 following entries on each page
    page = int(request.args.get('page', 1))
    page_data = Question.query.filter_by(is_valid=True).paginate(
        page=page, per_page=per_page)
    return render_template('follow.html', page_data=page_data)


@qa.route('/write')
@login_required
def write():
    """ write a post/article """
    return render_template('write.html')


@qa.route('/detail/<int:q_id>')
def detail(q_id):
    """ detail of question """
    # 1. query the question
    question = Question.query.get(q_id)
    if not question.is_valid:
        abort(404)
    # 2. show the first answer
    answer = question.answer_list.filter_by(is_valid=True).first()
    return render_template('detail.html', question=question, answer=answer)
