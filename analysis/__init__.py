import pandas
import pandas.io.sql as psql
import psycopg2
import sys
sys.path.insert(0,'/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/personal_info')
sys.path.insert(0,'/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/sql/')
from personal_constants import *
from sql_methods import *

conn = psycopg2.connect(dbname = DB_maxim, user = USER_maxim, password = PASSWORD_maxim, host = HOST_maxim, port = PORT_maxim)
dataframe = psql.read_sql_query("SELECT * FROM data", con=conn)
print(dataframe)