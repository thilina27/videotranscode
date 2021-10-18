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
        db_dict = {"name": f"{file_name}", "status": f"{VideoFile.ADDED_STATUS}"}
        return col.insert_one(db_dict)

    def get_data(self):
        db = self.db_client[self.db_name]
        col = db[self.db_collection]
        return col.find({}, {"_id": 0, "name": 1, "status": 1})

    def update_db_status(self, file_name, status):
        db = self.db_client[self.db_name]
        col = db[self.db_collection]
        query = {"name": f"{file_name}" }
        new_values = {"$set": {"status": f"{status}"}}
        col.update_one(query, new_values)
