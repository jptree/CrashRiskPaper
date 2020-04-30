import pandas as pd
import datetime
from statsmodels.formula.api import ols
import numpy as np
import matplotlib.pyplot as plt

DATABASE_FILENAME = "MSCI Data.csv"
data = pd.read_csv(DATABASE_FILENAME)

pd.set_option('display.max_rows', 1500)
pd.set_option('display.max_columns', 90500)
pd.set_option('display.width', 1000)


def get_weekly_return_data_frame(data):
    weekly_prices_df = pd.DataFrame()
    for country in data:
        all_weeks_df = pd.DataFrame()
        if country == 'Date':
            continue

        prices = pd.DataFrame(data, columns=[country, 'Date'])
        prices['dayOfWeek'] = prices.apply(lambda row: pd.to_datetime(row['Date']).dayofweek, axis=1)

        monday_close = 0
        initial_monday = False

        for i in range(len(prices.index) - 1):
            if not initial_monday:
                if not prices.isnull().iloc[i][country] and prices.iloc[i]['dayOfWeek'] == 0:
                    monday_close = prices.iloc[i][country]
                    initial_monday = True
                    continue
                elif prices.iloc[i]['dayOfWeek'] == 6:
                    weeks_return_df = pd.DataFrame({country: np.NaN}, index=[prices.iloc[i]['Date']])
                    all_weeks_df = all_weeks_df.append(weeks_return_df)
                    continue
                else:
                    continue

            if prices.iloc[i]['dayOfWeek'] == 0:
                monday_close = prices.iloc[i][country]

            if prices.iloc[i]['dayOfWeek'] == 6:
                sunday_close = prices.iloc[i][country]
                sunday_date = prices.iloc[i]['Date']
                weekly_return = sunday_close / monday_close - 1
                weeks_return_df = pd.DataFrame({country: weekly_return}, index=[sunday_date])
                all_weeks_df = all_weeks_df.append(weeks_return_df)

        if weekly_prices_df.isnull:
            weekly_prices_df = weekly_prices_df.join(all_weeks_df, how='outer')
        else:
            weekly_prices_df = pd.concat([weekly_prices_df, all_weeks_df], join='inner', axis=1)
        print(weekly_prices_df)

    return weekly_prices_df


def index_model_regression(weekly_returns, benchmark, country):



    # print(daily_returns)
    first_row = weekly_returns[country].first_valid_index()
    last_row = weekly_returns[country].last_valid_index()

    mrm2 = weekly_returns[benchmark][first_row: last_row - 4].tolist()
    mrm1 = weekly_returns[benchmark][first_row + 1: last_row - 3].tolist()
    mr = weekly_returns[benchmark][first_row + 2: last_row - 2].tolist()
    mrp1 = weekly_returns[benchmark][first_row + 3: last_row - 1].tolist()
    mrp2 = weekly_returns[benchmark][first_row + 4: last_row].tolist()
    cr = weekly_returns[country][first_row + 2: last_row - 2].tolist()

    regression_data = pd.DataFrame({'MRM2': mrm2, 'MRM1': mrm1, 'MR': mr, 'MRP1': mrp1, 'MRP2': mrp2, 'CR': cr})
    # print(regression_data)
    fitted_regression = ols("CR ~ MRM2 + MRM1 + MR + MRP1 + MRP2", regression_data).fit()
    # print(fitted_regression.resid)
    # print(fitted_regression.summary())
    # print(data["Date"][first_row + 2: last_row - 2])
    epsilon = pd.DataFrame({country: fitted_regression.resid})
    epsilon = epsilon.apply(lambda e: np.log(1 + e))
    epsilon = epsilon.set_index(weekly_returns['Date'][first_row + 2: last_row - 2])

    return epsilon

def negative_skewness(residuals):
    yearly_residual_squared = []
    yearly_residual_cubed = []
    negative_skewness_dataframe = pd.DataFrame()
    previous_year = residuals.iloc[0].name.split("/")[2]

    for index, row in residuals.iterrows():
        current_year = index.split("/")[2]

        if current_year != previous_year or index == residuals.iloc[-1].name:
            sum_cubed = sum(yearly_residual_cubed)
            sum_squared = sum(yearly_residual_squared)
            num_elements = len(yearly_residual_squared)
            ncskew_numerator = -((num_elements * (num_elements - 1) ** (3 / 2)) * sum_cubed)
            ncskew_denominator = (num_elements - 1) * (num_elements - 2) * (sum_squared) ** (3 / 2)
            ncskew = ncskew_numerator / ncskew_denominator
            ncskew.name = f'{12}/1/{previous_year}'
            negative_skewness_dataframe = negative_skewness_dataframe.append(ncskew)

            yearly_residual_squared = []
            yearly_residual_cubed = []

            yearly_residual_squared.append(row ** 2)
            yearly_residual_cubed.append(row ** 3)

        else:
            yearly_residual_squared.append(row ** 2)
            yearly_residual_cubed.append(row ** 3)



        previous_year = current_year


    return negative_skewness_dataframe


