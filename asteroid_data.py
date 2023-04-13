from flask import Flask, request, send_file 
import redis
import json
import requests
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

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
    return redis.Redis(host= redis_ip, port=6379,db=0, decode_responses=True)
rd = get_redis_client()
rd2 = redis.Redis(host = os.environ.get("REDIS_HOST"), port=6379, db=1) 

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
            global json_data
            json_data = json.loads(rd.get('ast_data'))
            return 'Asteroid Data Posted\n'
        else:
            return 'Data failed to retrieve\n'


    if request.method == 'GET':
        try:
            json_data = json.loads(rd.get('ast_data'))
            return json_data
        except:
            return 'Data not found (use path /data with POST method to fetch it)\n'

    if request.method == 'DELETE':
        try:
            del json_data 
            rd.delete('ast_data')
            return 'Asteroid Data deleted\n'
        except NameError:
            return 'Data already deleted\n'
#Other Flask Routes Start Here

@app.route('/asteroids', methods=['GET'])
def asteroids() -> list:
    """
    Returns the whole data set
    Args:
        None    
    Returns:
        Returns a json formated list named asteroids of all names of the asteroids in the data set
    """
    try:
        asteroids = []
        json_data = data() 
        for x in range(len(json_data)):
            asteroids.append(json_data[x]['name'])
        return asteroids
    except:
       return 'Data not found (use path /data with POST method to fetch it)\n'

@app.route('/asteroids/<string:ast_name>', methods=['GET'])
def spec_ast(ast_name: str) -> dict:
    """
    Gets the asteroids data from a specific name given
    Args:
        ast_name - the name of the asteroid to pull data from
    Returns:
        a dictionary (ast_data) containing all data pertaining to a specific asteroid
    """
    try:

        json_data = data()
        for a_name in json_data:
            if a_name['name']  == ast_name:
                return a_name

        raise TypeError
    except TypeError:
        return f'invalid asteroid name or no data found with error\n'

@app.route('/image', methods=['GET','DELETE','POST'])
def image():
    if request.method == 'POST':   
        try:
            plot_data = json.loads(rd.get('ast_data'))
            H = []
            name = []
            counter = 0 
            sorted_data = sorted(plot_data, key=lambda x: float(x['H']), reverse=False) 
            for counter in range(len(sorted_data)): 
                H.append(sorted_data[counter]['H'])
                name.append(sorted_data[counter]['name']) 
                if counter == 10: 
                    break 
            plt.figure(figsize=(10,10))
            plt.scatter(name,H) 
            plt.xlabel('Names of asteroid') 
            plt.ylabel('H (Brightness)') 
            plt.title('Lowest 10 Brightness of the asteroids')
            plt.savefig('asteroid_graph.png')
            file_bytes = open('./asteroid_graph.png', 'rb').read()
            rd2.set('key', file_bytes)
            return "Image is posted\n" 
        except TypeError: 
            return "Make sure the data has been posted\n" 
        except NameError:
            return "Make sure the data has been posted\n"

    if request.method == 'GET':
        try:
            path = './asteroid_graph.png'
            with open(path, 'wb') as f: 
                f.write(rd2.get('key'))
            return send_file(path, mimetype='image/png', as_attachment=True) 
        except TypeError:
            return "Post the data first and then post the image to use this function\n"

    if request.method == 'DELETE': 
        rd2.delete('key') 
        return "Graph was deleted\n"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
