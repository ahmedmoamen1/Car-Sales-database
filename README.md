# Car-Sales-database

## Getting Started
Make sure you follow the conditions:

- Use Terminal
```bash
git clone https//:www.github.com:ahmedmoamen1/Car-Sales-database.git
touch Car-Sales-database
```
- Through github download code
- Create mysql Databse server through any hosting website.(https://www.freemysqlhosting.net/)
- Or localhost by downloading a sql server and mysql workbench

## Libraries
Must download the follwoing libraries:
- beautifulsoup4 
- requests 
- pandas 
- selenium 
- selenium-stealth 
- mysql-connector-python 
- flask
- Code:
```bash
pip install beautifulsoup4 requests pandas selenium selenium-stealth mysql-connector-python flask
```

## Database Schema

The database has 7 tables:

- **Seller** table stores information about car sellers.
- **Car** table stores information about cars owned by sellers.
- **CarAdvert** table stores information about car advertisements created by sellers.
- **CarAdvert_features** table stores information about features of car advertisements.
- **User_buyer** table stores information about buyers.
- **User_buyer_intCars** table stores information about cars that a buyer is interested in.
- **Purchase** table stores information about car purchases made by buyers.

## Populateing the database

This program extracts data from a website using web scraping techniques. It uses the BeautifulSoup library for parsing HTML and the Requests library for making HTTP requests. It also uses the Selenium library to handle dynamically generated content and to perform actions on the webpage. The program extracts numerical data from the website and saves it to a CSV file. 

### How to use

1. Make sure you have the required libraries installed (BeautifulSoup, Requests, Selenium, Pandas).
2. Run the program by executing the following command: `python program_name.py`
3. The program will prompt you to enter a URL. Enter the URL of the website you want to scrape.
4. The program will then extract the data and save it to a CSV file.

## Webapp and databse connection

### SQL Reader code

The application provides the following functionalities:

- Register new users
- Add new car advertisements
- Purchase cars
- View car reviews and ratings
- Filter car advertisements by features and location
- View top 5 locations for a specific car make and model

### WebPage

1. Run the application with `python main.py`.
2. Navigate to `http://localhost:5000` in your web browser.
3. Register an account or log in with an existing account.
4. Search for cars using the search form on the home page.
6. View a seller's inventory by clicking on their name.
7. Leave a review or rating for a car you purchased by clicking on the "Add a review" button on the car's page.



