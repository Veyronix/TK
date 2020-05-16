from flask import Flask, request, send_file, make_response
from flask import jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import send, emit
import video_converter
import uuid

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
# cors2 = CORS(socketio)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


@app.route("/convertVideo/<newFormat>", methods=["POST"])
def convertVideo(newFormat):
    if request.method == 'POST':
        f = next(iter(request.files.values()))

        tmp_filename = str(uuid.uuid4()) + '.' + video_converter.video_extension(f.filename)
        f.save(tmp_filename)

        converter_filename = video_converter.convert_video(newFormat, tmp_filename)

        new_file_name = video_converter.video_name(f.filename) + '.' + newFormat

        response = make_response(send_file(converter_filename, attachment_filename=new_file_name))
        response.headers['x-suggested-filename'] = new_file_name
        return response


@app.route("/editVideo/<operations>", methods=["POST"])
def simpleEditVideo(operations):
    if request.method == 'POST':
        f = next(iter(request.files.values()))
        filename = f.filename
        tmp_filename = str(uuid.uuid4()) + '.' + video_converter.video_extension(f.filename)
        f.save(tmp_filename)

        edited_filename = video_converter.simple_edit_video(tmp_filename, operations)

        response = make_response(send_file(edited_filename, attachment_filename=filename))
        response.headers['x-suggested-filename'] = filename
        return response


# @socketio.on('message')
# def handle_message(message):
#     print('received message: ' + message)
#
# @socketio.on('json')
# def handle_json(json):
#     send(json, json=True)
#
#
# @socketio.on('my event', namespace='/test')
# def test_message(message):
#     emit('my response', {'data': 'got it!'})


# @app.route("/")
# @cross_origin()
# def helloWorld():
#   return "Hello, cross-origin-world!"

if __name__ == '__main__':
    tmp = {}
    app.run()
    # socketio.run(app)
