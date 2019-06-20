import pymongo

client = pymongo.MongoClient("mongodb://124.16.71.133:27017/")
files = client['test']['files']
nodes = client['test']['nodes']
users = client['test']['users']