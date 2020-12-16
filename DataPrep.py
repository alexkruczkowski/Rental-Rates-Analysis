'''
File prep and cleaning for analysis
'''
import pandas as pd
import os

def read_file(path: str):
    """
    Determines if file extension is valid. 
    Raises TypeError if it is not. 
    Reads file into pandas df if valid.
    Parameters 
    ----------
    path : str
        The path to the file
    Returns
    -------
    pandas dataframe
    Examples
    --------
    """
    filename, file_extension = os.path.splitext(path)
    valid_file_extensions = ['.csv']

    if file_extension in valid_file_extensions:
        df = pd.read_csv(path)
    else:
        error_msg_file_extension = ', '.join(valid_file_extensions)
        raise TypeError(f'Please input either one of the following file formats: {error_msg_file_extension}')

    return(df)

def select_city(dataframe: str):
    """
    Select desired city of choice by inputting 
    the number corresponding to city size.

    Prints top cities and their corresponding number, 
    user inputs the number of the city for analysis.
    
    Parameters 
    ----------
    dataframe : str
        The name of the pandas dataframe
    
    Returns
    -------
    Dataframe filtered down to a city level

    Examples
    --------
    """
    #Print full data frame with size rank and reset display option after printing to default
    pd.set_option('display.max_rows', len(dataframe))
    print(dataframe[['RegionName','SizeRank']])
    pd.reset_option('display.max_rows')

    #input the sizerank, not index #, of the city for analysis
    filter_val = int(input('Enter the sizerank # of the city for analysis: '))
    
    #return the df filtered for that city
    df_filtered = dataframe[dataframe['SizeRank']==filter_val]
    return(df_filtered)

def prep_for_analysis(dataframe: str):
    """
    Takes filtered df, drops unnecessary columns,
    pivots columns and sets date as index.
    
    Parameters 
    ----------
    dataframe : str
        The name of the pandas dataframe
    
    Returns
    -------
    Pivoted dataframe ready for analysis

    Examples
    --------
    """
    #remove unnecessary columns
    df_drop = dataframe.drop(['RegionID', 'SizeRank'], axis = 1) 
    #convert rows into columns
    df_pivot = df_drop.melt(id_vars=["RegionName"], 
                            var_name="Date", 
                            value_name="Value")
    #change date columnd to datetime format, required for model
    df_pivot['Date']= pd.to_datetime(df_pivot['Date'])
    #remove region name
    df_remove_region = df_pivot.drop(['RegionName'], axis = 1) 
    #set date as index
    df_final = df_remove_region
    df_final.set_index('Date', inplace=True)

    return(df_final)

#df = read_file('data/MetroUSSmoothed.csv')
#df_filtered = select_city(df)
#df_final = prep_for_analysis(df_filtered)