# -*- coding: utf-8 -*-
"""Distance approach.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rHSMhCDFt_heLlfwnG-Okj0A27vehXjX
"""

import pandas as pd

# Load the data
df = pd.read_csv('pair_trading.csv')

# Display the first few rows and the column names
print(df.head())
print(df.columns)

import numpy as np
from scipy.spatial.distance import pdist, squareform

# Calculate daily returns (percentage change)
returns = df.pct_change().dropna()

# Calculate Euclidean distances between the returns of different stocks
distance_matrix = squareform(pdist(returns.T, 'euclidean'))
distance_df = pd.DataFrame(distance_matrix, index=returns.columns, columns=returns.columns)

# Find the pair of stocks with the smallest distance
min_distance_pair = np.unravel_index(np.argmin(distance_matrix + np.eye(distance_matrix.shape[0]) * np.max(distance_matrix)), distance_matrix.shape)
stock1, stock2 = returns.columns[min_distance_pair[0]], returns.columns[min_distance_pair[1]]
print(f"The selected pair of stocks are: {stock1} and {stock2}")

from copulas.multivariate import GaussianMultivariate
from copulas.visualization import scatter_2d

# Extract returns of the selected pair
selected_pair_returns = returns[[stock1, stock2]]

# Fit Gaussian Copula
copula = GaussianMultivariate()
copula.fit(selected_pair_returns)

# Sample data from the copula
sampled_data = copula.sample(len(selected_pair_returns))

# Plot the sampled data against the actual returns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(selected_pair_returns.iloc[:, 0], selected_pair_returns.iloc[:, 1], label='Actual Returns')
plt.scatter(sampled_data.iloc[:, 0], sampled_data.iloc[:, 1], label='Sampled Returns', alpha=0.7)
plt.xlabel(stock1)
plt.ylabel(stock2)
plt.legend()
plt.title('Copula Model - Actual vs Sampled Returns')
plt.show()

def generate_signals(returns, copula_model):
    # Calculate the cumulative distribution function (CDF) values for the returns
    u = copula_model.cdf(returns.values)

    # Ensure u is a 2D array
    u = np.atleast_2d(u)

    signals = []

    for i in range(u.shape[0]):
        signal1 = 0
        signal2 = 0
        if u[i, 0] >= 0.95 and u[i, 1] <= 0.05:
            signal1 = 'long'
            signal2 = 'short'
        elif u[i, 0] <= 0.05 and u[i, 1] >= 0.95:
            signal1 = 'short'
            signal2 = 'long'

        signals.append((signal1, signal2))

    return signals

# Generate signals
signals = generate_signals(selected_pair_returns, copula)

# Combine signals with dates
signals_df = pd.DataFrame(signals, columns=[f'{stock1}_signal', f'{stock2}_signal'])
signals_df['Date'] = selected_pair_returns.index
print(signals_df.head())

import numpy as np
import pandas as pd
from copulas.multivariate import GaussianMultivariate

# Load the dataset
df = pd.read_csv('pair_trading.csv')

# Calculate daily returns
returns = df.pct_change().dropna()

# Calculate Euclidean distances
distances = pdist(returns.T, 'euclidean')
dist_matrix = squareform(distances)

# Find the pair of stocks with the minimum distance
min_dist_idx = np.unravel_index(np.argmin(dist_matrix + np.eye(dist_matrix.shape[0]) * np.inf), dist_matrix.shape)
stock1, stock2 = df.columns[min_dist_idx[0]], df.columns[min_dist_idx[1]]

# Select returns for the pair of stocks
selected_pair_returns = returns[[stock1, stock2]]

# Fit a Gaussian copula to the selected pair's returns
copula = GaussianMultivariate()
copula.fit(selected_pair_returns)

# Define the function to generate trading signals
def generate_signals(returns, copula_model):
    # Calculate the cumulative distribution function (CDF) values for the returns
    u = copula_model.cdf(returns)

    # Ensure u is a 2D array
    u = np.atleast_2d(u)

    signals = []

    for i in range(u.shape[0]):
        signal1 = 0
        signal2 = 0
        if u[i, 0] >= 0.95 and u[i, 1] <= 0.05:
            signal1 = 'long'
            signal2 = 'short'
        elif u[i, 0] <= 0.05 and u[i, 1] >= 0.95:
            signal1 = 'short'
            signal2 = 'long'

        signals.append((signal1, signal2))

    return signals

# Generate signals
signals = generate_signals(selected_pair_returns, copula)

# Check lengths of selected_pair_returns and signals
print(f"Length of selected_pair_returns: {len(selected_pair_returns)}")
print(f"Length of signals: {len(signals)}")

# Combine signals with dates
signals_df = pd.DataFrame(signals, columns=[f'{stock1}_signal', f'{stock2}_signal'])
signals_df['Date'] = selected_pair_returns.index

# Ensure the index length matches
assert len(signals_df) == len(selected_pair_returns), "Length mismatch between signals and returns DataFrame"

print(signals_df.head())

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from copulas.multivariate import GaussianMultivariate

# Load the dataset
df = pd.read_csv('pair_trading.csv')

# Calculate daily returns
returns = df.pct_change().dropna()

# Calculate Euclidean distances
distances = pdist(returns.T, 'euclidean')
dist_matrix = squareform(distances)

# Find the pair of stocks with the minimum distance
min_dist_idx = np.unravel_index(np.argmin(dist_matrix + np.eye(dist_matrix.shape[0]) * np.inf), dist_matrix.shape)
stock1, stock2 = df.columns[min_dist_idx[0]], df.columns[min_dist_idx[1]]

# Select returns for the pair of stocks
selected_pair_returns = returns[[stock1, stock2]]

# Fit a Gaussian copula to the selected pair's returns
copula = GaussianMultivariate()
copula.fit(selected_pair_returns)

# Define the function to generate trading signals
def generate_signals(returns, copula_model):
    # Calculate the cumulative distribution function (CDF) values for the returns
    u = copula_model.cdf(returns)

    # Ensure u is a 2D array
    u = np.atleast_2d(u)

    signals = []

    for i in range(u.shape[0]):
        signal1 = 0
        signal2 = 0
        if u[i, 0] >= 0.95 and u[i, 1] <= 0.05:
            signal1 = 'long'
            signal2 = 'short'
        elif u[i, 0] <= 0.05 and u[i, 1] >= 0.95:
            signal1 = 'short'
            signal2 = 'long'

        signals.append((signal1, signal2))

    return signals

# Generate signals
signals = generate_signals(selected_pair_returns, copula)

# Ensure the signals list length matches the selected_pair_returns
assert len(signals) == len(selected_pair_returns), "Length mismatch between signals and selected_pair_returns"

# Combine signals with dates
signals_df = pd.DataFrame(signals, columns=[f'{stock1}_signal', f'{stock2}_signal'])
signals_df['Date'] = selected_pair_returns.index

print(signals_df.head())