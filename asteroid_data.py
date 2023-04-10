from flask import Flask, request
import redis
import json
import requests
import os
import csv

app = Flask(__name__)

def get_redis_client():
    """
    Gets the redis client
    Args:
        None
    Returns:
        the redis client with host redis_host in order to interact and get from the os to work with docker and k8s
    """
    redis_ip = os.environ.get("REDIS_HOST")
    return redis.Redis(host= redis_ip, port=6379,db=0,decode_responses=True)
rd = get_redis_client()

@app.route('/data', methods=['GET', 'POST', 'DELETE'])
def data():
    """
    POST's (loads), GET's (returns), or DELETE's the data from HGNC from the redis database.
    Args:
        None
    Returns:
        Returns a json formated list of all the data in the data set
    """

    if request.method == 'POST':
        url = 'https://raw.githubusercontent.com/TreyGower7/AsteroidDataProject/main/ModifiedAsteroidData.csv'
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            csv_data = csv.reader(response.text.splitlines())
            keys = next(csv_data)
            data = [dict(zip(keys, row)) for row in csv_data]
            rd.set('ast_data', json.dumps(data))
            return 'Asteroid Data Posted'
        else:
            return 'Data failed to retrieve'


    if request.method == 'GET':
        try:
            json_data = json.loads(rd.get('ast_data'))
            return json_data
        except:
            return 'Data not found (use path /data with POST method to fetch it)'
    if request.method == 'DELETE':
        rd.delete('ast_data')
        return 'Asteroid Data deleted'

#Other Flask Routes Start Here


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
