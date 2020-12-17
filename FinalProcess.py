'''
Analyzing rental rates in the Metro U.S. 

Goal: determine the best time to rent a unit in order to save money

Data: Zillow Metro U.S. Smoothed Rental Rates
'''
import DataPrep as prep
import RentAnalysis as ra
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
import statsmodels.api as sm
import matplotlib

#import file
df = prep.read_file('data/MetroUSSmoothed.csv')

#filter for one city
df_filtered = prep.select_city(df)

#preform final clean up before analysis
df_final = prep.prep_for_analysis(df_filtered)

#visualize the rent trends
ra.decompose_rent(df_final)

#find the best parameters for the sarimax model
ra.sarimax_param(df_final)

#enter the paramters for the sarimax model and returns sarimax results used for summary and forecasting
sresults = ra.sarimax_results(df_final)

#summary of model results
ra.sarimax_summary(sresults)

#check model mse and rmse to help determine performance
ra.check_mse(sresults, df_final)

#final forecast for 24 periods or 2 years
ra.sarimax_forecast(sresults, df_final)