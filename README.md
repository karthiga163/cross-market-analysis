# cross-market-analysis:
In this project past 5 years cryptocurrency, oil, stock prices were analysed separately and compared to get the data accurately for investment ideas and financial purposes.
To begin with we can use any compiler to do this project like vs code, google colab, jupyternotebook. Here I have done this in google colab.
#collecting first five pages:
#FOR LOOP AND STRING FORMATTING:
At first I have imported the library requests, using for loop and string formatting first five pages of cryptocurrency data was extracted from the url. 
It was stored in the json file in the variable called data.
Using for loop the data was appended with the necessary column names in to a new variable called records
#pandas:
using pandas library the data was converted into dataframe and the date column was converted into datetime.
now we have collected first five pages.
#finding top 3 coins historical prices
new empty list called historical data was created and the using forloop and string formatting data was collected.
#pandas:
using pandas library the data was converted into dataframe and the date column was converted into datetime.
#collecting oil prices data
As we need only jan2020 to jan 2026 oil prices we have filtered the necessary data.
#collecting stock prices data
for this we need two libraries yfinance and pandas we have imported them.
And we have downloaded the tickers=["^GSPC", "^IXIC", "^NSEI"].
using dropna we have excluded the null values.
#ALL THE DATAS WERE EXCTRACTED SUCCESSFULLY
#CREATING SQL TABLES
Now sqlite3 library was imported and connection was established using cursor.
All the data were pushed into the database called mydb.db
four tables were created.
#SQL QUERY RUNNING
From each table 5 queries were runned to exctract the needed data.
#SREAMLIT
import streamlit and create three pages  'MARKET OVERVIEW', 'SQL QUERY RUNNER', 'TOP COINS TREND ANALYSIS' and entire coding was written to filter the data.
app.py was created.
from this app we can now analyse the project.

