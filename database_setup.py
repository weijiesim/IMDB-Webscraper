from getpass import getpass
from mysql.connector import connect
from webscrapper import sql_df
import logging

print('Connecting to Google Cloud mysql server.')
try:
    connection = connect(
        host = input("Enter Public IP address: "),
        user = input("Enter username: "),
        password = getpass("Enter password: "),
        auth_plugin = 'mysql_native_password',
        database = 'imdb'
        )

except Exception as e:
    logging.error(e)

logging.info('Connected to Google Cloud MySQL successfully!')

mycursor = connection.cursor()

# Drop table if it already exists
mycursor.execute("DROP TABLE IF EXISTS IMDB ")


print("Creating table...")

# Create table
sql = """CREATE TABLE IMDB (
    NAME VARCHAR(100),
    YEAR INT,
    LINK VARCHAR(50),
    NUMBER_OF_RATINGS INT,
    IMDB_RATINGS FLOAT(2,1),
    GROSS_EARNINGS VARCHAR(20),
    MOVIE_BUDGET VARCHAR(20),
    RUNTIME VARCHAR(10))
    """

mycursor.execute(sql)

cols = "`,`".join([str(i) for i in sql_df.columns.tolist()])

for i,row in sql_df.iterrows():
    sql = "INSERT INTO `IMDB` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    mycursor.execute(sql, tuple(row))

    # Commit to save changes to database
    connection.commit()

mycursor.close()
connection.close()
logging.info("Table created successfully!")
print("Table created successfully!")