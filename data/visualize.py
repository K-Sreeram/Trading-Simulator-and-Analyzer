import pandas as pd
import matplotlib.pyplot as plt

# Load the stock data from the CSV file
df = pd.read_csv("stock_data.csv")

# Convert the 'DATE' column to datetime format
df['DATE'] = pd.to_datetime(df['DATE'])

# Plot the closing price over time
plt.figure(figsize=(12, 6))
plt.plot(df['DATE'], df['CLOSE'], label='Closing Price', color='blue')
plt.title("RELIANCE Stock Price Over Time")
plt.xlabel("Date")
plt.ylabel("Closing Price (INR)")
plt.legend()
plt.grid(True)
plt.show()