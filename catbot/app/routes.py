from flask import Blueprint, render_template, request, Response, stream_with_context
from .utils.main_utils import chat_with_cat_bot
from .utils.cat_image import get_cat_image

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/chat_stream', methods=['POST'])
def chat_stream():
    user_input = request.json['message']

    def generate():
        for token in chat_with_cat_bot(user_input, get_cat_image):
            yield f"data: {token}\n\n"

    return Response(stream_with_context(generate()), content_type='text/event-stream')
