from flask import (
    Blueprint, request
)

from auth import login_required
from db import files, nodes

bp = Blueprint('blog', __name__)


@bp.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    f.save('chunks/' + f.filename)
    return 'ok'


@bp.route('/download', methods=['POST'])
def download():
    filename = request.args.get('filename')
    return filename
