from jugaad_data.nse import stock_df, NSELive
import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt
import plotly.express as px

def get_stock_data(stock_symbol,start_date,end_date, criteria):
    criteria = criteria.upper()
    start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
    end_date = datetime.strptime(end_date,"%Y-%m-%d").date()
    df = stock_df(symbol=stock_symbol,from_date=start_date, to_date=end_date,series="EQ")
    df = df[["DATE","OPEN","CLOSE","HIGH","LOW","LTP","VOLUME","VALUE", "NO OF TRADES"]]
    graph_image = generate_graph(df, criteria, stock_symbol)
    return graph_image


def generate_graph(df, criteria, stock_symbol):
    df["DATE"] = pd.to_datetime(df["DATE"]) 

    plt.figure(figsize=(10, 5))
    plt.plot(df["DATE"], df[criteria], marker='o', linestyle='-', label=criteria)

    plt.xlabel("Date")
    plt.ylabel(criteria)
    plt.title(f"{criteria} vs Date for {stock_symbol}")
    plt.legend()
    plt.grid(True)
    plt.show()





if __name__ == "__main__":
    stock_symbol = "RELIANCE"  
    start_date = "2024-03-01"
    end_date = "2024-03-15"
    criteria = "CLOSE"  

    graph_path = get_stock_data(stock_symbol, start_date, end_date, criteria)
    print(f"Graph saved at: {graph_path}")
