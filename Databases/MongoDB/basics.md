# Install MongoDB

## Step 1 - Ensure Docker is installed

Run this to check:

```
docker --version
```

## Step 2 - Create a persistent data directory

This folder on your host will hold MongoDB’s database files permanently.

```
mkdir -p ~/mongo-data
```

This directory will persist even if the container is deleted — you can reuse or inspect it anytime.

## Step 3 - Run MongoDB as a Docker container

Run this once to create the container:

```
docker run -d --name mongodb -p 27017:27017 -v ~/mongo-data:/data/db --restart always mongo:latest
```


* `-d` → run detached (in the background)
* `--name mongodb` → name of the container
* `-p 27017:27017` → expose MongoDB’s default port
* `-v ~/mongo-data:/data/db` → persist data to your VM (not just in the container)
* `--restart always` → automatically restart on reboot or crash
* `mongo:latest` → official MongoDB image with the latest tag

This is the Docker equivalent of a **systemctl-managed MongoDB service**.

## Step 4 - Verify mongoDB is running

Run the command:

```
docker ps
```

Expect an output like this:

```
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                                           NAMES
bd4adc31dce4   mongo:latest   "docker-entrypoint.s…"   34 minutes ago   Up 34 minutes   0.0.0.0:27017->27017/tcp, :::27017->27017/tcp   mongodb
```

## Step 5 - Test the connection

Now try connecting with your local Mongo shell or PyMongo:

**Mongo shell**:

```
docker exec -it mongodb mongosh
```

or if you have **mongosh on your VM**:

```
mongosh "mongodb://localhost:27017"
```

Executing the Mongo Shell results in an output like:

```
Current Mongosh Log ID:	6903769c27b3a6d84fce5f46
Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.8
Using MongoDB:		8.2.1
Using Mongosh:		2.5.8

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

------
   The server generated these startup warnings when booting
   ............................................
   ............................................
   ............................................
------
```

## Step 6 - Python Scripts

Create a folder to store your Python scripts , create a virtual environment, activate it and then, install the necessary packages (`pymongo`):

```
mkdir ~/Desktop/mongo-training
python -m venv venv
source venv/bin/activate
pip install pymongo
```

Create the script `insert_document.py`. Inside it, we create a database `db` named `test_database` and a collection `collection` named `test_collection` inside `test_database`. Finally, we insert one document with the method `insert_one()`:

```
from pymongo import MongoClient

# 1. Connect to the local Docker MongoDB
client = MongoClient("mongodb://localhost:27017")

# 2. Choose or create a database
db = client["test_database"]

# 3. Choose or create a collection
collection = db["test_collection"]

# 4. Example JSON dictionary to insert
data = {
    "title": "Prestige",
    "year": 2006,
    "rating": 8.5,
    "genres": ["Action", "Mystery", "Thriller"],
    "director": "Christopher Nolan"
}

# 5. Insert the document
result = collection.insert_one(data)

# 6. Print the inserted document’s unique ID
print(f"Document inserted with _id: {result.inserted_id}")
```

After running the script inside `venv` using the command `python3 insert_documents.py`, the output is something like this:

```
Document inserted with _id: 690378800e4fed436aadc6f9
```

We can verify that all works well by using the interactive shell of Docker container:

```
docker exec -it mongodb mongosh
```

Then, in Mongo Shell, hit the commands:

```
use test_database
```

The output verifies a database with such a name indeed exists:

```
switched to db test_database
test_database> 
```

Then, hit the command:

```
db.test_collection.find().pretty()
```

to verify that the collection named `test_collection` that was created with the Python script `insert_documents.py` exists as well:

```
[
  {
    _id: ObjectId('690378800e4fed436aadc6f9'),
    title: 'Prestige',
    year: 2006,
    rating: 8.5,
    genres: [ 'Action', 'Mystery', 'Thriller' ],
    director: 'Christopher Nolan'
  }
]
```

Finally, we can create a second Python script to get all the database names and the collection names inside the database `test_database`. Let's call this script `get_results.py`:

```
from pymongo import MongoClient

# 1. Connect to the local Docker MongoDB
client = MongoClient("mongodb://localhost:27017")

# 2. Choose or create a database
db = client["test_database"]

# 3. Choose or create a collection
collection = db["test_collection"]

all_dbs = client.list_database_names()
all_collections = db.list_collection_names()
print(f"All databases: {all_dbs}\nAll collections: {all_collections}")
```

The execution output in the console is:

```
All databases: ['admin', 'config', 'local', 'test_database']
All collections: ['test_collection']
```
