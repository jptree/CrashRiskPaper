import pandas as pd
import datetime
from statsmodels.formula.api import ols
import numpy as np
import matplotlib.pyplot as plt

# DATABASE_FILENAME = "MSCI Data.csv"
DATABASE_FILENAME = "MSCI Country.csv"
data = pd.read_csv(DATABASE_FILENAME)


def day_of_week(date):
    date_components = str(date).split("/")
    yyyy = int(date_components[2])
    mm = int(date_components[0])
    dd = int(date_components[1])
    day = datetime.datetime(yyyy, mm, dd).weekday()
    return day

def negative_skewness1(data, column, frequency="annual"):
    frequencies = ["annual", "monthly"]
    if frequency not in frequencies:
        raise ValueError(f'{frequency} not a valid frequency')

    if frequency == "monthly":
        daily_returns = data[column].pct_change()
        first_row = daily_returns.first_valid_index()
        last_row = daily_returns.last_valid_index()
        daily_returns_series = pd.Series()
        for row in range(last_row - first_row):
            try:
                current_row_month = str(data.iloc[first_row + row]["Date"]).split("/")[0]
                previous_row_month = str(data.iloc[first_row + row - 1]["Date"]).split("/")[0]
            except IndexError:
                print("Key Error")
                previous_row_month = str(data.iloc[first_row + row]["Date"]).split("/")[0]
            if current_row_month != previous_row_month:
                # calculate crash risk for the month
                print(daily_returns_series)
                daily_returns_series = []
            else:
                daily_returns_series.append(daily_returns.iloc[first_row + row])
                # calculate residual


    return daily_returns


def index_model_regression(data, benchmark, country):
    daily_returns = pd.DataFrame(data, columns=[country, benchmark]).pct_change()

    first_row = daily_returns[country].first_valid_index()
    last_row = daily_returns[country].last_valid_index()

    mrm2 = daily_returns[benchmark][first_row: last_row - 4].tolist()
    mrm1 = daily_returns[benchmark][first_row + 1: last_row - 3].tolist()
    mr = daily_returns[benchmark][first_row + 2: last_row - 2].tolist()
    mrp1 = daily_returns[benchmark][first_row + 3: last_row - 1].tolist()
    mrp2 = daily_returns[benchmark][first_row + 4: last_row].tolist()
    cr = daily_returns[country][first_row + 2: last_row - 2].tolist()

    regression_data = pd.DataFrame({'MRM2': mrm2, 'MRM1': mrm1, 'MR': mr, 'MRP1': mrp1, 'MRP2': mrp2, 'CR': cr})

    fitted_regression = ols("CR ~ MRM2 + MRM1 + MR + MRP1 + MRP2", regression_data).fit()

    epsilon = pd.DataFrame({country: fitted_regression.resid}).set_index(data["Date"][first_row + 2: last_row - 2])
    epsilon = epsilon.apply(lambda e: np.log(1 + e))

    return epsilon

def negative_skewness(residuals):
    monthly_residual_squared = []
    monthly_residual_cubed = []
    negative_skewness_dataframe = pd.DataFrame()
    previous_month = residuals.iloc[0].name.split("/")[0]

    for index, row in residuals.iterrows():
        current_month = index.split("/")[0]

        if current_month != previous_month or index == residuals.iloc[-1].name:
            sum_cubed = sum(monthly_residual_cubed)
            sum_squared = sum(monthly_residual_squared)
            num_elements = len(monthly_residual_squared)
            ncskew_numerator = -((num_elements * (num_elements - 1) ** (3 / 2)) * sum_cubed)
            ncskew_denominator = (num_elements - 1) * (num_elements - 2) * (sum_squared) ** (3 / 2)
            ncskew = ncskew_numerator / ncskew_denominator

            if previous_month == str(12):
                ncskew.name = f'{previous_month}/1/{(int(index.split("/")[2]) - 1)}'
            else:
                ncskew.name = f'{previous_month}/1/{(int(index.split("/")[2]))}'

            negative_skewness_dataframe = negative_skewness_dataframe.append(ncskew)

            monthly_residual_squared = []
            monthly_residual_cubed = []

            monthly_residual_squared.append(row ** 2)
            monthly_residual_cubed.append(row ** 3)

        else:
            monthly_residual_squared.append(row ** 2)
            monthly_residual_cubed.append(row ** 3)



        previous_month = current_month


    return negative_skewness_dataframe


