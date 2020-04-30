import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_columns', 90500)
pd.set_option('display.max_rows', 200)

# data = pd.read_csv('panel_with_annual.csv')
# print(data)
#
#
# for column in data:
#     if isinstance(data.iloc[0][column], float):
#         print(column)
#         plt.scatter(x=data.loc[data['month'] == 0, 'negskew'], y=data.loc[data['month'] == 0, column])
#         # plt.scatter(x=data['negskew'], y=data[column])
#         plt.xlabel('negskew')
#         plt.ylabel(column)
#         plt.show()

# for column in data:
#     if isinstance(data.iloc[0][column], float):
#         print(column)
#         plt.scatter(x=data.loc[data['month'] == 1, 'negskew_annual'], y=data.loc[data['month'] == 1, column])
#         plt.scatter(x=data['duvol'], y=data[column].apply(lambda row: np.log(row)))
#         # plt.scatter(x=data.loc[data['country'] == 'China', 'duvol_annual'], y=data.loc[data['country'] == 'China', column])
#         # plt.xlabel('duvol_annual')
#         plt.ylabel(column)
#         plt.show()



# data = pd.read_csv('PanelForGoodell.csv')
#
# plt.scatter(x=data['negskew'], y=data['gdpPerCapita'])
#
# #
# plt.scatter(x=data.loc[data['country'] == 'China', 'duvol_annual'], y=data.loc[data['country'] == 'China', column])
#  plt.xlabel('negskew')
# plt.ylabel('gdpPerCapita')
# plt.show()
# print(data)
#
# country_list = ['Indonesia', 'Argentina', 'Ukraine', 'Colombia', 'India', 'Israel', 'Malaysia',
#                 'Thailand', 'Brazil', 'China', 'Russia', 'Philippines', 'Mexico', 'Korea', 'Turkey']
#
#
# corr = data.corr()
#
# corr = data.groupby('country')['negskew']


# plt.matshow(corr)
# plt.show()

# a = corr.reset_index()
# print(a)

# id_df = corr.apply(lambda x: pd.Series(x.values)).unstack().transpose()
# print(id_df)
# print(id_df.corr())
# plt.matshow(id_df.corr())
# plt
# plt.show()

# for country in country_list:
#     dd = data.loc[data['country'] == country, ['negskew', 'geopoliticalRisk']]
#     # plt.scatter(x=dd['negskew'], y=dd['geopoliticalRisk'])
#     plt.scatter(x=dd['negskew'], y=dd['geopoliticalRisk'].apply(lambda row: np.log(row)))
#     plt.xlabel('negskew')
#     plt.ylabel('geopoliticalRisk')
#     plt.title(country)
#     plt.show()




def run_regression(dataTable, dependentColumn):
    for column in dataTable:
        # print(dataTable[dependentColumn].shift(periods=1))
        # print(dataTable[dependentColumn].shift(periods=2))
        # print(dataTable[dependentColumn].shift(periods=-2))
        plt.scatter(x=dataTable[dependentColumn], y=dataTable[column])
        plt.xlabel(dependentColumn)
        plt.ylabel(column)
        plt.title("Normal")
        plt.show()
        try:
            plt.scatter(x=dataTable[dependentColumn], y=dataTable[column].shift(periods=1))
        except ValueError:
            continue
        plt.xlabel(dependentColumn)
        plt.ylabel(column)
        plt.title("Shift +1")
        plt.show()
        plt.scatter(x=dataTable[dependentColumn], y=dataTable[column].shift(periods=2))
        plt.xlabel(dependentColumn)
        plt.ylabel(column)
        plt.title("Shift +2")
        plt.show()

data = pd.read_csv('goodellPetriAnnual1.2.csv')
plt.scatter(x=data.loc[data['cncode'] == 'USA', 'year'], y=data.loc[data['cncode'] == 'USA', 'duvol_annual'])
plt.xlabel("date")
plt.ylabel("duvol")
plt.show()

# run_regression(data, 'duvol_annual')


