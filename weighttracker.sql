create database weight_tracker;
use weight_tracker;

create table users(
	Username varchar(255),
	Email varchar(255),
	Password varchar(255),
	primary key(Username,Email)
);
