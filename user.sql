create database userstable;
use userstable;

create table users(
	Username varchar(255),
	Email varchar(255),
	Password varchar(255),
	primary key(Username,Email)
);