def down_up_volatility(residuals):
    monthly_residual_squared_down = []
    monthly_residual_squared_up = []
    duvol_dataframe = pd.DataFrame()
    previous_month = residuals.iloc[0].name.split("/")[0]

    for index, row in residuals.iterrows():
        current_month = index.split("/")[0]

        if current_month != previous_month or index == residuals.iloc[-1].name:
            sum_squared_down = sum(monthly_residual_squared_down)
            sum_squared_up = sum(monthly_residual_squared_up)
            num_elements_down = len(monthly_residual_squared_down)
            num_elements_up = len(monthly_residual_squared_up)

            duvol_numerator = (num_elements_up - 1) * sum_squared_down
            duvol_denominator = (num_elements_down - 1) * sum_squared_up
            duvol = np.log10(duvol_numerator / duvol_denominator)
            if previous_month == str(12):
                duvol.name = f'{previous_month}/1/{(int(index.split("/")[2]) - 1)}'
            else:
                duvol.name = f'{previous_month}/1/{index.split("/")[2]}'
            duvol_dataframe = duvol_dataframe.append(duvol)


            monthly_residual_squared_down = []
            monthly_residual_squared_up = []


            if row.values[0] < 0:
                monthly_residual_squared_down.append(row ** 2)
            else:
                monthly_residual_squared_up.append(row ** 2)

        else:
            if row.values[0] < 0:
                monthly_residual_squared_down.append(row ** 2)
            else:
                monthly_residual_squared_up.append(row ** 2)


        previous_month = current_month

    return duvol_dataframe

def down_up_volatility_new(residuals):
    monthly_residual_squared_down = []
    monthly_residual_squared_up = []
    duvol_dataframe = pd.DataFrame()
    previous_month = residuals.iloc[0].name.split("/")[0]

    for index, row in residuals.iterrows():
        current_month = index.split("/")[0]

        if current_month != previous_month or index == residuals.iloc[-1].name:
            sum_squared_down = sum(monthly_residual_squared_down)
            sum_squared_up = sum(monthly_residual_squared_up)
            num_elements_down = len(monthly_residual_squared_down)
            num_elements_up = len(monthly_residual_squared_up)

            duvol_numerator = (num_elements_up - 1) * sum_squared_down
            duvol_denominator = (num_elements_down - 1) * sum_squared_up
            duvol = np.log10(duvol_numerator / duvol_denominator)
            if previous_month == str(12):
                duvol.name = f'{previous_month}/1/{(int(index.split("/")[2]) - 1)}'
            else:
                duvol.name = f'{previous_month}/1/{index.split("/")[2]}'
            duvol_dataframe = duvol_dataframe.append(duvol)


            monthly_residual_squared_down = []
            monthly_residual_squared_up = []


            if row.values[0] < 0:
                monthly_residual_squared_down.append(row ** 2)
            else:
                monthly_residual_squared_up.append(row ** 2)

        else:
            if row.values[0] < 0:
                monthly_residual_squared_down.append(row ** 2)
            else:
                monthly_residual_squared_up.append(row ** 2)


        previous_month = current_month

    return duvol_dataframe


# residual = index_model_regression(data, "MSCI World Gross Index USD", "MSCI Vietnam Gross Index USD_Adjusted")
# la = negative_skewness(residual)


