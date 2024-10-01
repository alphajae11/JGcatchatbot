from flask import Blueprint, render_template, request, Response, stream_with_context
from .utils.main_utils import process_chat

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/chat_stream', methods=['POST'])
def chat_stream():
    user_input = request.json['message']

    def generate():
        for token in process_chat(user_input):
            print(token)
            yield f"data: {token}\n\n"

    return Response(stream_with_context(generate()), content_type='text/event-stream')