def down_up_volatility(residuals):
    yearly_residual_squared_down = []
    yearly_residual_squared_up = []
    duvol_dataframe = pd.DataFrame()
    previous_year = residuals.iloc[0].name.split("/")[2]

    for index, row in residuals.iterrows():
        current_year = index.split("/")[2]

        if current_year != previous_year or index == residuals.iloc[-1].name:
            sum_squared_down = sum(yearly_residual_squared_down)
            sum_squared_up = sum(yearly_residual_squared_up)
            num_elements_down = len(yearly_residual_squared_down)
            num_elements_up = len(yearly_residual_squared_up)

            duvol_numerator = (num_elements_up - 1) * sum_squared_down
            duvol_denominator = (num_elements_down - 1) * sum_squared_up
            duvol = np.log10(duvol_numerator / duvol_denominator)
            duvol.name = f'{12}/1/{previous_year}'
            duvol_dataframe = duvol_dataframe.append(duvol)


            yearly_residual_squared_down = []
            yearly_residual_squared_up = []


            if row.values[0] < 0:
                yearly_residual_squared_down.append(row ** 2)
            else:
                yearly_residual_squared_up.append(row ** 2)

        else:
            if row.values[0] < 0:
                yearly_residual_squared_down.append(row ** 2)
            else:
                yearly_residual_squared_up.append(row ** 2)


        previous_year = current_year

    return duvol_dataframe

# residual = index_model_regression(data, "MSCI World Gross Index USD", "MSCI Vietnam Gross Index USD_Adjusted")
# la = negative_skewness(residual)


# print(get_weekly_return_data_frame(data))

def get_weekly_return_data_frame_singular(data, country):
    weekly_prices_df = pd.DataFrame()
    all_weeks_df = pd.DataFrame()

    prices = pd.DataFrame(data, columns=[country, 'Date'])
    prices['dayOfWeek'] = prices.apply(lambda row: pd.to_datetime(row['Date']).dayofweek, axis=1)

    monday_close = 0
    initial_monday = False

    for i in range(len(prices.index) - 1):
        if not initial_monday:
            if not prices.isnull().iloc[i][country] and prices.iloc[i]['dayOfWeek'] == 0:
                monday_close = prices.iloc[i][country]
                initial_monday = True
                continue
            elif prices.iloc[i]['dayOfWeek'] == 6:
                weeks_return_df = pd.DataFrame({country: np.NaN}, index=[prices.iloc[i]['Date']])
                all_weeks_df = all_weeks_df.append(weeks_return_df)
                continue
            else:
                continue

        if prices.iloc[i]['dayOfWeek'] == 0:
            monday_close = prices.iloc[i][country]

        if prices.iloc[i]['dayOfWeek'] == 6:
            sunday_close = prices.iloc[i][country]
            sunday_date = prices.iloc[i]['Date']
            weekly_return = sunday_close / monday_close - 1
            weeks_return_df = pd.DataFrame({country: weekly_return}, index=[sunday_date])
            all_weeks_df = all_weeks_df.append(weeks_return_df)

    if weekly_prices_df.isnull:
        weekly_prices_df = weekly_prices_df.join(all_weeks_df, how='outer')
    else:
    #     weekly_prices_df = weekly_prices_df.join(all_weeks_df, how='left')
        weekly_prices_df = pd.concat([weekly_prices_df, all_weeks_df], join='inner', axis=1)
    print(weekly_prices_df)

    return weekly_prices_df



# weekly = get_weekly_return_data_frame(data)
# weekly.to_csv('weeklyReturns.csv')

neg_skew = pd.DataFrame()

weekly_returns = pd.read_csv('weeklyReturns.csv')

# #this works
residuals = index_model_regression(weekly_returns, "MSCI World Gross Index USD", "MSCI China Gross Index USD")
# residuals.to_csv("residtest.csv")
# print(residuals)

neg_skew = negative_skewness(residuals)
# neg_skew = negative_skewness(residuals)
# print(neg_skew)
# duvol = down_up_volatility(residuals)
# print(duvol)


# print(residuals)

# print(weekly_returns)
# for country in weekly_returns:
#     if country == 'Date' or country == "MSCI World Gross Index USD":
#         continue
#
#     residuals = index_model_regression(weekly_returns, "MSCI World Gross Index USD", country)
#     duvol_df = down_up_volatility(residuals)
#
#     negskew_df = negative_skewness(residuals)
#     if neg_skew.isnull:
#         neg_skew = neg_skew.join(negskew_df, how='outer')
#     else:
#         neg_skew = pd.concat([neg_skew, negskew_df], join='inner', axis=1)
#
#     neg_skew.rename(columns={country: f'{country}_NEGSKEW'}, inplace=True)
#
#     if neg_skew.isnull:
#         neg_skew = neg_skew.join(duvol_df, how='outer')
#     else:
#         neg_skew = pd.concat([neg_skew, duvol_df], join='inner', axis=1)
#
#     neg_skew.rename(columns={country: f'{country}_DUVOL'}, inplace=True)
#
#
#
#     print(country)
#
# print(neg_skew)
# neg_skew.to_csv('crash_risk_annual.csv')

# print(data['MSCI Europe & Middle East Gross Index USD'])