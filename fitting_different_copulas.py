
import pandas as pd
import scipy.stats
import itertools
import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_kendall_tau(df):
    results = []
    # Generate all pairs of columns (stocks)
    for stock1, stock2 in itertools.combinations(df.columns, 2):
        tau, _ = scipy.stats.kendalltau(df[stock1], df[stock2])
        results.append((tau, stock1, stock2))
    # Sort results in decreasing order
    results.sort(reverse=True, key=lambda x: x[0])
    return results

file_path = 'log_returns_final.csv'
dataset = pd.read_csv(file_path)
df = dataset.iloc[0:131, :]
df=pd.DataFrame(df)
results = calculate_kendall_tau(df)
print(results)

column_name1 = 'TATA IS Equity'
column_name2 = 'JSTL IS Equity'
if column_name1 in df.columns:
    print(df[column_name1])
else:
    print(f"Column '{column_name1}' does not exist in the DataFrame.")
if column_name2 in df.columns:
    print(df[column_name2])
else:
    print(f"Column '{column_name2}' does not exist in the DataFrame.")
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

!pip install copulas
import copulas
from copulas.univariate import Univariate
univariate = Univariate()
univariate.fit(df[column_name1])
parameters = univariate.to_dict()
cdf1 = univariate.cumulative_distribution
print(parameters['type'])
print('---------------')
univariate2 = Univariate()
univariate2.fit(df[column_name2])
parameters2 = univariate2.to_dict()
cdf2 = univariate2.cumulative_distribution
print(parameters2['type'])
print('---------------')

!pip install copulae

pseudo_obs1 = df[column_name1]
pseudo_obs2 = df[column_name2]

pseudo_obs1=pseudo_obs1.apply(cdf1)
pseudo_obs2=pseudo_obs2.apply(cdf2)


print(pseudo_obs1)
print(pseudo_obs2)

data = np.column_stack((pseudo_obs1, pseudo_obs2))

data=np.array(data)

def calculate_aic(log_likelihood, num_params):
    return 2 * num_params - 2 * log_likelihood

#print(pseudo_obs)
#from pycopula.copula import ArchimedeanCopula, GaussianCopula, StudentCopula
from copulae import GaussianCopula, StudentCopula, ClaytonCopula, FrankCopula, GumbelCopula
_, ndim = data.shape

g_cop = GaussianCopula(dim=ndim)
g_cop.fit(data)
g_ll=g_cop.log_lik(data, to_pobs=False)
print('Parameters for Gaussian:', g_cop.params)
print('Log Likelihood for Gaussian: ',g_ll)
g_aic = calculate_aic(g_ll, 1)
print('AIC for Gaussian:', g_aic)
print('----------------------------------')

degrees_of_freedom = 5.5
t_cop = StudentCopula(dim=ndim, df=degrees_of_freedom)
t_cop.fit(data)
t_ll=t_cop.log_lik(data, to_pobs=False)
print('Parameters for Student-t:', t_cop.params)
print('Log Likelihood for Student-t: ',t_ll)
t_aic = calculate_aic(t_ll, 2)
print('AIC for Student-t:', g_aic)
print('----------------------------------')

c_cop=ClaytonCopula(dim=ndim)
c_cop.fit(data)
c_ll=c_cop.log_lik(data, to_pobs=False)
print('Parameters for Clayton:', c_cop.params)
print('Log Likelihood for Clayton: ',c_ll)
c_aic = calculate_aic(c_ll, 1)
print('AIC for Clayton:', c_aic)
print('----------------------------------')

gu_cop=GumbelCopula(dim=ndim)
gu_cop.fit(data)
gu_ll=gu_cop.log_lik(data, to_pobs=False)
print('Parameters for Gumbel:', gu_cop.params)
print('Log Likelihood for Gumbel: ',gu_ll)
gu_aic = calculate_aic(gu_ll, 1)
print('AIC for Gumbel:', gu_aic)
print('----------------------------------')

f_cop=FrankCopula(dim=ndim)
f_cop.fit(data)
f_ll=f_cop.log_lik(data, to_pobs=False)
print('Parameters for Frank:', f_cop.params)
print('Log Likelihood for Frank: ',f_ll)
f_aic = calculate_aic(f_ll, 1)
print('AIC for Frank:', f_aic)
print('----------------------------------')

aic_values = {
    g_cop: g_aic,
    t_cop: t_aic,
    c_cop: c_aic,
    gu_cop: gu_aic,
    f_cop: f_aic
}

best_copula = min(aic_values, key=aic_values.get)
print('Copula with the lowest AIC:', best_copula)



plt.scatter(pseudo_obs1, pseudo_obs2, alpha=0.5)
plt.xlabel(column_name1)
plt.ylabel(column_name2)
plt.title('Pseudo Observations')
plt.show()


u1, u2 = dataset.iloc[132:199][column_name1], dataset.iloc[132:199][column_name2]
u1 = u1.apply(cdf1)
u2 = u2.apply(cdf2)
data_array = np.column_stack((u1, u2))
data_array2 = np.column_stack((u2, u1))

def partial_derivative_u1(u1, u2, theta):
    exp_theta = np.exp(-theta)
    exp_theta_u1 = np.exp(-theta * u1)
    exp_theta_u2 = np.exp(-theta * u2)

    numerator = exp_theta_u1 * (exp_theta_u2 - 1)
    denominator = (exp_theta - 1) * (1 + (exp_theta_u1 - 1) * (exp_theta_u2 - 1) / (exp_theta - 1))

    return numerator / denominator

def partial_derivative_u2(u1, u2, theta):
    exp_theta = np.exp(-theta)
    exp_theta_u1 = np.exp(-theta * u1)
    exp_theta_u2 = np.exp(-theta * u2)

    numerator = exp_theta_u2 * (exp_theta_u1 - 1)
    denominator = (exp_theta - 1) * (1 + (exp_theta_u1 - 1) * (exp_theta_u2 - 1) / (exp_theta - 1))

    return numerator / denominator

def h1_u1_given_u2(u1, u2, theta):
    return partial_derivative_u2(u1, u2, theta)-0.5

def h2_u2_given_u1(u2, u1, theta):
    return partial_derivative_u1(u1, u2, theta)-0.5

theta=f_cop.params

u1_given_u2=[]
u2_given_u1=[]

for i,j in data_array:
    u1_given_u2.append(h1_u1_given_u2(i,j,theta))

for i,j in data_array2:
    u2_given_u1.append(h2_u2_given_u1(i,j,theta))

print(u1_given_u2)
print(u2_given_u1)

sum1=0
flag1=0
sum2=0
flag2=0

for i in u1_given_u2:
    sum1+=i
    if i>0.5:
        flag1=1
for i in u2_given_u1:
    sum2+=i
    if i<-0.5:
        flag2=1

if flag1==1 and flag2==1 :
  print('Trade start')