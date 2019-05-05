## Install : Flask, Python3, MySQL, Docker

To install run commands: 

```sudo apt install python3-pip```,
			 ```pip3 install Flask```,
			 ```pip3 install mysql-connector-python```

Link for installing Docker: https://docs.docker.com/install/

To install Docker 18.06 through terminal run command: 

```sudo snap install docker```

Uninstall older versions of docker with command:

```sudo apt-get remove docker docker-engine docker.io containerd runc```


## Clone Repository

To clone or download this project into your system run command:

```git clone https://github.com/mas2g2/RJI-CS4320-Project```


Note: Our project uses a system from another github repository called image-quality-assessment from user idealo, which is included in our repository. When editing any python script in this folder, your must rebuild a docker image after editing it. 

To build the docker image run: 

```docker build -t nima-cpu . -f Dockerfile.cpu```

Use the command above to build a docker image, since the image-quality-assessment code will be runninig on the docker image.


## Install MySQL and Create Databse

```sudo apt-get install mysql-server mysql-client```

```sudo systemctl start mysql.service```

```sudo mysql_secure_installation```

To create database and tables run commands:
	```sudo mysql -u root -p```
When in MySQL monitor create database with command:
	```create database rjiDB```
	```use rjiDB```
	```\. schema.sql``` //Creates tables


## Databse Configuration and Connection

To create a user for the database server run commads:
	```sudo mysql```

When in MySQL monitor create database user with commands:

- ```GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' IDENTIFIED BY 'password';```
- ```FLUSH PRIVILEGES```

Go to directory ```etc\mysql``` and open file my.cnf.fallback and change the bind_address to 0.0.0.0

To connect to database go to function login_page() and change credentials to connect to your database:

	- host : <URL of ec2 instance, example : "ec2-1-23-45-678.us-east-2.compute.amazonaws.com">
	- username : <your-username>
	- password : <your-password>
	- database : "rjiDB"

Note: It is highly recommended that you run this project on an ec2 instance

## Launch Project

To launch project run command: 

- ```sudo python3 app.py```
- Copy URL of ec2 instance and paste it on browser