def add_hofstede():
    data = pd.read_csv('Copy of goodellPetriAnnual1.0.csv')
    # data = data.set_index('a')
    #
    hofstede = pd.read_csv('hofstede.csv')
    print(hofstede)
    # new = pd.DataFrame()

    for index, row in data.iterrows():

        current_country = row['country']

        if current_country == "Egypt":
            current_country = "Egypt, Arab Rep."
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

        try:
            pdi = hofstede.loc[hofstede['country'] == current_country, 'pdi'].iloc[0]
            uai = hofstede.loc[hofstede['country'] == current_country, 'uai'].iloc[0]
            idv = hofstede.loc[hofstede['country'] == current_country, 'idv'].iloc[0]
            mas = hofstede.loc[hofstede['country'] == current_country, 'mas'].iloc[0]
            lto = hofstede.loc[hofstede['country'] == current_country, 'lto'].iloc[0]
            ltowvs = hofstede.loc[hofstede['country'] == current_country, 'ltowvs'].iloc[0]
            ivr = hofstede.loc[hofstede['country'] == current_country, 'ivr'].iloc[0]
            cncode = hofstede.loc[hofstede['country'] == current_country, 'cncode'].iloc[0]

            data.loc[(data['country'] == row['country']), 'pdi'] = pdi
            data.loc[(data['country'] == row['country']), 'uai'] = uai
            data.loc[(data['country'] == row['country']), 'idv'] = idv
            data.loc[(data['country'] == row['country']), 'mas'] = mas
            data.loc[(data['country'] == row['country']), 'lto'] = lto
            data.loc[(data['country'] == row['country']), 'ltowvs'] = ltowvs
            data.loc[(data['country'] == row['country']), 'ivr'] = ivr
            data.loc[(data['country'] == row['country']), 'cncode'] = cncode

        except IndexError:
            print(f"{row['country']} not found!!!!")


def fix_governance():
    data = pd.read_csv('HofstedePanel.csv')
    previous_country = "hehe"
    p_governance = {}

    for index, row in data.iterrows():
        current_country = row['country']

        corruption = row['corruption']
        governmentEffectiveness = row['governmentEffectiveness']
        politicalStability = row['politicalStability']
        regulatoryQuality = row['regulatoryQuality']
        ruleOfLaw = row['ruleOfLaw']
        voiceAccountability = row['voiceAccountability']

        c_governance = {"corruption": corruption, "governmentEffectiveness": governmentEffectiveness,
                        "politicalStability": politicalStability, "regulatoryQuality": regulatoryQuality,
                        "ruleOfLaw": ruleOfLaw, "voiceAccountability": voiceAccountability}

        if current_country != previous_country:
            previous_country = current_country
            p_governance = c_governance
            continue
        else:
            for key in c_governance:
                if np.isnan(c_governance[key]) and not np.isnan(p_governance[key]):
                    data.loc[index, key] = p_governance[key]
                    c_governance[key] = p_governance[key]
            previous_country = current_country
            p_governance = c_governance

    print(data)
    data.to_csv("teh.csv")


def add_data(columnName, indicatorCode):
    data = pd.read_csv('teh2.csv')
    # data = data.set_index('Date')
    new_data = data
    new_data[columnName] = np.nan


    world_bank = pd.read_csv('WorldBankData.csv', encoding='latin1')

    print(world_bank)

    for index, row in data.iterrows():
        index_year = str(row['Date']).split('/')[2]
        current_country = row['cncode']

        value = world_bank.loc[(world_bank['Country Code'] == current_country) & (world_bank['Indicator Code'] == indicatorCode)][index_year]

        print(str(current_country) + str(value) + str(index_year))

        try:
            value = float(value)
        except TypeError:
            value = np.NAN

        new_data.loc[(new_data['cncode'] == current_country) & (new_data['Date'] == row['Date']), columnName] = float(value)

    print(new_data)
    new_data.to_csv("teh3.csv")


def add_data2(columnName, indicatorCode):
    data = pd.read_csv('goodellPetriAnnual1.1.csv')
    # data = data.set_index('Date')
    new_data = data
    new_data[columnName] = np.nan


    database = pd.read_csv('KOFGI Data.csv')


    for index, row in data.iterrows():
        index_year = str(row['Date']).split('/')[2]
        current_country = row['cncode']

        value = database.loc[(database['code'] == current_country) & (database['year'] == int(index_year)), indicatorCode]

        print(str(current_country) + str(value) + str(index_year))

        try:
            value = float(value)
        except TypeError:
            value = np.NAN

        new_data.loc[(new_data['cncode'] == current_country) & (new_data['Date'] == row['Date']), columnName] = float(value)

    print(new_data)
    new_data.to_csv("goodellPetriAnnual1.2.csv")
