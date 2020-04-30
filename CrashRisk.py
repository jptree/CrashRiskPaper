import pandas as pd
import datetime
import math
from statsmodels.formula.api import ols

pd.set_option('display.max_rows', 1500)
pd.set_option('display.max_columns', 90500)
pd.set_option('display.width', 1000)


def day_of_week(date):  # this function is no longer needed but still kind of cool to look at
    date_components = str(date).split("-")  # function takes in the "date" parameter, str() turns an object into a string, .split() is a method for string objects that will turn the object into a list by a specified delimeter
    # for example, '2019-03-14' becomes a string, then this string is turned into ['2019', '03', '14']

    yyyy = int(date_components[0])  # the 0th element is turned into an integer using int() and assigned to variable: yyyy
    mm = int(date_components[1])  # the 1st element is turned into an integer...
    dd = int(date_components[2][:2])  # the 2nd element is actually '14 00:00:00:00' or something, so the [:2] means I only want the characters before the 2nd character
    day = datetime.datetime(yyyy, mm, dd).weekday()  # creates a datetime object and then returns its weekday value
    return day  # return statement or what the value of the function being called will equal to

def negative_skewness_formula(num, sum_third, sum_second):  # function for nskew; num is number of elments; sum_third is sum of the cubed weekly returns; sum_second is sum of squared weekly returns
    numerator = num * (num - 1) ** (3/2) * sum_third  # ** is how you do exponents
    denominator = (num - 1) * (num - 2) * sum_second ** (3/2)  # I hope my PEMDAS holds true here
    return -1 * (numerator / denominator)