def make_panel():
    big_df = pd.DataFrame()
    world_bank = pd.read_csv('WorldBankData.csv', encoding='latin1')
    for country in data:
        if country == 'Date' or country == 'MSCI World Gross Index USD':
            continue

        small_df = pd.DataFrame()
        print("Beginning... : " + country )
        resid = index_model_regression(data, 'MSCI World Gross Index USD', country)
        negskew = negative_skewness(resid)
        duvol = down_up_volatility(resid)


        small_df = negskew
        small_df = small_df.rename(columns={country: 'negskew'})



        small_df['duvol'] = duvol.apply(lambda row: row)

        small_df['Date'] = negskew.apply(lambda row: row.index)

        dates = small_df['Date'].str.split('/')
        small_df['year'] = dates.apply(lambda row: row[2])

        negskew = negskew.reset_index(drop=True)
        small_df['month'] = negskew.index

        country_list = country.split(' ')

        start = 'MSCI '
        end = ' Gross'
        s = country
        name = s[s.find(start) + len(start):s.rfind(end)]

        small_df['country'] = name

        a = world_bank.loc[world_bank['Indicator Code'] == 'NY.GDP.PCAP.PP.KD']
        b = a.loc[a['Country Name'] == name].T
        if b.empty:
            b = a.loc[a['Country Name'] == name].T
            if name == "Egypt":
                b = a.loc[a['Country Name'] == "Egypt, Arab Rep."].T
            elif name == "SRI Lanka":
                b = a.loc[a['Country Name'] == "Sri Lanka"].T
            elif name == "Bosnia And Herzegovina":
                b = a.loc[a['Country Name'] == "Bosnia and Herzegovina"].T
            elif name == "Russia":
                b = a.loc[a['Country Name'] == "Russian Federation"].T
            elif name == "Hong Kong":
                b = a.loc[a['Country Name'] == "Hong Kong SAR, China"].T
            elif name == "Korea":
                b = a.loc[a['Country Name'] == "Korea, Rep."].T
            else:
                print(name + " Not found in WorldBank")
                continue


        b = b.rename(columns={b.columns[0]: 'GDP'})
        b = b.iloc[3:]

        b['Date'] = b.apply(lambda row: '12/1/' + row.index)

        converted = pd.DataFrame()
        for index, row in b.iterrows():
            row['Date'] = '1/1/' + index
            converted = converted.append(row)
            row['Date'] = '2/1/' + index
            converted = converted = converted.append(row)
            row['Date'] = '3/1/' + index
            converted = converted.append(row)
            row['Date'] = '4/1/' + index
            converted = converted.append(row)
            row['Date'] = '5/1/' + index
            converted = converted.append(row)
            row['Date'] = '6/1/' + index
            converted = converted.append(row)
            row['Date'] = '7/1/' + index
            converted = converted.append(row)
            row['Date'] = '8/1/' + index
            converted = converted.append(row)
            row['Date'] = '9/1/' + index
            converted = converted.append(row)
            row['Date'] = '10/1/' + index
            converted = converted.append(row)
            row['Date'] = '11/1/' + index
            converted = converted.append(row)
            row['Date'] = '12/1/' + index
            converted = converted.append(row)

            # print(converted)

        converted.set_index('Date', inplace=True)

        small_df = small_df.join(converted)



        # print(small_df)
        big_df = big_df.append(small_df)

    big_df.to_csv("panel.csv")


def add_data(columnName, indicatorCode):
    data = pd.read_csv('geo2.csv')
    data = data.set_index('Unnamed: 0')
    new_data = data
    new_data[columnName] = np.nan


    world_bank = pd.read_csv('WorldBankData.csv', encoding='latin1')


    for index, row in data.iterrows():
        index_year = str(index).split('/')[2]
        current_country = row['country']

        if current_country == "Egypt":
            current_country == "Egypt, Arab Rep."
        elif current_country == "SRI Lanka":
            current_country = "Sri Lanka"
        elif current_country == "Bosnia And Herzegovina":
            current_country = "Bosnia and Herzegovina"
        elif current_country == "Russia":
            current_country = "Russian Federation"
        elif current_country == "Hong Kong":
            current_country = "Hong Kong SAR, China"
        elif current_country == "Korea":
            current_country = "Korea, Rep."
        # else:
        #     print(current_country + " Not found in WorldBank")
        #     continue





        value = world_bank.loc[(world_bank['Country Name'] == current_country) & (world_bank['Indicator Code'] == indicatorCode)][index_year]

        print(str(current_country) + str(value) + str(index_year))
        try:
            value = float(value)
        except TypeError:
            value = np.NAN

        new_data.loc[(new_data['country'] == current_country) & (new_data['Date'] == index), columnName] = float(value)

    new_data.to_csv('DataForGoodell.csv')


