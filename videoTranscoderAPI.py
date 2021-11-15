import os
import threading
import logging
import flask
from flask import request
from convert import convert_video
from queue import Queue
import time
from videoData import VideoFile
import configparser
from databaseAccess import DataBase
from util import get_table
from minioAccess import MinIoS3

app = flask.Flask(__name__)
app.config["DEBUG"] = False
# todo : move to cfg
# API host information
app_host = "0.0.0.0"
app_port = 5000

queue = Queue()
database = None


def converter_thread_function(q, db, minio):
    logging.info("Thread %s: starting")
    while True:
        if not q.empty():
            # get file from queue
            v_file = q.get()
            # update status
            v_file.change_status(VideoFile.PROCESSING_STATUS)
            db.update_db_status(v_file.name, VideoFile.PROCESSING_STATUS)
            # download video from s3 to convert
            minio.get_file(v_file.name)

            # convention based on current video quality
            to_convert = []
            converted_files = []
            if v_file.quality == "480p":
                to_convert.append("240")
                to_convert.append("360")
            else:
                to_convert.append("240")
            for qlt in to_convert:
                new_file_name = qlt + '_' + v_file.name
                rs = convert_video(v_file.name, new_file_name, qlt)
                converted_files.append(new_file_name)

            # upload all converted files
            for f in converted_files:
                minio.put_file(f)
                os.remove(f)
            os.remove(v_file.name)
            v_file.change_status(VideoFile.DONE_STATUS)
            db.update_db_status(v_file.name, VideoFile.DONE_STATUS)
            # print(rs)
        print("nothing to do")
        time.sleep(10)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Video Transcoding API</h1><p> This a simple video transcoding api with ffmpeg and flask" \
           "</br>" \
           "Use homepage/api/v1/convert?input=file to convert&q=current file quality (480p).</p>"


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


# http://127.0.0.1:5000/api/v1/test?input=inp.mp4&q=480p
@app.route('/api/v1/test', methods=['GET'])
def api_qtest():
    if 'input' and 'q' in request.args:
        inp = str(request.args['input'])
        qlt = str(request.args['q'])
    else:
        return "Error: No input field provided. Please specify an input."
    file = VideoFile(inp, qlt)

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

    # minio
    minio_cfg = config['MINIO']
    minio_endpoint = minio_cfg['Endpoint']
    minio_accessKey = minio_cfg['AccessKey']
    minio_secretKey = minio_cfg['SecretKey']
    minio_bucket = minio_cfg['Bucket']

    database = DataBase(db_path, db_name, db_collection)
    minio_s3 = MinIoS3(minio_endpoint, minio_accessKey, minio_secretKey, minio_bucket)
    converter_thread = threading.Thread(target=converter_thread_function, args=(queue, database, minio_s3))
    converter_thread.start()
    app.run(host=app_host, port=app_port)
