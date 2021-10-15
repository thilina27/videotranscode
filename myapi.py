import threading
import logging
import flask
from flask import request
from bson.json_util import dumps, loads
from convert import convert_video
from queue import Queue
import time
from videoData import VideoFile
import pymongo

app = flask.Flask(__name__)
app.config["DEBUG"] = True

queue = Queue()


def converter_thread_function(q):
    count = 0
    logging.info("Thread %s: starting")
    while True:
        if not q.empty():
            v_file = q.get()
            # no need
            v_file.change_status(VideoFile.PROCESSING_STATUS)
            update_db_status(v_file.name, VideoFile.PROCESSING_STATUS)
            rs = convert_video(v_file.name, str(count) + v_file.quality + v_file.name)
            v_file.change_status(VideoFile.DONE_STATUS)
            update_db_status(v_file.name, VideoFile.DONE_STATUS)
            print(rs)
            count += 1
        print("nothing to do")
        time.sleep(10)


# data base updates
def update_db_status(file_name, status):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["videodatabase"]
    mycol = mydb["convertions"]

    myquery = { "name": f"{file_name}" }
    newvalues = { "$set": { "status": f"{status}" } }

    mycol.update_one(myquery, newvalues)


x = threading.Thread(target=converter_thread_function, args=(queue,))
x.start()


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


@app.route('/api/v1/test', methods=['GET'])
def api_qtest():
    if 'input' in request.args:
        inp = str(request.args['input'])
    else:
        return "Error: No input field provided. Please specify an input."
    file = VideoFile(inp, "C:/Exptr", "360")


    # data base insertion
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["videodatabase"]
    mycol = mydb["convertions"]
    mydict = {"name": f"{file.name}", "status": f"{VideoFile.ADDED_STATUS}"}
    id = mycol.insert_one(mydict)
    file.id = id
    queue.put_nowait(file)
    return "file added to queue"

@app.route('/api/v1/vtest', methods=['GET'])
def api_vtest():

    # data base view
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["videodatabase"]
    mycol = mydb["convertions"]
    x = mycol.find({},{ "_id": 0, "name": 1, "status": 1 })
    list_cur = list(x)

    # Converting to the JSON
    json_data = dumps(list_cur, indent = 3)
    return json_data


app.run()
