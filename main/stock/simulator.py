import random
from datetime import datetime, timedelta
from pymongo import MongoClient
import json
from bson import ObjectId


def connect_to_mongodb():
    client = MongoClient("mongodb://mongodb:27017/")

    db = client["stocks"]  

    collection = db["stocks_trade"] 

    return collection


def read_from_mongodb(user_id, timestamp=None, type='read', limit=10):
    collection = connect_to_mongodb()
    query={}
    if user_id:
        query['user']= user_id
    sort_key = 'user' 
    if type=='read':
        if timestamp:
            query['timestamp'] = {'$gte': timestamp.replace(second=0, microsecond=0).timestamp()}
            

        documents = collection.find(query).limit(limit)
    elif type=='poll':
        if timestamp:
            query['timestamp'] = timestamp.replace(second=0, microsecond=0).timestamp()
        
        documents = collection.find(query).limit(limit)
    return documents

def write_to_mongodb(data):
    collection = connect_to_mongodb()

    collection.insert_one(data)

def simulate_trader(initial_amount, num_minutes, num_users):
    all_data = []  
    
    for id in range(1, num_users+1):
        current_amount = initial_amount
        timestamp = datetime.now() - timedelta(minutes=10)
        user_data = []  
        
        for _ in range(num_minutes):
            price_change = random.uniform(-15, 15)
            current_amount += price_change
            data = {
                'user': id,
                'price': current_amount,
                'timestamp': timestamp.replace(second=0, microsecond=0).timestamp()
            }
            write_to_mongodb(data)
            data['_id'] = str(ObjectId())  
            user_data.append(data)
            
            timestamp += timedelta(minutes=1)
        all_data.append(user_data)
    
    
    with open('data.json', 'w') as outfile:
        json.dump(all_data, outfile)
