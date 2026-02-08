
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import sqlite3

st.set_page_config(layout = 'wide')

st.title('Cross Market Analysis')

# Connect to the SQLite database
conn = sqlite3.connect('mydb.db')

with st.sidebar:
    select = option_menu('Main Menu', ['Home', 'MARKET OVERVIEW', 'SQL QUERY RUNNER', 'TOP COINS TREND ANALYSIS'])

if select == 'Home':
    st.header('Welcome to the Cross Market Analysis Dashboard')
    st.write('Use the sidebar to navigate through different analysis pages.')

elif select == 'MARKET OVERVIEW':
    st.header('MARKET OVERVIEW: Filters & Data Exploration')

    # Date Range Selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date', pd.to_datetime('2020-01-01'))
    with col2:
        end_date = st.date_input('End Date', pd.to_datetime('2026-01-26'))

    if start_date > end_date:
        st.error('Error: End Date must be after Start Date.')
    else:
        st.subheader(f'Data for the period: {start_date} to {end_date}')

        # Bitcoin Average Price
        st.subheader('Average Prices')
        sql_btc_avg = f"""
        SELECT AVG(price) FROM "Crypto prices"
        WHERE coin_name = 'bitcoin' AND date BETWEEN '{start_date}' AND '{end_date}'
        """
        avg_btc_price = pd.read_sql_query(sql_btc_avg, conn).iloc[0,0]
        st.write(f"Average Bitcoin Price: ${avg_btc_price:,.2f}" if avg_btc_price else "N/A")

        # Oil Average Price
        sql_oil_avg = f"""
        SELECT AVG(Price) FROM "oil prices"
        WHERE Date BETWEEN '{start_date}' AND '{end_date}'
        """
        avg_oil_price = pd.read_sql_query(sql_oil_avg, conn).iloc[0,0]
        st.write(f"Average Oil Price: ${avg_oil_price:,.2f}" if avg_oil_price else "N/A")

        # S&P 500 Average Closing Price
        sql_gspc_avg = f"""
        SELECT AVG("('^GSPC', 'Close')") FROM "stock prices"
        WHERE "('Date', '')" BETWEEN '{start_date}' AND '{end_date}'
        """
        avg_gspc_close = pd.read_sql_query(sql_gspc_avg, conn).iloc[0,0]
        st.write(f"Average S&P 500 Closing Price: ${avg_gspc_close:,.2f}" if avg_gspc_close else "N/A")

        # NIFTY Average Closing Price
        sql_nifty_avg = f"""
        SELECT AVG("('^NSEI', 'Close')") FROM "stock prices"
        WHERE "('Date', '')" BETWEEN '{start_date}' AND '{end_date}'
        """
        avg_nifty_close = pd.read_sql_query(sql_nifty_avg, conn).iloc[0,0]
        st.write(f"Average NIFTY Closing Price: ${avg_nifty_close:,.2f}" if avg_nifty_close else "N/A")

        st.subheader('Daily Market Snapshot')
        sql_snapshot = f"""
        SELECT
            sp."('Date', '')" AS Date,
            cp_btc.price AS Bitcoin_Price,
            op.Price AS Oil_Price_USD,
            sp."('^GSPC', 'Close')" AS SP500_Close,
            sp."('^NSEI', 'Close')" AS NIFTY_Close
        FROM "stock prices" AS sp
        LEFT JOIN "oil prices" AS op ON sp."('Date', '')" = op.Date
        LEFT JOIN "Crypto prices" AS cp_btc ON sp."('Date', '')" = cp_btc.date AND cp_btc.coin_name = 'bitcoin'
        WHERE sp."('Date', '')" BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY Date;
        """
        market_snapshot_df = pd.read_sql_query(sql_snapshot, conn)
        st.dataframe(market_snapshot_df)

