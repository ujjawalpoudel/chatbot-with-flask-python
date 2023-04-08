import pymongo

# Establish a connection to the MongoDB server
client = pymongo.MongoClient("mongodb+srv://ujjawal:lambton@cluster0.nxdac.mongodb.net/health")

# Select the database
db = client["mydatabase"]

# Select the collection
collection = db["mycollection"]

# Create a document
document = {"name": "John", "age": 30}

# Insert the document into the collection
result = collection.insert_one(document)

# Print the inserted document ID
print(result.inserted_id)
