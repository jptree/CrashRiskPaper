import urllib.request
import pandas as pd
import json
import datetime
import numpy as np
from statsmodels.formula.api import ols

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



def ticker_dataframe(ticker):
    url = f'https://cloud.iexapis.com/stable/stock/{ticker}/chart/5y?token=pk_b26afc552fda4677a3aeb306804d69d5'
    df = pd.read_json(url)
    # df.to_csv(f"{ticker}.csv")
    return df


def day_of_week(date):
    # print(date)
    date_components = str(date).split("-")
    yyyy = int(date_components[0])
    mm = int(date_components[1])
    dd = int(date_components[2][:2])
    day = datetime.datetime(yyyy, mm, dd).weekday()
    return day


def dataframe_with_day_of_week(ticker):
    df = pd.read_csv(f'{ticker}.csv', index_col=0)
    df['dayOfWeek'] = df.apply(lambda row: day_of_week(row['date']), axis=1)
    return df

def dataframe_day(data):
    print(data)
    df = pd.DataFrame(data)
    df['dayOfWeek'] = df.apply(lambda row: day_of_week(row['date']), axis=1)
    return df


def dataframe_weekly_returns(data, ticker):
    startClose = 0
    y_close = 0
    y_date = 0
    y_day = 0
    weeklyReturns = pd.DataFrame()
    findMonday = False


    for index, row in data.iterrows():
        while findMonday != True:
            if row['dayOfWeek'] == 0:
                startClose = row['close']
                findMonday = True
        if row["dayOfWeek"] < y_day:
            wklyReturn = y_close / startClose - 1  # should this be log returns?
            df = pd.DataFrame({f'{ticker}_weeklyReturn': wklyReturn}, index=[y_date])
            weeklyReturns = weeklyReturns.append(df)
            startClose = row["close"]
        y_date = row["date"]
        y_close = row["close"]
        y_day = row["dayOfWeek"]

    return weeklyReturns
    # print(weeklyReturns)

def wkly_return(ticker):
    d = ticker_dataframe(ticker)
    d2 = dataframe_day(d)
    d3 = dataframe_weekly_returns(d2, ticker)
    return d3

# dasd = wkly_return("URTH")
# print(dasd)

x1 = [1, 3, 5, 6, 9, 6]
x2 = [3, 4, 5, 6, 7, 7]
y = [17.5, 26.5, 35.5, 42.5, 53.5, 7]


def weekly_return_regression(index_data_file_name, data):
    market_dataframe = pd.read_csv(index_data_file_name, index_col=0)

    for i in range(len(data.index)):
        if (i > 1) & (i < len(data.index) - 2):
            mrm2 = market_dataframe.iloc[i - 2]["weeklyReturn"]
            mrm1 = market_dataframe.iloc[i - 1]["weeklyReturn"]
            mr = market_dataframe.iloc[i]["weeklyReturn"]
            mrp1 = market_dataframe.iloc[i + 1]["weeklyReturn"]
            mrp2 = market_dataframe.iloc[i + 2]["weeklyReturn"]
            cr = data.iloc[i]["weeklyReturn"]
            regression_data = pd.DataFrame({'MRM2': mrm2, 'MRM1': mrm1, 'MR': mr, 'MRP1': mrp1, 'MRP2': mrp2, 'CR': cr})
            epsilon = ols("CR ~ MRM2 + MRM1 + MR + MRP1 + MRP2", regression_data).fit().bse

# data = pd.DataFrame({'X1': x1, 'Y': y, 'X2': x2})
# model = ols("Y ~ X1 + X2", data).fit()
# print(model.summary())
# print(model.bse)
