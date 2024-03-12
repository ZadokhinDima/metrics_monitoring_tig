from bson import json_util
from flask import Flask, jsonify, json, Response
from pymongo import MongoClient
from elasticsearch import Elasticsearch

app = Flask(__name__)

client = MongoClient('mongodb://admin:adminpassword@mongodb:27017/')
users_mongo = client.users

es = Elasticsearch(['elasticsearch'])

@app.route('/mongo-johns')
def mongo_johns():
    data = users_mongo.users.find({'$text': {'$search': 'John'}})
    data = list(data)
    json_data = json.dumps(data, default=json_util.default)
    return Response(json_data, mimetype='application/json'), 200

@app.route('/elastic-johns')
def elastic_johns():
    res = es.search(index="users", body={"query": {"match": {"name": "John"}}})
    data = [doc['_source'] for doc in res['hits']['hits']]
    return jsonify(data), 200

@app.route('/all-johns')
def all_johns():
    # Get the data from the MongoDB and Elasticsearch endpoints
    mongo_response, _ = mongo_johns()
    elastic_response, _ = elastic_johns()

    mongo_data = mongo_response.get_json()
    elastic_data = elastic_response.get_json()

    # Combine the data into a dictionary with two keys
    all_data = {
        'mongo_data': mongo_data,
        'elastic_data': elastic_data
    }

    # Return the combined data as JSON
    return jsonify(all_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)