from jugaad_data.nse import stock_df
from datetime import datetime, timedelta

to_date = datetime.today().date()  
from_date = to_date - timedelta(days=7)  
# Get historical stock data for RELIANCE
df = stock_df(symbol="RELIANCE", from_date=from_date, to_date=to_date, series="EQ")

df.to_csv("stock_data.csv", index=False)

print(f"Stock data collected from {from_date} to {to_date} and saved successfully!")
