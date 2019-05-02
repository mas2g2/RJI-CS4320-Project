Install : Flask, Python3, MySQL, Docker

To install run commands: "sudo apt install python3-pip",
			 "pip3 install Flask",
			 "pip3 install mysql-connector-python"

Link for installing Docker: https://docs.docker.com/install/

To install Docker 18.06, run command: "sudo snap install docker"

Uninstall older versions of docker with command: "sudo apt-get remove docker docker-engine docker.io containerd runc"

To build docker image: docker build -t nima-cpu . -f Dockerfile.cpu

Note: Our project uses a project from another github repository called image-quality-assessment from user idealo.(
To clone this project run command "git clone https://github.com/idealo/image-quality-assessment"), when editing any python script in this folder, your must build a docker image after editing it. 
Use the command above to build a docker image, since this code will be runninig on the docker image.

To clone or download this project into your system run command:
			 "git clone https://github.com/mas2g2/RJI-CS4320-Project"

To create database and tables run commands:
	"sudo mysql"
When in MySQL monitor create database with command:
	"create database rjiDB"
	"use rjiDB"
	"\. schema.sql" //Creates tables

To create a user for the database server run commads:
	"sudo mysql"

When in MySQL monitor create database user with commands:
	"GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' IDENTIFIED BY 'password';"
	"FLUSH PRIVILEGES"

Go to directory "etc/mysql" and open file my.cnf.fallback and change the bind_address to 0.0.0.0

To connect to database go to line 36 in function login_page() and change name of host to:
	<URL of ec2 instance, example : "ec2-1-23-45-678.us-east-2.compute.amazonaws.com">

Note: It is highly recommended that you run this project on an ec2 instance

To launch project run command: 

- sudo python3 app.py
- Copy URL of ec2 instance and paste it on browser
