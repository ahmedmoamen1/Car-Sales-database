CREATE DATABASE  IF NOT EXISTS carSale;
use carSale;

CREATE TABLE Seller(
Phone varchar(14),
Fname varchar(50),
Lname varchar(50),
date_joined DATE,
primary key(Phone)
);

CREATE TABLE Car(
Make varchar(50),
Model varchar(50),
Car_Year Year,
Phone varchar(14),
primary key(Make, Model, Car_year),
foreign key (Phone) references Seller(Phone)
);


CREATE TABLE CarAdvert(
AdId varchar(9),
car_make varchar(50),
car_model varchar(50),
car_year year,
Phone varchar(14),
odometer_rangeLow INTEGER,
odometer_rangeHigh INTEGER,
priceListed INTEGER,
body_type varchar(50) ,
fuel_type varchar(50) ,
Location varchar(50) ,
payment_method varchar(50) ,
color varchar(20) ,
CCLow  INTEGER,
CCHigh INTEGER,
transmission varchar(30) ,
car_descr varchar(10000),
primary key(AdId),
foreign key (Phone) references Seller(Phone)
);


CREATE TABLE CarADvert_features(
Feauture varchar(50) ,
AdId varchar(9),
primary key(AdId, Feauture),
foreign key (AdId) references CarAdvert(AdId)
);

CREATE TABLE User_buyer(
email varchar(50) ,
username varchar(50) ,
password varchar(50),
gender char(1) ,
Date_of_Birth DATE ,
primary key(email)
);

CREATE TABLE User_buyer_intCars(
car_make varchar(50) ,
car_model varchar(50) ,
car_year year,
email varchar(50) ,
primary key(car_make,car_model,email, car_year),
foreign key (email) references User_buyer(email)
);


CREATE TABLE Purchase(
email varchar(50) ,
AdId varchar(9),
priceBought INTEGER,
review varchar(200) ,
rating INTEGER Check(rating >=1 AND rating<= 5) ,
primary key(AdId, email),
foreign key (AdId) references CarAdvert(AdId),
foreign key (email) references User_buyer(email)
);