class CountryCrashRisk():  # class structure for crash risk. I thought it was a novel idea to store all the data for crash risk in a class. Classes are not a requirement for this language
    """Returns various functionality in the process of calculating crash risk"""  # this is the description and it can be called by printing CountryCrashRisk().__doc__

    def __init__(self, ticker):  # init function, this is required when making a class I think.
        self.ticker = ticker  # this ticker value is needed to make a class because it is vital info

    def get_prices_data_frame(self):  # a dataframe is an object created in the Pandas library. This library is comparable to the R language
        # url = f'https://cloud.iexapis.com/stable' \
              # f'/stock/{self.ticker}/chart/5y?token=pk_b26afc552fda4677a3aeb306804d69d5'
        url = f'{self.ticker}.json'  # I am setting the URL to my local reference to a file I have saved so I do not keep calling the API. Above is the implementation of actually accessing the API
        df_prices = pd.read_json(path_or_buf=url)  # "pd" refers to the pandas library. The read.json() method takes data from a JSON file and creates a dataframe--a table of data
        df_prices.set_index('date', inplace=True)  # this sets the index column to what used to be the 'date' column.
        df_prices['dayOfWeek'] = df_prices.apply(lambda row: row.name.dayofweek, axis=1)  # this creates a new column with a header of "dayOfWeek" and the values are the week day: 0=monday, 1=tuesday, 3=wednesday...
        return df_prices  # this function will return this data

    def get_weekly_return_data_frame(self):  # this function goes through a daily dataframe of historical prices and calculates weekly return--Friday/Monday - 1 (if Monday and Friday are not available, the program finds the next possible start or finish)
        prices = self.get_prices_data_frame()  # gets the prices data from the other method
        weekly_data_frame = pd.DataFrame()  # creates a new blank dataframe to later be added to
        found_initial_monday = False  # boolean variable to essentially skip the first mid week (if applicable) in order to properly start on a Monday
        monday_close = 0  # declare a new variable so I don't get an error later on; this represents the closing price on Monday

        for i in range(len(prices.index) - 1):  # for loop, this will loop through all of the prices dataframe except for the last row. I will get an error if I do not subtract 1 because later in my code I am referencing the next row. If you're at the end of the dataframe and you reference nth row + 1, you will get an error because it does not exist
            row_weekday = prices.iloc[i]['dayOfWeek']  # this is the current row's day of week number. the iloc[] method takes an integer and putting another [] next to this will refer to the column desired
            row_close = prices.iloc[i]['close']  # same as above, but referenced ['close'] column
            row_date = prices.iloc[i].name  # this gets the name of the row index. My index column are dates: 2019-05-15

            if not found_initial_monday:  # this will check because found_initial_monday is currently False, but when negated, it is True so this if statement will run
                if row_weekday == 0:  # checks if the current row's weekday is equal to zero or Monday
                    found_initial_monday = True  # if this succeeds, then the variable gets set to True so this if statement will no longer run
                    monday_close = row_close  # this assigns the Monday close value to the current row's close

            if (row_weekday > prices.iloc[i + 1]['dayOfWeek']) & found_initial_monday:  # if the current row's weekday is greater than the next row's weekday, then that means the next row is the start of a new week. 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0...
                weekly_return = row_close / monday_close - 1  # calculates return
                weekly_return_df = pd.DataFrame({'weeklyReturn': weekly_return}, index=[row_date])  # this is a temporary dataframe for the purposes of appending the next dataframe. I am adding data to the 'weeklyReturn' column, and the data is weekly_return, the row's index is the current row's date
                weekly_data_frame = weekly_data_frame.append(weekly_return_df)  # this is my previously declared dataframe. We will append the just made dataframe to this one
                monday_close = prices.iloc[i + 1]['close']  # we know now that the next row is a start of week


        return weekly_data_frame  # returns the weekly dataframe to be used in the next method

    def get_residual_data_frame(self, market_data_frame):
        weekly_returns_data_frame = self.get_weekly_return_data_frame()  # this takes in weekly return data from the market
        negative_skewness = {}
        market_data_frame_length = len(market_data_frame.index)
        market_lag_two = []
        market_lag_one = []
        market = []
        market_lead_one = []
        market_lead_two = []
        country = []

        # Potentially code logic for treatment of unequal data start dates

        for i in range(market_data_frame_length - 2)[2:]:  # for loop but I want to start at the second element and go till the end of the dataframe minus two. This is due to lead and lag references
            current_row_year = market_data_frame.iloc[i].name.year  # getting the year is important. We will need to when the year changes. Much like the calculation of when the next monday occurs
            next_row_year = market_data_frame.iloc[i + 1].name.year  # this will be used to see if the next row's date (the next row's year) is greater than the current
            if current_row_year == next_row_year:  # if current year and next row's year are the same, lets add market data to their respective lists
                market_lag_two.append(market_data_frame.iloc[i - 2]['weeklyReturn'])  # this is the lag by 2 element
                market_lag_one.append(market_data_frame.iloc[i - 1]['weeklyReturn'])  # this is the lag by 1 element
                market.append(market_data_frame.iloc[i]['weeklyReturn'])  # this has no lag or lead
                market_lead_one.append(market_data_frame.iloc[i + 1]['weeklyReturn'])  # this is the lead by 1 element
                market_lead_two.append(market_data_frame.iloc[i + 2]['weeklyReturn'])  # this is the lead by 2 element
                country.append(weekly_returns_data_frame.iloc[i]['weeklyReturn'])  # this is the country's return with no lead or lag. This will be used as our dependent variable in the regression
            else:  # if the two years in question are not the same, lets do this
                regression_data = pd.DataFrame({  # we run the regression because we know that the year is completed
                    'MLAG2': market_lag_two, 'MLAG1': market_lag_one, 'M': market,  # I am forming a dataframe with all of the data from the above lists
                    'MLEAD1': market_lead_one, 'MLEAD2': market_lead_two, 'C': country})
                residuals = list(ols("C ~ MLAG2 + MLAG1 + M + MLEAD1 + MLEAD2", regression_data).fit().resid + 1)  # this runs a regression through a statistics library.  .fit() is called to run the regression, .resid means I just want the residuals returned. I add 1 and make this whole thing a list
                 # we now have residuals of weekly returns added with 1. Now we must cube then sum or square then sum
                sum_third_power = 0  # this is the sum of the cubed weekly returns
                sum_second_power = 0  # this is the sum of the squared weekly returns
                for x in residuals:
                    sum_third_power = sum_third_power + (math.log(x)**3)  # we are looping through every element in my residuals list and adding this to itself
                    sum_second_power = sum_second_power + (math.log(x)**2)
                negative_skewness[current_row_year] = negative_skewness_formula(len(residuals), sum_third_power, sum_second_power)  # we are forming a list. Keep in mind, this is in a bigger loop for each year

                market_lag_two = []  # we need to clear the lists to be appended to again. we do not want the previous years data in this list
                market_lag_one = []
                market = []
                market_lead_one = []
                market_lead_two = []
                country = []


        return negative_skewness



EWG = CountryCrashRisk("EWG")
URTH = CountryCrashRisk("URTH")
URTH_returns = URTH.get_weekly_return_data_frame()


nskew_germany = EWG.get_residual_data_frame(URTH_returns)
print(nskew_germany)