# add_data("gdpGrowth", "NY.GDP.MKTP.KD.ZG")


def add_data2(columnName, csv):
    data = pd.read_csv("panel.csv")
    data = data.set_index('Unnamed: 0')
    new_data = data
    new_data[columnName] = 69


    world_bank = pd.read_csv(csv, encoding='latin1')


    for index, row in data.iterrows():
        index_year = str(index).split('/')[2]
        current_country = row['country']

        if current_country == "Egypt":
            current_country == "Egypt, Arab Rep."
        elif current_country == "SRI Lanka":
            current_country = "Sri Lanka"
        elif current_country == "Bosnia And Herzegovina":
            current_country = "Bosnia and Herzegovina"
        elif current_country == "Russia":
            current_country = "Russian Federation"
        elif current_country == "Hong Kong":
            current_country = "Hong Kong SAR, China"
        elif current_country == "Korea":
            current_country = "Korea, Rep."
        # else:
        #     print(current_country + " Not found in WorldBank")
        #     continue





        value = world_bank.loc[(world_bank['Country/Territory'] == current_country)][index_year]

        print(str(current_country) + str(value) + str(index_year))
        try:
            value = float(value)
        except TypeError:
            value = np.NAN

        new_data.loc[(new_data['country'] == row['country']) & (new_data['Date'] == index), columnName] = float(value)

    new_data.to_csv('panel.csv')

#
# csv_list = ["Corruption.csv", "GovermentEffective.csv", "Political Stability.csv", "Regulatory.csv", "RuleOfLaw.csv", "VoiceAccountability.csv"]
# csv_list_name = ["corruption", "governmentEffectiveness", "politicalStability", "regulatoryQuality", "ruleOfLaw", "voiceAccountability"]
#
# for csv in range(len(csv_list)):
#     add_data2(csv_list_name[csv], csv_list[csv])

# add_data2("Corruption", "Corruption.csv")





def make_panel2():
    current_df = pd.read_csv('DataForGoodell.csv').set_index("Unnamed: 0")
    annual_cr = pd.read_csv('crash_risk_annual.csv').set_index("Unnamed: 0")
    current_df['negskew_annual'] = np.nan
    current_df['duvol_annual'] = np.nan


    for index, row in current_df.iterrows():
        index_year = str(index).split('/')[2]
        current_country = row['country']
        column_name_negskew = f"MSCI {current_country} Gross Index USD_NEGSKEW"
        column_name_duvol = f"MSCI {current_country} Gross Index USD_DUVOL"


        duvol_value = annual_cr[column_name_duvol][f'12/1/{index_year}']
        negskew_value = annual_cr[column_name_negskew][f'12/1/{index_year}']

        current_df.loc[(current_df['country'] == current_country) & (current_df['Date'] == index), 'negskew_annual'] = float(negskew_value)
        current_df.loc[(current_df['country'] == current_country) & (current_df['Date'] == index), 'duvol_annual'] = float(duvol_value)
        print(current_country, float(negskew_value), float(duvol_value))


    print(current_df)
    print(annual_cr)
    current_df.to_csv('PanelForGoodell.csv')

make_panel2()

# def make_panel3():
#     current_df = pd.read_csv('panel.csv').set_index("Unnamed: 0")
#     gpr = pd.read_csv('gpr_web_latest.csv')
#     current_df['geopoliticalRisk'] = np.nan
#     # print(current_df)
#
#
#     for index, row in current_df.iterrows():
#         current_country = f"GPR_{str(row['country']).upper()}"
#         # print(current_country)
#         # print(index)
#         try:
#             gpr_value = gpr.loc[gpr['Date'] == index, current_country]
#             print(float(gpr_value), str(index), str(current_country))
#
#             current_df.loc[(current_df['country'] == row['country']) & (current_df['Date'] == index), 'geopoliticalRisk'] = float(gpr_value)
#
#             continue
#         except KeyError:
#             continue
#
#
#     print(current_df)
#     current_df.to_csv('geo.csv')
#
#
# make_panel3()
