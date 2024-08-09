import hashlib
import time
import pymongo
from bson.objectid import ObjectId

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        # Update the connection string to use your online MongoDB instance
        self.client = pymongo.MongoClient("mongodb+srv://mthakore12:miru123@cluster0.iba1sa7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.db = self.client["malware_chain"]
        self.collection = self.db["blockchain"]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", self.calculate_hash(0, "0", time.time(), "Genesis Block"))

    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_index = latest_block.index + 1
        new_timestamp = time.time()
        new_hash = self.calculate_hash(new_index, latest_block.hash, new_timestamp, data)
        new_block = Block(new_index, latest_block.hash, new_timestamp, data, new_hash)
        self.chain.append(new_block)
        self.store_block(new_block)
        return new_block

    def store_block(self, block):
        block_data = {
            "index": block.index,
            "previous_hash": block.previous_hash,
            "timestamp": block.timestamp,
            "data": block.data,
            "hash": block.hash
        }
        self.collection.insert_one(block_data)

    def load_blockchain(self):
        cursor = self.collection.find().sort("index", pymongo.ASCENDING)
        for document in cursor:
            block = Block(document["index"], document["previous_hash"], document["timestamp"], document["data"], document["hash"])
            self.chain.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != self.calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
