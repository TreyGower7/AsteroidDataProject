from flask import Flask, request, send_file 
import redis
import json
import requests
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import math 
import xmltodict
import datetime
from jobs import rd, q, rdimg, rdjobs, add_job, generate_job_key
import jobs

app = Flask(__name__)

#Help Route
@app.route('/help', methods=['GET'])
def help() -> str:
    """Provides a manual for the user

    Args:
        None
    Returns:
        Help string with useful path data

    """
    get_help = """Usage:  curl [Localhost ip]:5000/[Path]\n
            A general utility for iss_tracking and paths\n
Path Options:\n

Paths:
           API Path:          Type:       Description of Path:\n 
            (1) /data           GET         Retrives all data for all asteroids\n
            (2) /data           POST        upload data to database\n
            (3) /data           DELETE      Deletes all data in the database\n
           Job Paths:\n
            (1) /jobs/graph   GET         Submits a job to the queue for graping data\n
            (1) /jobs/delete  DELETE      Delete a job from the queue for graping data\n


***End Help Section For Asteroid Stats***\n"""
    return get_help

#all the jobs stuff below

@app.route('/jobs', methods= ['POST','GET'])
def run_jobs():
    """
    This route post asteroids to be run
    args:
        None
    Query Parameters:
        ast_start: what asteroid to start with for the image data
        ast_end: what asteroid to end with for the image data
    Curl:
        "localhost:5000/jobs/graph?start=&end=" keep the parenthesis 
    Returns: 
        an added job to the queue
    """
    if request.method == "POST": 
        try:
            start = int(request.args.get('start', 0))
            end = int(request.args.get('end', 1000))
            if start < 300 or start > 1000 or end < 300 or end > 1000:
                return "There are no asteroids closer than 300 AU or farther than 1000 AU\n"
            if end < start:
                return "The farthest value is lower than the closest value, this can't happen try again with different values\n"
        except Exception as e:
            return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
        json.dumps(jobs.add_job(start, end))
        return f'Job submitted to the queue\n'
    else:
        return rdjobs.keys()

@app.route('/jobs/delete', methods=['GET','DELETE'])
def delete_job():
    if request.method =="DELETE":
        job = request.form['jid']
        keys = rdjobs.keys()
        if job in keys or job == "All": 
            if job == "All":
                rdjobs.flushdb()
                file_list = os.listdir('.')
                for item in file_list:
                    if item.endswith('.png'):
                        os.remove(item)
                return 'All jobs deleted\n'
            else:
                rdjobs.delete(job)
                if os.path.exists(f'{job}.png'):
                    os.remove(f'{job}.png')
            return f'Job {job} deleted\n'
        else:
            return 'Job id entered was not found\n'
    else:
        return "This is a route for DELETE-ing former jobs. Use the form: curl -X DELETE -d 'jid=asdf1234' localhost:5000/delete. Use -d 'jid=ALL' to delete all jobs.\n"



#end jobs stuff here

#Other Flask Routes Start Here

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
        url = 'https://raw.githubusercontent.com/TreyGower7/AsteroidDataProject/main/used-data/ModifiedAsteroidData.csv'
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            csv_data = csv.reader(response.text.splitlines())
            keys = next(csv_data)
            data = [dict(zip(keys, row)) for row in csv_data]
            rd.set('ast_data', json.dumps(data))
            return 'Asteroid Data Posted\n'
        else:
            return 'Data failed to retrieve\n'


    if request.method == 'GET':
        try:
            json_data = json.loads(rd.get('ast_data'))
            if json_data != {}:
                return json_data
        except:
            return 'Data not found (use path /data with POST method to fetch it)\n'

    if request.method == 'DELETE':
        try:
            rd.delete('ast_data')
            return 'Asteroid Data deleted\n'
        except NameError:
            return 'Data already deleted\n'

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
    ast_name= str.title(ast_name)
    try:
        json_data = data()
        for a_name in json_data:
            if a_name['name']  == ast_name:
                return a_name

        raise TypeError
    except TypeError:
        return f'invalid asteroid name or no data found with error\n'

