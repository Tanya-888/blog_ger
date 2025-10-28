from flask import Blueprint, render_template, request
from controller.base import BaseController


controller = BaseController()
base_bp = Blueprint('base', __name__)


@base_bp.route("/", methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 4, type=int)

    data, has_next = controller.index(page=page, per_page=per_page)
    
    return render_template('blog/index.html', post_ids=data, has_next=has_next, page=page, username=request.request_user)


