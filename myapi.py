import threading
import logging
import flask
from flask import request
from bson.json_util import dumps, loads
from convert import convert_video
from queue import Queue
import time
from videoData import VideoFile
from videoDownload import download_video
import configparser
from databaseAccess import DataBase
from util import get_table


app = flask.Flask(__name__)
app.config["DEBUG"] = True

queue = Queue()
database = None


def converter_thread_function(q, db):
    count = 0
    logging.info("Thread %s: starting")
    while True:
        if not q.empty():
            v_file = q.get()
            # no need
            v_file.change_status(VideoFile.PROCESSING_STATUS)
            db.update_db_status(v_file.name, VideoFile.PROCESSING_STATUS)
            download_video(v_file.location, v_file.name)
            rs = convert_video(v_file.name, str(count) + v_file.quality + '_' + v_file.name)
            v_file.change_status(VideoFile.DONE_STATUS)
            db.update_db_status(v_file.name, VideoFile.DONE_STATUS)
            # print(rs)
            count += 1
        # print("nothing to do")
        time.sleep(10)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Video Transcoding API</h1><p> This a simple video transcoding api with ffmpeg and flask" \
           "</br>" \
           "Use homepage/api/v1/convert?input=file to convert.</p>"


@app.route('/api/v1/convert', methods=['GET'])
def api_convert():
    # Check if an input provided in url
    if 'input' in request.args:
        input_file = str(request.args['input'])
    else:
        return "Error: No input field provided. Please specify an input."

    # if input found convert using ffmpeg
    result = convert_video(input_file)
    return result


# http://127.0.0.1:5000/api/v1/test?input=inp.mp4&id=CkSS7IuGRKo
@app.route('/api/v1/test', methods=['GET'])
def api_qtest():
    if 'input' and 'id' in request.args:
        inp = str(request.args['input'])
        db_id = str(request.args['id'])
    else:
        return "Error: No input field provided. Please specify an input."
    file = VideoFile(inp, db_id, "360")

    # data base insertion
    db_id = database.insert(file.name)
    file.id = db_id
    queue.put_nowait(file)
    return "file added to queue"


# http://127.0.0.1:5000/api/v1/vtest
@app.route('/api/v1/vtest', methods=['GET'])
def api_vtest():
    return get_table(database)


if __name__ == "__main__":

    # initialization
    config = configparser.ConfigParser()
    config.read('config.cfg')

    # database
    db_cfg = config['DATABASE']
    db_path = db_cfg['DBPath']
    db_name = db_cfg['DBName']
    db_collection = db_cfg['DBTable']

    database = DataBase(db_path, db_name, db_collection)

    converter_thread = threading.Thread(target=converter_thread_function, args=(queue, database,))
    converter_thread.start()
    app.run()
