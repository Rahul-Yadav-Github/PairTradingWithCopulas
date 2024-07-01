# -*- coding: utf-8 -*-
"""copula with distance.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17puDldPqHmNUy284XvDAYJGyZqhr6qdo
"""

pip install copulae

pip install copulas

import pandas as pd
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
from copulas.univariate import Univariate
from scipy.stats import rankdata
from copulae import GaussianCopula, StudentCopula, ClaytonCopula, FrankCopula, GumbelCopula
from scipy.spatial.distance import pdist, squareform

def convert_to_pseudo_observations(matrix):
    if isinstance(matrix, pd.DataFrame):
        matrix = matrix.values
    n_samples = matrix.shape[0]
    ranks = np.apply_along_axis(rankdata, 0, matrix)
    pseudo_observations = ranks / (n_samples + 1)
    return pseudo_observations

def calculate_aic(log_likelihood, num_params):
    return 2 * num_params - 2 * log_likelihood

def calculate_bic(log_likelihood, num_params, num_samples):
    return np.log(num_samples) * num_params - 2 * log_likelihood

# Load data
file_path = 'pair_trading.csv'
df = pd.read_csv(file_path).iloc[1:146]

# Calculate daily returns (percentage change)
returns = df.pct_change().dropna()

# Calculate Euclidean distances between the returns of different stocks
distance_matrix = squareform(pdist(returns.T, 'euclidean'))
distance_df = pd.DataFrame(distance_matrix, index=returns.columns, columns=returns.columns)

# Find the pair of stocks with the smallest distance
min_distance_pair = np.unravel_index(np.argmin(distance_matrix + np.eye(distance_matrix.shape[0]) * np.max(distance_matrix)), distance_matrix.shape)
column_name1, column_name2 = returns.columns[min_distance_pair[0]], returns.columns[min_distance_pair[1]]
print(f"The selected pair of stocks are: {column_name1} and {column_name2}")

# Plot histograms
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.hist(df[column_name1], bins=100, color='blue', alpha=0.7)
plt.title(f'Histogram of {column_name1}')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
plt.hist(df[column_name2], bins=100, color='green', alpha=0.7)
plt.title(f'Histogram of {column_name2}')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# Fit univariate distributions
univariate1 = Univariate()
univariate1.fit(df[column_name1])
parameters1 = univariate1.to_dict()
print(parameters1['type'])
print('---------------')

univariate2 = Univariate()
univariate2.fit(df[column_name2])
parameters2 = univariate2.to_dict()
print(parameters2['type'])
print('---------------')

# Convert data to pseudo-observations
data = np.column_stack((df[column_name1], df[column_name2]))
data = convert_to_pseudo_observations(data)

# Fit copulas and calculate AIC and BIC
copulas = {
    'Gaussian': GaussianCopula(dim=data.shape[1]),
    'Student-t': StudentCopula(dim=data.shape[1], df=5.5),
    'Clayton': ClaytonCopula(dim=data.shape[1]),
    'Gumbel': GumbelCopula(dim=data.shape[1]),
    'Frank': FrankCopula(dim=data.shape[1])
}

aic_values = {}
bic_values = {}
num_samples = data.shape[0]

for name, copula in copulas.items():
    copula.fit(data)
    log_likelihood = copula.log_lik(data, to_pobs=False)
    num_params = 2 if name == 'Student-t' else 1
    aic = calculate_aic(log_likelihood, num_params)
    bic = calculate_bic(log_likelihood, num_params, num_samples)
    aic_values[name] = aic
    bic_values[name] = bic
    print(f'Parameters for {name}:', copula.params)
    print(f'Log Likelihood for {name}:', log_likelihood)
    print(f'AIC for {name}:', aic)
    print(f'BIC for {name}:', bic)
    print('----------------------------------')

best_copula_aic = min(aic_values, key=aic_values.get)
best_copula_bic = min(bic_values, key=bic_values.get)
print('Copula with the lowest AIC:', best_copula_aic)
print('Copula with the lowest BIC:', best_copula_bic)