from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import logging

logging.basicConfig(filename='activity.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def movie_runtime(runtime_string):
    '''
    Takes in movie runtime in string and returns movie runtime in minutes
    '''
    if 'hour' in runtime_string or 'hours' in runtime_string:
        if len(runtime_string.split()) < 4:
            return runtime_string
        return int(runtime_string.split()[0])*60 + int(runtime_string.split()[2])
    else:
        return int(runtime_string.split()[0]) # if movie is less than 1 hour
    
def movie(url):
    '''
    Takes in a movie url and returns the gross earnings, budget, and runtime of the movie in order in a list
    '''
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features='html.parser')
        result = []
        
        # Extract gross earnings
        earnings_element = soup.find('li', attrs={'data-testid':'title-boxoffice-cumulativeworldwidegross'})
        if earnings_element:
            gross_earnings = earnings_element.find(class_ = 'ipc-metadata-list-item__list-content-item').get_text()
            result.append(gross_earnings)
        else:
            result.append('NA')
        
        # Extract budget
        budget_element = soup.find('li', attrs={'data-testid':'title-boxoffice-budget'})
        if budget_element:
            movie_budget = budget_element.find(class_ = 'ipc-metadata-list-item__list-content-item').get_text().split()[0]
            result.append(movie_budget)
        else:
            result.append('NA')
            
        # Extract Runtime
        runtime_element = soup.find('li', attrs={'data-testid':'title-techspec_runtime'})
        if runtime_element:
            runtime_string = runtime_element.find(class_ = 'ipc-metadata-list-item__content-container').get_text()
            result.append(movie_runtime(runtime_string))
        else:
            result.append('NA')
                
        return result
    
    except Exception as e:
        logging.error(e)

def imdb(url):
    '''
    Takes in imdb url page and extracts movie name, movie year, movie link, imdb rating, number of user ratings, 
    gross earnings, budget, and runtime of all movies on the page.
    
    Returns a dataframe of all the information.
    '''
    
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features='html.parser')
        
        name = []
        year = []
        root_link = 'https://www.imdb.com'
        link = []
        imdb_rating = []
        num_rating = []
        gross = []
        budget = []
        runtime = []
        
        logging.info('Webscrapping started.')
        print('Webscrapping started.')
        
        # Scrapping Movie Titles
        for item in soup.find_all('td', class_ = 'titleColumn'):
            movie_list = item.get_text().split('.')[1].lstrip('\n').split()
            movie_list.pop() # remove year
            name.append(' '.join(movie_list))

        # Scrapping Movie Years
        for item in soup.find_all(class_ = 'secondaryInfo'):
            year.append(item.get_text().strip('()'))
            
        # Scrapping Movie Links
        for item in soup.find_all('td', class_ = 'posterColumn'):
            movie_link = root_link + item.find('a').get('href') 
            link.append(movie_link)
            # Scrapping Gross Earnings, Budget, Runtime
            result = movie(movie_link)
            gross.append(result[0])
            budget.append(result[1])
            runtime.append(result[2])
            
        # Scrapping imdb ratings
        for item in soup.find_all(class_ = 'ratingColumn imdbRating'):
            rating_value = float(str(item.find('strong')).split('"')[1][:3])
            imdb_rating.append(rating_value)
            
            # Scrapping number of ratings
            number_of_ratings = int(''.join(str(item.find('strong')).split('"')[1].split('on ')[1].split()[0].split(','))) 
            num_rating.append(number_of_ratings)

        logging.info('Scrapping Finished')
        return name, year, link, num_rating, imdb_rating, gross, budget, runtime
    
    except Exception as e:
        logging.error(e)
