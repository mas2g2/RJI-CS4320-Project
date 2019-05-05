## Update Packages on Server

Note: This project is best run on Ubuntu 18.04

```sudo apt-get update && sudo apt-get dist-upgrade && sudo apt-get autoremove```

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

Install MySQL onto the serever:

```sudo apt-get install mysql-server mysql-client```

Start MySQL:

```sudo systemctl start mysql.service```

Run through the steps for secure installation:

```sudo mysql_secure_installation```

Steps of Installation:

```
Enter password for user root: TYPE CURRENT ROOT PASSWORD

VALIDATE PASSWORD PLUGIN can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough. Would you like to setup VALIDATE PASSWORD plugin?

Press y|Y for Yes, any other key for No: y

There are three levels of password validation policy:

LOW    Length >= 8
MEDIUM Length >= 8, numeric, mixed case, and special characters
STRONG Length >= 8, numeric, mixed case, special characters and dictionary file

Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG: 1
Using existing password for root.

Estimated strength of the password: 50 
Change the password for root ? ((Press y|Y for Yes, any other key for No) : n

 ... skipping.
By default, a MySQL installation has an anonymous user,
allowing anyone to log into MySQL without having to have
a user account created for them. This is intended only for
testing, and to make the installation go a bit smoother.
You should remove them before moving into a production
environment.

Remove anonymous users? (Press y|Y for Yes, any other key for No) : y
Success.


Normally, root should only be allowed to connect from
'localhost'. This ensures that someone cannot guess at
the root password from the network.

Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y
Success.

By default, MySQL comes with a database named 'test' that
anyone can access. This is also intended only for testing,
and should be removed before moving into a production
environment.


Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y
 - Dropping test database
Success.

 - Removing privileges on test database...
Success.

Reloading the privilege tables will ensure that all changes
made so far will take effect immediately.

Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y

```

To create database and tables run commands:

```sudo mysql -u root -p```
	
When in MySQL monitor create database with command:
	
Create Database:
	
```create database rjiDB```
	
Switch to Using that Database:
	
```use rjiDB```
	
Generate Tables:
	
```\. schema.sql```

## Databse Configuration and Connection

To create a user for the database server run commads:

```sudo mysql -u root -p```

When in MySQL monitor create database user with commands:

- ```GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' IDENTIFIED BY 'password';```

- ```FLUSH PRIVILEGES```

Go to directory ```/etc/mysql/mysql.conf.d``` and open file mysqld.cnf and change the bind_address to 0.0.0.0

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
