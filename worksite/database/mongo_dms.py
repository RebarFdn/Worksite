from pymongo import MongoClient, AsyncMongoClient # pyright: ignore[reportMissingImports]

uri:str = "mongodb://localhost:27017/"

client = MongoClient(uri) #MongoClient(uri)
async_client = AsyncMongoClient(uri) #AsyncMongoClient(uri)

#client.drop_database("project")
