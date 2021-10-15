import pymongo
import threading


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]


def t1():
    count = 0
    while count < 100:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        mycol = mydb["customers"]
        mydict ={ "name": f"Peter{count}", "address": "Lowstreet 27" }
        x = mycol.insert_one(mydict)
        count += 1

def t2():
    count = 0
    while count<100:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        mycol = mydb["customers"]
        mydict ={ "name": f"sam{count}", "address": "Lowstreet 27" }
        x = mycol.insert_one(mydict)
        count += 1

#x = threading.Thread(target=t1, args=())
#y = threading.Thread(target=t2, args=())
#x.start()
#y.start()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["videodatabase"]
mycol = mydb["convertions"]
x = mycol.delete_many({})
for x in mycol.find():
    print(x)