@app.route('/<string:ast_name>/temp', methods=['GET'])
def temp(ast_name: str) -> dict:
    """
    Calculates Temperature of a specific asteroid
    args:
        ast_name which specifies an asteroid
    returns:
        A dictionary with the temperature of the asteroid and the units in kelvin
    """
    ast_name= str.title(ast_name)
    try:
        asteroid = spec_ast(ast_name)
        s_knot = 1376 #w/m^2
        albedo = float(asteroid['albedo'])  
        boltzman = 5.67 * (10**-8) 
        temp = float(((s_knot*(1-albedo))/(4*boltzman)) ** (1/4))   
        awnser = {'Temp': temp, 'units': "Kelvin"} 
        return awnser 
    except TypeError: 
        return "Make sure asteroid name is correct\n" 

@app.route('/<string:ast_name>/luminosity', methods=['GET'])
def lumin(ast_name: str) -> str:
    """
    Calculates Luminosity of a specific asteroid
    args:
        ast_name which specifies an asteroid
    returns:
        a string with the asteroids name and luminosity
    """
    ast_name= str.title(ast_name)
    try:
        asteroid = spec_ast(ast_name)
        s_knot = 1376 #w/m^2
        albedo = float(asteroid['albedo'])
        boltzman = 5.67 * (10**-8)
        temp = float(((s_knot*(1-albedo))/(4*boltzman)) ** (1/4))
        diameter = float(asteroid['diameter'])
        radius = diameter/2
        luminosity = 4*math.pi*(radius**2)*boltzman*(temp ** 4)
        return f'{ast_name} has a luminosity of {luminosity} Watts\n' 
    except TypeError:
        return "Make sure asteroid name is correct\n"

@app.route('/<string:ast_name>/visibility', methods=['GET'])
def visibility(ast_name: str) -> str:
    """
    Calculates the visibility of a specific asteroid based on the magnitude parameter H
    args:
        ast_name which specifies an asteroid
    returns:
        A string giving information on what device you need to see the asteroid
    """
    ast_name= str.title(ast_name)
    try: 
        asteroid = spec_ast(ast_name) 
        visible = float(asteroid['H'])  
        if visible <= 6.5:  
            return f'You can see {ast_name} with the naked eye if it was 10 parsecs away\n'
        elif visible > 6.5 and visible <=25: 
            return f'You can see {ast_name} with a regular telescope if it was 10 parsecs away\n' 
        elif visible > 25 and visible <= 32: 
            return f' You can see {ast_name} with the Hubble telescope if it was 10 parsecs away\n' 
    except TypeError: 
        return "Make sure asteroid name is correct\n" 

@app.route('/<string:ast_name>/power/<string:country>', methods=['GET'])
def power(ast_name: str, country:str) -> str:
    """
    Calculates power output of a specific asteroid and compares to powering a country
    args:
        ast_name which specifies an asteroid
    returns:
        A string detailing how many hours a specific asteroid could power a country
    """
    ast_name= str.title(ast_name)
    country= str.title(country)
    kwh = 0
    try:
        asteroid = spec_ast(ast_name)
    except TypeError:
        return "Make sure asteroid name is correct\n"
    try:
        url = 'https://raw.githubusercontent.com/TreyGower7/AsteroidDataProject/main/used-data/API_EG.USE.ELEC.KH.PC_DS2_en_xml_v2_5362092.xml'
        response = requests.get(url)
        if response.status_code == 200:
            data = xmltodict.parse(response.text)
    except TypeError:
        return "Power Data Currently Unavailable"
    try:
        s_knot = 1376 #w/m^2
        albedo = float(asteroid['albedo'])
        boltzman = 5.67 * (10**-8)
        temp = float(((s_knot*(1-albedo))/(4*boltzman)) ** (1/4))
        diameter = float(asteroid['diameter'])
        radius = diameter/2
        luminosity = 4*math.pi*(radius**2)*boltzman*(temp ** 4)
        power = luminosity/1000
        for x in range(len(data["Root"]["data"]["record"])):
            if kwh != 0:
                break
            if data["Root"]["data"]["record"][x]["field"][0]["#text"].find(country) != -1:
                if kwh == 0:
                    try:
                        kwh = data["Root"]["data"]["record"][x]["field"][3]["#text"]
                    except KeyError:
                        continue
        output = power/float(kwh)
        return f'the power generated by {ast_name} can power {data["Root"]["data"]["record"][x]["field"][0]["#text"]} for {output} hours\n'
    except ZeroDivisionError:
        return 'The country you specified does not have energy data. Try another country.\n'
