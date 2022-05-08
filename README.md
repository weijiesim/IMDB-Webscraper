# Imdb Webscraping and Analysis
## Overview
This is a project that scrapes the imdb top 250 movies using BeautifulSoup, and pushes it to a Google MySQL Database. It also includes a python notebook that includes some exploratory data analysis, exploring the main factors that affect the gross earnings of movies.

## Installation
Clone this project from github then go to the folder of the files in your local and change directory to the cloned file.

## Installing requirements
`pip install -r requirements.txt`

## Setting up Google MySQL Database
Follow the instructions from this link https://cloud.google.com/sql/docs/sqlserver/create-manage-databases to set up Google MySQL account.<br> <mark>In your created instance, create a new database named **imdb**.</mark> 
<br>Choosing a different name for the database will require you to make adjustments in the code block connecting to the database in `database_setup.py`, at line 13, for the argument `database`.

## Running script to create table
`python database_setup.py` <br>
Enter Public IP Address, username, and password for created instance when prompted.

## Analysis
For the exploratory data analysis, view `analysis.ipynb`.