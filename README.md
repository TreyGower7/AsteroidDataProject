<a name="Mapping The Cosmos"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/TreyGower7/AsteroidDataProject">
  <img src=https://user-images.githubusercontent.com/70235944/231852260-a794b567-d60c-49fc-a2f6-a131ac7a8809.jpg
       alt="Logo" width="400" height="250">
    

<h3 align="center">Mapping The Cosmos</h3>

  <p align="center">
    Project Objective

The goal of this Asteroid project is to create a REST API with flask to store data into a redis database and generate cool asteroid statistics given data from https://github.com/TreyGower7/AsteroidDataProject/blob/main/ModifiedAsteroidData.csv



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  
1. [About The Asteroid Project](#about-the-asteroid-project)>
    - [The Files In This Repo](#the-files-in-this-repo)
    - [Built With](#built-with)
2. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Pulling a docker image](#pulling-a-docker-image)
    - [Building a docker image](#building-a-docker-image)
3. [Paths & Routes](#paths---routes)
4. [Usage](#usage)
5. [Kubernetes Deployment](#kubernetes-deployment)
    - [Using The Provided Image](#using-the-provided-image)
    - [Building Your Own Image and Adapting The yml](#building-your-own-image-and-adapting-the-yml)
    - [Running The Deployments](#running-the-deployments)
    - [Envirnomental variables](#envirnomental-variables)
6. [What the Important data says](#what-the-important-data-says)
7. [The API Can Run From Any Machine!](#the-api-can-run-from-any-machine-)
8. [Contact](#contact)
9. [Acknowledgments](#acknowledgments)
  
</details>



<!-- ABOUT THE PROJECT -->
## About The Asteroid Project
This project is based off of asteroid data found on https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset where we 
took values in the data set and computed some interesting properties. Using this data and constants pulled from astrophysics, we can do calculations such as checking the power output of an asteroid as compared to a country and see the hours of power that country can get. But, the main focus of this project was building the backend and front end of our application with REST API, Kubernetes, Docker, Concurrency and Queues, and much more detailed below.
    
### The Files In This Repo
***`Scripts:`***

`asteroid_data.py` -
python script contains and executes the `Flask`, `redis`, and python `requests` libraries functions. The script retrieves the data from the web at https://github.com/TreyGower7/AsteroidDataProject/blob/main/ModifiedAsteroidData.csv, then can be displayed with different paths that send http requests.

`jobs.py` -
 python script interacts with the `asteroid_data.py` api script to add, delete, or update from a `HotQueue` and `redis` database any graph creating jobs to be carried out.

`worker.py` -
python script takes all the data gathered from both the `asteroid_data.py` api and `jobs.py` scripts and does the work in the background to process and create the graph.

***`Docker Files:`***

`docker-compose.yml` -
saves the user (you) from having to type in tricky commands to run the docker image. Instead it wraps the information for the docker image into one file and runs it with a simple command.
    
`Dockerfile` -
is used to capture the docker image for `asteroid_data.py`, the file specifies the Python version, and installs any libraries used in the python script to run the application.

`Dockerfile.wrk` -
is used to capture the docker image for `worker.py`, the file specifies the Python version, and installs any libraries used in the python script to run the application.

***`Kubernetes Files:`***
    
  `asteroid-test-flask-service.yml` - Used to run the flask cluster (Runs all pods associated with the ip)
    
  `asteroid-test-flask-deployment.yml` - Provides declartive updates for flask api pods

  `asteroid-test-wrk-deployment.yml` - Provides declartive updates for worker pods
    
  `asteroid-test-redis-service.yml` - Used to run the redis cluster (Runs all pods associated with the ip)
    
  `asteroid-test-redis-deployment.yml` - Provides declartive updates for redis pods
    
  `asteroid-test-pvc.yml` - Persitant Volume Claim to store our data from the redis database with kubernetes

 `asteroid_nodeport_service.yml` - serves as the external entry point for incoming requests for the asteroid app

 `asteroid_ingress.yml` - Allows incoming curl commands to the pod from the public

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With
  <img src=https://user-images.githubusercontent.com/70235944/227825420-7601d2a1-d92f-4a0c-9726-92f4e65e7699.png alt="Logo" width="80" height="80">
  <img src=https://user-images.githubusercontent.com/70235944/227826270-c253f2a4-c294-4146-bb7d-17f9cf0e4f24.png alt="Logo" width="80" height="80">
  <img src=https://user-images.githubusercontent.com/70235944/227825491-6821ba07-4561-4f6b-8b72-62d53eab346b.png alt="Logo" width="80" height="80">
<img src=https://user-images.githubusercontent.com/70235944/234373495-83ac1167-d13f-4840-9c7e-ec3c8d96d4d9.png alt="Logo" width="80" height="80">
<img src=https://user-images.githubusercontent.com/70235944/234373487-dd6182f6-64ef-4451-b897-374fba0bdf69.png alt="Logo" width="80" height="80">
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Running this script is extremely easy using the docker and kubernetes files provided to you in this repository. We can either pull an already created image or build our own image.

### Prerequisites
***Docker must be installed on your machine in order to run the files provided in this repo***
1. Since most use Ubuntu here is a link to get docker up and running on your machine using Ubuntu: https://docs.docker.com/engine/install/ubuntu/

2. Clone the repo
   ```sh
   git clone https://github.com/TreyGower7/AsteroidDataProject.git
   ```
3. Make a data directory in the docker-src directory to store your data with redis
    ```sh
    mkdir data
    ```
    
## Pulling a docker image
1. docker pull request for api
   ```sh
   docker pull tagower/asteroid_stats:final   
   ```
    Output: <img width="627" alt="Screenshot 2023-03-27 at 8 14 47 PM" src="https://user-images.githubusercontent.com/70235944/234376326-1f6e0fa2-f5c9-4ede-ad36-f943382af907.png">

2. docker pull request for worker
   ```sh
   docker pull tagower/asteroid_worker:final   
   ```

3. Run Redis and Flask on ports 6379 and 5000 respectively
   ```sh
   docker-compose up -d
   ```
    Ouput: <img width="627" alt="Screenshot 2023-03-27 at 8 16 20 PM" src="https://user-images.githubusercontent.com/70235944/234376337-8ef62c5d-01b9-4d28-916c-31da29632ffe.png">

4. Run <a href="#Paths & Routes">Paths & Routes</a></li> or stop containers
  ```sh
  docker-compose down
  ```
    
## Building a docker image
1. Build the image for the api using included Dockerfile
```sh  
docker build -t <username>/asteroid_stats:<yourtag> -f Dockerfile .
```
2. Build the image for the worker using included Dockerfile.wrk
```sh  
docker build -t <username>/asteroid_worker:<yourtag> -f Dockerfile.wrk .
```
3. Check images were created
```sh  
docker images
```
4. Run the images and containers
```sh  
docker-compose up -d
```
5. Check Everything is running if you're paranoid
```sh  
docker ps -a
```
6. Run <a href="#Paths & Routes">Paths & Routes</a></li> or stop containers
  ```sh
  docker-compose down
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Paths & Routes -->
## Paths & Routes

| Api Paths | Method | 
| -------- | ----------- | 
| (1) /data|      `GET`         |
| Retrieves all data for all asteroids|
| (2) /data    |       `POST `       |
| Upload data to database        |
| (3) /data      |     `DELETE`      |
|Deletes all data in the database |
|(4) /asteroids   |   `GET`         |
| Retrieves all asteroid names in the database |
| (5) /asteroids/{ast_name} | `GET`         |
| Retrieves all data given a specific asteroid |


| Calculatory Paths | Method |
| -----------------|--------|
|(1) /{ast_name}/temp              |  `GET`         |
|Calculates tempurature of a specific asteroid |
|(2) /{ast_name}/lumin             |  `GET`         |
|Calculates luminosity of a specific asteroid |
|(3) /{ast_name}/visibility         | `GET`         |
|Calculates visibility of a specific asteroid |
|(4) /{ast_name}/compare/{ast2_name} | `GET`        |
|Compares properties of two given asteroids |
|(5) /{ast_name}/power/{country}   |   `GET`          |
|Calculates power supplied to a country from a specific asteroid |

| Job Paths | Methods |
| ----- | ----- |
|(1) /jobs      |     `GET `        |
|Retrieves job id's from the queue |
|(2) /jobs          | `POST`        |
|Submits a job to the queue for graping data |
|(3) /jobs/delete   | `DELETE`      |
|Delete a job from the queue for graping data |
|(4) /jobs/{jobid}  |  `GET`         |
|Retrieves data pertaining to a specific job id|
|(5) /download/{jobid}  | `GET`         |
|Downloads the image from the database |
<p align="right">(<a href="#readme-top">back to top</a>)</p>
 

<!-- USAGE EXAMPLES -->
## Usage
1. Main api or help route for all commands
    ```sh
    curl localhost:5000/
    ```
    or
    ```sh
    curl localhost:5000/help
    ```
2. Post the data to the redis database
    ```sh
    curl -X POST localhost:5000/data
    ```
      Output: Asteroid Data Posted
3. Get the data from redis in json format
    ```sh
    curl localhost:5000/data
    ```
      Output: **Outputs same as belows curl localhost:5000/asteroids/<asteroid_name> except returns all ids**
4. Delete the data from the redis database
    ```sh
    curl -X DELETE localhost:5000/data
    ```
      Output: Asteroid Data Deleted
5. Get all asteroids
    ```sh
    curl localhost:5000/asteroids
    ```
      Output: <img width="100" alt="Screenshot 2023-03-27 at 9 23 48 PM" src="https://user-images.githubusercontent.com/70235944/234381403-fd6da2a6-fab5-4319-b18a-d9bf0050b769.png">
6. Compare Asteroids temperature, luminosity, and visibility
    ```sh
    curl localhost:5000/<asteroid_name>/compare/<asteroid_name>
    ```
      Output: <img width="600" alt="Screenshot 2023-03-27 at 9 24 13 PM" src="https://user-images.githubusercontent.com/70235944/234655569-267fea33-9f67-4650-b021-7dd3ebe5381e.png">

7. Power that an Asteroid provides to a city
    ```sh
    curl localhost:5000/<asteroid_name>/power/<country>
    ```
  Output: <img width="600" alt="Screenshot 2023-03-27 at 9 24 13 PM" src="https://user-images.githubusercontent.com/70235944/234655734-0109a371-304f-480d-b229-94b916d55a5a.png">

8. Generate a job into a new redis database to plot data
    ```sh
    curl -X POST localhost:5000/jobs
    ```
  Output: 

  **Job submitted to the queue! Use this path using GET to see posted jobs**

9. Get Job id 
    ```sh
    curl localhost:5000/jobs
    ```
    Output: **All job ids in the jobs database**

10. Get the plots of data (graphs only viewable in jupyter notebook or as a png on local device)
    ```sh
    curl localhost:5000/download/<jobid> --output <desiredname>.png
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
  <!-- Kubernetes -->
## Kubernetes Deployment
***IMPORTANT: You must be in a kubernetes cluster for these steps***

***In the github repository you can find 8 .yml files beginning with asteroid-test to run the docker image***

### Using The Provided Image
1. docker pull request for api
   ```sh
   docker pull tagower/asteroid_stats:final   
   ```
2. docker pull request for worker
   ```sh
   docker pull tagower/asteroid_worker:final   
   ```
3. Refer below to 'Running Deployments' Section
  
### Building Your Own Image and Adapting The yml
***if building your own image it must be a docker image, which you can create following the steps in the 'Building a docker image' section***

1. Adapt the flask deployment files by changing these to the name of your image <your_username>/{image}:<image_tag>
<img width="401" alt="Screenshot 2023-04-06 at 12 17 00 AM" src="https://user-images.githubusercontent.com/70235944/234686123-69a33fa9-aae7-44f9-a434-040e8086017d.png">
<img width="401" alt="Screenshot 2023-04-06 at 12 17 00 AM" src="https://user-images.githubusercontent.com/70235944/234686120-fe5c2966-7a57-432f-b79a-9ef01f8816ea.png">

2. Everything else remains the same. Now refer to 'Running The Deployments' section below
  
  
### Running The Deployments
***For both Using and Building sections we need to make sure the files are up and running*** 

1. Find your python debugger in kubernetes and ensure its running
<img width="529" alt="Screenshot 2023-04-05 at 8 40 33 PM" src="https://user-images.githubusercontent.com/70235944/230251539-ea530e8a-510e-4c7e-a8e0-56e6a0b034aa.png">

2. To run the other containers taken from this github repo ***apply in this order**
  ```sh
  kubectl apply -f asteroid-test-pvc.yml
  ```
  ```sh
  kubectl apply -f asteroid-test-flask-service.yml
  ```
  ```sh
  kubectl apply -f asteroid-test-flask-deployment.yml
  ```
  ```sh
  kubectl apply -f asteroid-test-redis-service.yml
  ```
  ```sh
  kubectl apply -f asteroid-test-redis-deployment.yml
  ```
  ```sh
  kubectl apply -f asteroid-test-wrk-deployment.yml
  ```
  |**Special Instructions for nodeport service**|
  |---|
  ```sh
  kubectl apply -f asteroid_nodeport_service.yml
  ```
  **Then**
  ```sh
  kubectl get services
  ```
  **Copy the green boxed port**

  <img width="529" alt="Screenshot 2023-04-05 at 8 48 12 PM" src="https://user-images.githubusercontent.com/70235944/234687763-b1e125cc-33c4-4170-af54-5aaf06980531.png">
  
  **Now**

  ```sh
  vi asteroid_ingress.yml
  ```
  **Replace the port number with your port number**
  <img width="300" alt="Screenshot 2023-04-05 at 8 48 12 PM" src="https://user-images.githubusercontent.com/70235944/234688819-dc366b60-ff5f-47cd-9e6a-54f8e346c363.png">
  
  

3. After all that Check that they are running 
  ```sh
  kubectl get pods
  ```
<img width="529" alt="Screenshot 2023-04-05 at 8 48 12 PM" src="https://user-images.githubusercontent.com/70235944/234689447-3848a23e-8279-43cd-aeb7-f817d6e9d3a0.png">

4. Get the Cluster ip for the flask service and use it to run curl commands
  ```sh
  kubectl get services
  ```
  
  <img width="529" alt="Screenshot 2023-04-05 at 8 52 30 PM" src="https://user-images.githubusercontent.com/70235944/234689442-2b341b2c-8f0d-43dc-94b7-f57f983ae7c9.png">

5. Exec into your python debugger
  ```sh
  kubectl exec -it <your_python_debugger> -- /bin/bash
  ```
6. Run the curl commands provided in the 'Paths & Routes' or 'Usage Section' using your cluster ip
  ```sh
  curl <cluster_ip>:5000/<a_path>
  ```
### Envirnomental variables
  ***Note: we are now using environmental variables instead of hardcoded ip addresses. You still do not need to change any of the code whether you use the provided image or not. Heres what this looks like in some of the files:***

`asteroid_data.py:` 

<img width="350" alt="Screenshot 2023-04-13 at 2 29 55 PM" src="https://user-images.githubusercontent.com/70235944/231863940-301195ea-de0b-4a3e-b2da-d56215bf334c.png">

`docker-compose.yml:` 
  ```sh
  environment:
    - REDIS_IP=<The name of your container>
  ```
  ***mine uses REDIS_IP=asteroidproject_redis-db_1***
  
  `flask-deployment:` 
  ```sh
  env:
  - name: REDIS_IP
    value: <The name of your redis service>
  ```
  ***mine uses REDIS_IP="asteroid-test-redis-service"***
<p align="right">(<a href="#readme-top">back to top</a>)</p>
    
<!-- What the data says -->
## What the Important data says
|Parameter | Description |
| ---- | ----- |
|H |Absolute magnitude parameter (Illumination measured one astronomical unit (AU) from both the Sun and the observer)
|Diameter | Asteroids diameter (in km)
|Diameter Uncertainty       | Uncertainty in diameter
|Albedo | Geometric albedo (reflection of light off the asteroid)
|Epoch | Time (Julian day form)
    
***Most other data values correlate to other properties of the asteroid we do not need in this project***



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## The API Can Run From Any Machine!
**As long as you set up the Nodeport and Ingress in the Kubernetes Section, you are able to run the api's curl commands from any web browser or linux terminal**


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Trey Gower - goweryert@gmail.com

Jeet Patel - redhinesward@gmail.com

Jordan Burton - jordane.burton@gmail.com

Project Link: https://github.com/TreyGower7/AsteroidDataProject


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Jet Propulsion Laboratory of California Institute of Technology: [https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset]()
* "Electric Power Consumption" World Bank Open Data: 
[https://data.worldbank.org/indicator/EG.USE.ELEC.KH.PC]()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
