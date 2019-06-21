import pymongo

client = pymongo.MongoClient("mongodb://124.16.71.133:27017/")
files = client['cloud']['files']
nodes = client['cloud']['nodes']
users = client['cloud']['users']
chunks = client['cloud']['users']