elif select == 'SQL QUERY RUNNER':
    st.header('SQL QUERY RUNNER: SQL Query Runner')

    predefined_queries = {
        'Top 3 Cryptocurrencies by Market Cap': "SELECT id, name, market_cap_rank, market_cap FROM Cryptocurrency ORDER BY market_cap DESC LIMIT 3;",
        'Cryptocurrencies with >90% Circulating Supply': "SELECT id, name, symbol, circulating_supply, total_supply FROM Cryptocurrency WHERE circulating_supply > (total_supply * 0.9) ORDER BY name;",
        'Average Oil Price by Year': "SELECT STRFTIME('%Y', Date) AS year, AVG(Price) AS average_price FROM \"oil prices\" GROUP BY year ORDER BY year;",
        'Highest NASDAQ Closing Price': "SELECT MAX(\"('^IXIC', 'Close')\") AS highest_close_price FROM \"stock prices\";",
        'Correlation: Bitcoin vs S&P 500': "SELECT cp.date AS crypto_date, cp.price AS bitcoin_price, sp.\"('Date', '')\" AS stock_date, sp.\"('^GSPC', 'Close')\" AS gspc_close FROM \"Crypto prices\" AS cp INNER JOIN \"stock prices\" AS sp ON cp.date = sp.\"('Date', '')\" WHERE cp.coin_name = 'bitcoin';"
    }

    selected_query_name = st.selectbox(
        'Select a SQL Query to Run:',
        list(predefined_queries.keys())
    )

    if st.button('Run Query'):
        query = predefined_queries[selected_query_name]
        st.code(query, language='sql') # Display the query being run
        try:
            result_df = pd.read_sql_query(query, conn)
            if not result_df.empty:
                st.subheader('Query Results:')
                st.dataframe(result_df)
            else:
                st.write('No results found for this query.')
        except Exception as e:
            st.error(f"Error executing query: {e}")

elif select == 'TOP COINS TREND ANALYSIS':
    st.header('TOP COINS TREND ANALYSIS: Top Cryptocurrencies Analysis')

    # Get top 3 cryptocurrencies for selection
    top_coins_query = "SELECT id, name FROM Cryptocurrency ORDER BY market_cap_rank ASC LIMIT 3;"
    top_coins_df = pd.read_sql_query(top_coins_query, conn)

    if not top_coins_df.empty:
        coin_names = top_coins_df['name'].tolist()
        selected_coin_name = st.selectbox('Select Cryptocurrency:', coin_names)
        selected_coin_id = top_coins_df[top_coins_df['name'] == selected_coin_name]['id'].iloc[0]

        st.subheader(f'Analysis for {selected_coin_name}')

        # Date Range Selection for Page 3
        col3, col4 = st.columns(2)
        with col3:
            start_date_crypto = st.date_input('Start Date', pd.to_datetime('2025-02-01'), key='p3_start_date')
        with col4:
            end_date_crypto = st.date_input('End Date', pd.to_datetime('2026-02-04'), key='p3_end_date')

        if start_date_crypto > end_date_crypto:
            st.error('Error: End Date must be after Start Date.')
        else:
            # Fetch daily prices for the selected crypto and date range
            sql_crypto_prices = f"""
            SELECT date, price FROM "Crypto prices"
            WHERE coin_name = '{selected_coin_id}' AND date BETWEEN '{start_date_crypto}' AND '{end_date_crypto}'
            ORDER BY date;
            """
            daily_prices_df = pd.read_sql_query(sql_crypto_prices, conn)
            daily_prices_df['date'] = pd.to_datetime(daily_prices_df['date'])
            daily_prices_df = daily_prices_df.set_index('date')

            if not daily_prices_df.empty:
                st.subheader('Daily Price Trend')
                st.line_chart(daily_prices_df['price'])

                st.subheader('Daily Price Table')
                st.dataframe(daily_prices_df)
            else:
                st.write(f'No historical price data available for {selected_coin_name} in the selected date range.')
    else:
        st.write('No top cryptocurrencies found in the database.')


# Close the connection when the app is done
conn.close()
