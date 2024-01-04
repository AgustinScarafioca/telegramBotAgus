from pymongo import MongoClient
from bson.binary import Binary

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['webstorage']
collection = db['monos']

# Read an image file
with open("C:/Agus/Fotos santi/santisdata/santi22.jpg", 'rb') as f:
    image_data = Binary(f.read())


# Insert the image data into MongoDB
image_record = {'name': 'santi22', 'data': image_data}
result = collection.insert_one(image_record)
print(f"Image inserted with ID: {result.inserted_id}")