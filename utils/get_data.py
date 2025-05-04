from jugaad_data.nse import stock_df, NSELive
import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt
import plotly.express as px
from utils.data import stock_names


def get_stock_data(stock_symbol, start_date, end_date, criteria):
    criteria = criteria.upper()
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()    
    df = stock_df(symbol=stock_symbol, from_date=start_date, to_date=end_date, series="EQ")
    df = df[["DATE", "OPEN", "CLOSE", "HIGH", "LOW", "LTP", "VOLUME", "VALUE", "NO OF TRADES"]]
    graph_image = generate_graph(df, criteria, stock_symbol)
    return graph_image

def get_live_stock_data(stock_symbol):
    n = NSELive()
    data = n.stock_quote(stock_symbol)
    return data['priceInfo']    

def generate_graph(df, criteria, stock_symbol):
    df = df[["DATE", criteria]]
    fig = px.line(df, x="DATE", y=criteria, title=criteria + " vs Date for " + stock_symbol)
    filepath = "static/graph/history.html"
    fig.write_html(filepath)
    return filepath

def get_live_stock_data():
    n = NSELive()
    stock_list = list(stock_names.keys())
    column_names = ["Stock", "lastPrice", "change", "pChange", "previousClose", "open", "close", "basePrice" ]
    df = pd.DataFrame(columns=column_names)
    for stock in stock_list:
        data = n.stock_quote(stock)
        data = data['priceInfo']
        df.loc[len(df.index)] = [stock, data['lastPrice'], data['change'], data['pChange'], data['previousClose'], data['open'], data['close'], data['basePrice']]
    return df

def generate_combined_graph(criteria, stock_symbols, start_date, end_date):
    criteria = criteria.upper()
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()  

    
    dataframes = [stock_df(symbol=stock_symbol, from_date=start_date, to_date=end_date, series="EQ") for stock_symbol in stock_symbols]
    fig = px.line(title=f"{criteria} vs Date for Multiple Stocks")

    
    for i in range(len(dataframes)):
        df = dataframes[i]
        df = df[["DATE", criteria]]
        fig.add_scatter(x=df["DATE"], y=df[criteria], name=stock_symbols[i])

    filepath = f"static/graph/combined.html"

    fig.write_html(filepath)
    return filepath