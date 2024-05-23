import pandas as pd
import matplotlib.pyplot as plt

target = "kalteneck"

# Read the data using pandas, skipping header lines
data = pd.read_csv("examples/%s.csv" % target, delimiter=';', quotechar='|', skiprows=9)

# Convert the 'Mittelwert' column to float
data['Mittelwert'] = data['Mittelwert'].str.replace(',', '.').astype(float)
data['Maximum'] = data['Maximum'].str.replace(',', '.').astype(float)
data['Minimum'] = data['Minimum'].str.replace(',', '.').astype(float)

# Extract the year and month from the 'Datum' column
data['Date'] = pd.to_datetime(data['Datum'])
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Group by year and calculate the mean 'Mittelwert' for each year
yearly_avg = data.groupby('Year').agg({'Mittelwert': 'mean', 'Maximum': 'mean', 'Minimum': 'mean'}).reset_index()

# Ignore the first year if it's incomplete
yearly_avg = yearly_avg[yearly_avg['Year'] != yearly_avg['Year'].min()]

# Calculate the 5-year rolling average
yearly_avg['5-Year Rolling Avg'] = yearly_avg['Mittelwert'].rolling(window=5).mean()

# Calculate the 6-month moving averages for Maximum and Minimum values
yearly_avg['6-Month Max Moving Avg'] = yearly_avg['Maximum'].rolling(window=6).mean()
yearly_avg['6-Month Min Moving Avg'] = yearly_avg['Minimum'].rolling(window=6).mean()

# Plot the data
plt.figure(figsize=(10, 5))

# Yearly average
plt.plot(yearly_avg['Year'], yearly_avg['Mittelwert'], marker='o', linestyle='-', label='Yearly Average Temperature')

# 5-year rolling average
plt.plot(yearly_avg['Year'], yearly_avg['5-Year Rolling Avg'], color='r', linestyle='--', marker='x', label='5-Year Rolling Average')

# 6-month moving average for Maximum and Minimum values
plt.plot(yearly_avg['Year'], yearly_avg['6-Month Max Moving Avg'], color='g', linestyle='-', alpha=0.5, label='6-Month Max Moving Average')
plt.plot(yearly_avg['Year'], yearly_avg['6-Month Min Moving Avg'], color='b', linestyle='-', alpha=0.5, label='6-Month Min Moving Average')

plt.xlabel('Year')
plt.ylabel('Average Temperature (°C)')
plt.title('Yearly and Monthly Average Temperature Over Time')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig("examples/%s.png" % target)  # You can specify the file name and format here


plt.show()
