import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean_data(data, max_jump=10, min_val=0, max_val=50, flat_period=5):
    original_data = data.copy()

    # Checking for jumps
    prev_value = data.iloc[0]
    for t, value in data.items():
        if abs(value - prev_value) <= max_jump:
            data[t] = value
            prev_value = value
        else:
            data[t] = np.nan

    # Checking for values in range
    for t, value in data.items():
        if min_val <= value <= max_val:
            pass
        else:
            data[t] = np.nan

    # Checking for flat periods
    i = 0
    while i < len(data) - flat_period:
        if len(set(data[i: i + flat_period + 1])) == 1:
            data[i: i + flat_period + 1] = np.nan
            i += flat_period
        else:
            i += 1

    data_removed = original_data[~original_data.isin(data)]
    return data, data_removed

# Create date range
date_rng = pd.date_range(start="1/1/2020", end="1/31/2020", freq="D")

# Sample time series data with DateTimeIndex
data1 = pd.Series([1, 2, -1, 4, 5, 20, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                   21, 22, 24, 24, 24, 24, 24, 24, 29, 30, 31], index=date_rng)
data2 = pd.Series([5, 6, 200, 8, 9, 10, 11, 12, 300, 14, 15, 16, 17, 18, 19, 20, 21, 22, 
                   23, 24, 25, 26, 27, 27, 27, 30, 31, 32, 33, 34, 35], index=date_rng)
data3 = pd.Series([15, 16, 11, 18, 400, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 
                   32, 33, 34, 35, 36, 37, 38, 39, 45, 45, 45, 45, 45, 45], index=date_rng)

# Clean the data
data1, removed_data1 = clean_data(data1)
data2, removed_data2 = clean_data(data2)
data3, removed_data3 = clean_data(data3)

# Plot data showing outliers as red dots
def plot_data(original_data, cleaned_data, title):
    plt.figure(figsize=(10, 5))
    plt.plot(original_data, '.', color="red", label="Original Data")
    plt.plot(cleaned_data, '.', color="green", label="Cleaned Data")
    plt.title(title)
    plt.legend()
    plt.show()

plot_data(data1, removed_data1, "Data1")
plot_data(data2, removed_data2, "Data2")
plot_data(data3, removed_data3, "Data3")
