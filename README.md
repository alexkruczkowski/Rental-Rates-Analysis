# Rental-Rates-Analysis
Analysis on rental rates - forecasting future prices and examining seasonality to determine the best time to rent.

## Data
The U.S. metro smoothed rental data is sourced from the Zillow and can be found here.

Data includes average monthly rental prices for 100 U.S. metropolitan areas beginning in 2014 and ending in October of 2020. Zillow is a real estate marketplace that is widely popular in the United States.

## :mag: Methodology
Data prep and cleaning is done using the Python library, Pandas. The rental rates are filtered down to a single city and the data is prepared (date and values pivoted to be columns, date changed to datetime format, date set as index, unnecessary columns dropped) in order to be analyzed.

Analayis and modelling was done using a SARIMAX or seasonal autoregressive integrated moving average model as the data is a linear regression with seasonality. Model parameters were determined by finding the paramaters with the lowest AIC values. Once paramaters were found, model effectiveness was examined by checking p-values, skew, kurtosis, p-values and the mean squared error.

Finally, the data was forecasted if the model was found to be a relatively good fit.

## :computer: Findings
As a result of the analysis, it was found that the best time to rent in most cities was in January, and with rents increasing in most areas, longer term leases of 2 years were preferred.

For areas where rent was not trending upwards, shorter term, 1 year rentals are preferred.

## :wave: Author
Alex Kruczkowski
