import pymongo
from videoData import VideoFile
# todo: error handling


class DataBase:

    def __init__(self, db_path, db_name, db_collection):
        self.db_path = str(db_path)
        self.db_name = str(db_name)
        self.db_collection = str(db_collection)
        self.db_client = pymongo.MongoClient(self.db_path)

    def insert(self, file_name):
        db = self.db_client[self.db_name]
        col = db[self.db_collection]
        db_dict = {"name": f"{file_name}", "status": f"{VideoFile.ADDED_STATUS_TEXT}"}
        return col.insert_one(db_dict)

    def get_data(self):
        db = self.db_client[self.db_name]
        col = db[self.db_collection]
        return col

    def update_db_status(self, file_name, status):
        db = self.db_client[self.db_name]
        col = db[self.db_collection]
        query = {"name": f"{file_name}"}

        text_status = VideoFile.ADDED_STATUS_TEXT
        if status == VideoFile.PROCESSING_STATUS:
            text_status = VideoFile.PROCESSING_STATUS_TEXT
        elif status == VideoFile.DONE_STATUS:
            text_status = VideoFile.DONE_STATUS_TEXT

        new_values = {"$set": {"status": f"{text_status}"}}
        col.update_one(query, new_values)