@app.route('/<string:ast_name>/position', methods=['GET'])
def position(ast_name: str) -> dict:
    """
    Gives Keplerian Elements and the positional data from earth
    args:
        ast_name which specifies an asteroid
    returns:
        a dictionary of the elements
    """
    ast_name= str.title(ast_name)
    try:
        asteroid = spec_ast(ast_name)
        kepelements = {"Eccentricity": asteroid['e'], "Semimajor axis": asteroid['a'] , "Inclination": asteroid['i'], "Longitude of the ascending node": asteroid['om'] , "Argument of periapsis": asteroid['w'], "Distance from Earth (AU)": asteroid['moid_ld']}
        return {f"Keplerian Elements of {ast_name}": kepelements}
    except:
        return 'Make sure data is posted'

@app.route('/<string:ast_name>/compare/<string:ast2_name>', methods=['GET'])
def compare(ast_name: str, ast2_name: str) -> str:
    """
    Compares values of two asteroids
    args:
        ast_name and ast2_name which specify two asteroids
    returns:
        a string of comparable values
    """
    ast_name = str.title(ast_name) 
    ast2_name = str.title(ast2_name)  

    asteroid1 = spec_ast(ast_name)
    asteroid2 = spec_ast(ast2_name)
    s_knot = 1376 #w/m^2
    albedo1 = float(asteroid1['albedo'])
    albedo2 = float(asteroid2['albedo'])
    boltzman = 5.67 * (10**-8)
    temp1 = float(((s_knot*(1-albedo1))/(4*boltzman)) ** (1/4))
    temp2 = float(((s_knot*(1-albedo2))/(4*boltzman)) ** (1/4))

    diameter1 = float(asteroid1['diameter'])
    diameter2 = float(asteroid2['diameter']) 
    radius1 = diameter1/2
    radius2 = diameter2/2
    luminosity1 = 4*math.pi*(radius1**2)*boltzman*(temp1 ** 4)
    luminosity2 = 4*math.pi*(radius2**2)*boltzman*(temp2 ** 4)

    moid_ld1 = round(float(asteroid1['moid_ld']) * (1.496*(10**8))/9.461e+12,6) #light years 
    moid_ld2 = round(float(asteroid2['moid_ld']) * (1.496*(10**8))/9.461e+12,5) #light years

    if diameter1 >= diameter2:
        dia_diff = diameter1-diameter2
        dia_str = f'The diameter of {ast_name} is {dia_diff} Kilometers larger than {ast2_name}\n'
    else:
        dia_diff = diameter2-diameter1
        dia_str = f'The diameter of {ast2_name} is {dia_diff} Kilometers larger than {ast_name}\n' 

    if luminosity1 >= luminosity2: 
        lumin_diff = round((luminosity1-luminosity2)/1000,3)
        lumin_str = f'The luminosity of {ast_name} is {lumin_diff} Kilowatts higher than {ast2_name}\n' 
    else: 
        lumin_diff = round((luminosity2-luminosity1)/1000,3)
        lumin_str = f'The luminosity of {ast2_name} is {lumin_diff} Kilowatts higher than {ast_name}\n'

    if temp1 >= temp2: 
        temp_diff = round(temp1-temp2,3)
        temp_str = f'The temprature of {ast_name} is {temp_diff} Kelvin higher than {ast2_name}\n' 
    else: 
        temp_diff = round(temp2-temp1,3)
        temp_str = f'The temprature of {ast2_name} is {temp_diff} Kelvin higher than {ast_name}\n'
    
    if moid_ld1 >= moid_ld2: 
        moid_diff = round((moid_ld1 - moid_ld2)/1.496e+8,6)
        moid_str = f'{ast2_name} is {moid_ld2} AU from earth and is {moid_diff} AU closer than {ast_name}\n'
    else: 
        moid_diff = ((moid_ld2 - moid_ld1)/1.496e+8) 
        moid_str = f'{ast_name} is {moid_ld1} AU from earth and is {moid_diff} AU closer than {ast2_name}\n'

    return dia_str + lumin_str + temp_str + moid_str 

@app.route('/jobs/<jobuuid>', methods=['GET'])
def get_job_output(jobuuid):
    bytes_dict = rd.hgetall(jobuuid)
    return json.dumps(bytes_dict, indent=4)

@app.route('/download/<job_id>', methods=['GET'])
def download(job_id: str) -> str:
    #try:
    path = './asteroid_graph.png'
    with open(path, 'wb') as f:
        f.write(rdimg.hget(job_id, 'image'))
        return send_file(path, mimetype='image/png', as_attachment=True)
    #except TypeError:
        return "Post the data first and then post the image to use this function\n"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
