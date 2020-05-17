import os
import threading
import uuid

from flask import Flask, request, send_file, make_response, jsonify
from flask_cors import CORS

import video_converter

app = Flask(__name__)
CORS(app)


# app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, cors_allowed_origins="*")
# cors2 = CORS(socketio)


# @sockets.route('/echo')
# def echo_socket(ws):
#     global open_sockets
#     user_uuid = str(uuid.uuid4())
#
#     open_sockets.update({user_uuid: {"state": "connected", "socket": ws}})
#     ws.send(str({'state': 'send_file', 'uuid': user_uuid}))
#
#     while not ws.closed:
#         pass
#
#     return 1

# while not ws.closed:
#     ws.send('twoja dupa')
#     message = ws.receive()
#     print(message)
#     ws.send(message)


@app.route("/convertVideo/<newFormat>", methods=["POST"])
def convertVideo(newFormat):
    global videos_status
    if request.method == 'POST':
        f = next(iter(request.files.values()))

        tmp_filename = str(uuid.uuid4()) + '.' + video_converter.video_extension(f.filename)
        f.save(tmp_filename)

        new_filename = str(uuid.uuid4())

        thread1 = threading.Thread(target=video_converter.convert_video,
                                   args=(newFormat, tmp_filename, new_filename, videos_status))
        thread1.start()

        # new_file_name = video_converter.video_name(f.filename) + '.' + newFormat
        #
        # response = make_response(send_file(converter_filename, attachment_filename=new_file_name))
        # response.headers['x-suggested-filename'] = new_file_name
        # return response
        return jsonify(uuid=new_filename)


@app.route("/editVideo/<operations>", methods=["POST"])
def simpleEditVideo(operations):
    global videos_status
    if request.method == 'POST':
        f = next(iter(request.files.values()))
        filename = f.filename
        tmp_filename = str(uuid.uuid4()) + '.' + video_converter.video_extension(f.filename)
        f.save(tmp_filename)

        new_filename = str(uuid.uuid4())

        videos_status.update({new_filename: False})

        thread1 = threading.Thread(target=video_converter.simple_edit_video,
                                   args=(tmp_filename, operations, new_filename, videos_status))
        thread1.start()
        # edited_filename = video_converter.simple_edit_video(tmp_filename, operations, new_filename)
        # edited_filename = "dc34be14-aa82-4608-9672-1c84cf8ef483.mp4"
        # filename = "dupa321.mp4"
        # response = make_response(send_file(edited_filename, attachment_filename=filename))
        # response.headers['x-suggested-filename'] = filename
        return jsonify(uuid=new_filename)


@app.route("/downloadVideo/<user_uuid>", methods=["POST"])
def downloadVideo(user_uuid):
    global videos_status
    if request.method == 'POST' and videos_status.get(user_uuid, False):
        for fname in os.listdir('.'):
            if fname.startswith(user_uuid):
                response = make_response(send_file("/backend/" + fname, attachment_filename=fname))
                response.headers['x-suggested-filename'] = fname
                return response
                # return send_file(fname)
    return "not found"


if __name__ == '__main__':
    # rabbit.receive()
    open_sockets = {}
    videos_status = {}
    app.run(host="0.0.0.0", debug=True)
    # socketio.run(app)
    # http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    # http_server.serve_forever()
