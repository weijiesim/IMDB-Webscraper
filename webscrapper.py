from webscrapping_functions import *
import pandas as pd

url = "https://www.imdb.com/chart/top"
name, year, link, num_rating, imdb_rating, gross, budget, runtime = imdb(url)

sql_df = pd.DataFrame(data={
    'Name' : name,
    'Year' : year,
    'Link' : link,
    'Number_of_Ratings' : num_rating,
    'Imdb_Ratings' : imdb_rating,
    'Gross_Earnings' : gross,
    'Movie_Budget' : budget,
    'Runtime' : runtime
    })

number_of_rows = sql_df.shape[0]

print('Webscrapped Dataframe:')
print(sql_df)

logging.info(f'Number of rows: {number_of_rows}')