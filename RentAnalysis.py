'''
Process to analyze rental rates and determine when is the best time to rent and how long to rent for.
'''
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import pandas as pd
import statsmodels.api as sm
import matplotlib

def decompose_rent(df: str):
    """
    Takes pre-formatted dataframe and decomposes the trends.
    Generates plot for further analysis. 
    Parameters 
    ----------
    df : str
        Dataframe name
    Returns
    -------
    Seasonal decompomposition plot 
        (trend, seasonal, and residual factors split out)
    Examples
    --------
    """
    #additive model determined to be better fitting than multipilicative for rent trends
    components = seasonal_decompose(df, model='additive')
    plt.rcParams["figure.figsize"] = [12,8]
    components.plot()
    plt.show()  

def sarimax_param(df: str):
    """
    Takes pre-formatted dataframe and determines best SARIMAX paramaters.
    Looking for the lowest AIC value to use in the next step in the process.  
    Parameters 
    ----------
    df : str
        Dataframe name
    Returns
    -------
    Prints SARIMAX paramaters, seasonal paramters, and corresponding AIC values
    Examples
    --------
    """
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(df,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                results = mod.fit()
                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue

def sarimax_results(df:str):
    """
    Takes pre-formatted dataframe and SARIMAX user paramater input.
    Outputs model results that are used in later functions for summary and visualization purposes.
    Parameters 
    ----------
    df : str
        Dataframe name
    Returns
    -------
    Results of SARIMAX model. 
    Examples
    --------
    """
    params = [int(x) for x in input("input the first 6 parameters, all split by commas: ").split(',')]

    mod = sm.tsa.statespace.SARIMAX(df,
                                order=(params[0], params[1], params[2]),
                                seasonal_order=(params[3], params[4], params[5], 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
    results = mod.fit()
    return(results)

def sarimax_summary(results: str):
    """
    Takes SARIMAX results and shows model performance 
    for user to determine if results are significant. 
    Parameters 
    ----------
    results : str
        SARIMAX model results
    Returns
    -------
    Prints SARIMAX model summary and returns graphical visualization of model. 
    Examples
    --------
    """
    #show summary and determine if model is a good fit
    print(results.summary())

    #plot the results for visual analysis
    results.plot_diagnostics(figsize=(12, 6))
    plt.show()

def check_mse(results: str, df: str):
    """
    Takes SARIMAX results and checks MSE and RMSE. 
    This is to check how well the forecast worked. 
    Parameters 
    ----------
    results : str
        SARIMAX model results
    df: str
        pandas df for analysis
    Returns
    -------
    Prints model mean squared error and root mean squared error for analysis. 
    Examples
    --------
    """
    pred = results.get_prediction(start=pd.to_datetime('2020-01-01'), dynamic=False)
    y_forecast = list(pred.predicted_mean)
    yt = df['2020-01-01':]
    y_truth = yt['Value'].tolist()

    mse = mean_squared_error(y_truth, y_forecast)
    rmse = mean_squared_error(y_truth, y_forecast, squared=False)

    print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
    print('The Root Mean Squared Error of our forecasts is {}'.format(round(rmse, 2)))

def sarimax_forecast(results: str, df: str):
    """
    Takes SARIMAX results and generates forecast for next 24 months.
    Parameters 
    ----------
    results : str
        SARIMAX model results
    df: str
        pandas df for forecast
    Returns
    -------
    Prints SARIMAX model summary and returns graphical visualization of model. 
    Examples
    --------
    """
    pred_uc = results.get_forecast(steps=24)
    pred_ci = pred_uc.conf_int()
    ax = df.plot(label='observed', figsize=(14, 7))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Rent Price')
    plt.legend()
    plt.show()