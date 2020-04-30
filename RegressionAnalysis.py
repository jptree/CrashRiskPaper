import statsmodels.api as sm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', 90500)
pd.set_option('display.max_rows', 200)

data = pd.read_csv("goodellPetriAnnual1.2.csv")
data = data.drop('Unnamed: 0', axis=1)


cncode_list = ['MAR', 'ARE', 'ARG', 'AUS', 'AUT', 'BEL', 'BGD', 'BGR', 'BHR', 'BIH', 'BRA', 'BWA', 'CAN', 'CHE', 'CHL',
               'CHN', 'COL', 'CZE', 'DEU', 'DNK', 'EGY', 'ESP', 'EST', 'FIN', 'FRA', 'GBR', 'GHA', 'GRC', 'HKG', 'HRV',
               'HUN', 'IDN', 'IND', 'IRL', 'ISR', 'ITA', 'JAM', 'JOR', 'JPN', 'KAZ', 'KEN', 'KOR', 'KWT', 'LBN', 'LKA',
               'LTU', 'MEX', 'MUS', 'MYS', 'NGA', 'NLD', 'NOR', 'NZL', 'OMN', 'PAK', 'PER', 'PHL', 'POL', 'PRT', 'QAT',
               'ROU', 'RUS', 'SGP', 'SRB', 'SVN', 'SWE', 'THA', 'TUN', 'TUR', 'UKR', 'USA', 'VNM', 'ZWE']


def simple_regression(target_variable, independent_variable, country_code=False):
    regression = pd.DataFrame()

    regression[independent_variable] = data[independent_variable]
    regression[target_variable] = data[target_variable]
    regression = regression.dropna()
    # regression = regression.drop(regression[regression[column] < -2].index)


    # to specify a country
    if country_code:
        X = regression.loc[data['cncode'] == country_code, independent_variable]
        y = regression.loc[data['cncode'] == country_code, target_variable]
    else:
        X = regression[independent_variable]
        y = regression[target_variable]

    # to look at aggregate
    # X = regression[colum n]
    # y = regression[target_variable]


    # print(X)
    # print(y)

    # plt.scatter(x=X, y=y)
    # plt.xlabel(column)
    # plt.ylabel("negskew")
    # plt.show()

    # model = sm.OLS(y, X).fit()
    # print(model.summary())

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    # print(model.summary())
    return model


def multiple_regression(target_variable, independent_variables):
    regression = pd.DataFrame()

    for var in independent_variables:
        regression[var] = data[var]

    regression[target_variable] = data[target_variable]
    regression = regression.dropna()

    X = regression[independent_variables]
    y = regression[target_variable]

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    return model

def hypothesis_1_country():

    summary = pd.DataFrame(columns=['country', 'cncode', 'duvol_r2', 'duvol_b1_pval', 'duvol_observ', 'negskew_r2', 'negskew_b1_pval', 'negskew_observ'])
    for country in cncode_list:
        print(country)
        country_name = data.loc[data['cncode'] == country, 'country'].iloc[0]


        try:
            negskew_model = simple_regression('negskew_annual', 'gdpGrowth', country)
            negskew_r2 = str(round(negskew_model.rsquared, 3))
            negskew_b1_pval = str(round(negskew_model.pvalues[1], 3))

            if float(negskew_b1_pval) <= float(0.05):
                negskew_b1_pval = str(negskew_b1_pval) + '**'

            negskew_observ = negskew_model.nobs

            duvol_model = simple_regression('duvol_annual', 'gdpGrowth', country)
            duvol_r2 = str(round(duvol_model.rsquared, 3))
            duvol_b1_pval = str(round(duvol_model.pvalues[1], 3))

            if float(duvol_b1_pval) <= float(0.05):
                duvol_b1_pval = str(duvol_b1_pval) + '**'

            duvol_observ = duvol_model.nobs
            summary = summary.append(
                {'country': country_name, 'cncode': country, 'duvol_r2': duvol_r2, 'duvol_b1_pval': duvol_b1_pval,
                 'duvol_observ': duvol_observ, 'negskew_r2': negskew_r2,
                 'negskew_b1_pval': negskew_b1_pval, 'negskew_observ': negskew_observ}, ignore_index=True)

        except ValueError:
            summary = summary.append({'country': country_name, 'cncode': country, 'duvol_r2': np.nan, 'duvol_b1_pval': np.nan,
                                  'duvol_observ': np.nan, 'negskew_r2': np.nan,
                                  'negskew_b1_pval': np.nan, 'negskew_observ': np.nan}, ignore_index=True)



    print(summary)
    summary.to_csv('output.csv')

def hypothesis_1_aggregate():

    summary = pd.DataFrame(columns=['country', 'cncode', 'duvol_r2', 'duvol_b1_pval', 'duvol_observ', 'negskew_r2', 'negskew_b1_pval', 'negskew_observ'])
    country_name = 'All Countries'

    try:
        negskew_model = simple_regression('negskew_annual', 'gdpGrowth')
        print(negskew_model.summary())
        negskew_r2 = str(round(negskew_model.rsquared, 3))
        negskew_b1_pval = str(round(negskew_model.pvalues[1], 3))

        if float(negskew_b1_pval) <= float(0.05):
            negskew_b1_pval = str(negskew_b1_pval) + '**'

        negskew_observ = negskew_model.nobs

        duvol_model = simple_regression('duvol_annual', 'gdpGrowth')
        print(duvol_model.summary())

        duvol_r2 = str(round(duvol_model.rsquared, 3))
        duvol_b1_pval = str(round(duvol_model.pvalues[1], 3))

        if float(duvol_b1_pval) <= float(0.05):
            duvol_b1_pval = str(duvol_b1_pval) + '**'

        duvol_observ = duvol_model.nobs
        summary = summary.append(
            {'country': country_name, 'cncode': 'ALL', 'duvol_r2': duvol_r2, 'duvol_b1_pval': duvol_b1_pval,
             'duvol_observ': duvol_observ, 'negskew_r2': negskew_r2,
             'negskew_b1_pval': negskew_b1_pval, 'negskew_observ': negskew_observ}, ignore_index=True)

    except ValueError:
        summary = summary.append({'country': country_name, 'cncode': 'ALL', 'duvol_r2': np.nan, 'duvol_b1_pval': np.nan,
                              'duvol_observ': np.nan, 'negskew_r2': np.nan,
                              'negskew_b1_pval': np.nan, 'negskew_observ': np.nan}, ignore_index=True)



    print(summary)
    # summary.to_csv('output.csv')

def hypothesis_2_aggregate():

    summary = pd.DataFrame(columns=['country', 'cncode', 'duvol_r2', 'duvol_b1_pval', 'duvol_observ', 'negskew_r2', 'negskew_b1_pval', 'negskew_observ'])
    country_name = 'All Countries'

    try:
        negskew_model = simple_regression('negskew_annual', 'gdpPerCapita')
        print(negskew_model.summary())
        negskew_r2 = str(round(negskew_model.rsquared, 3))
        negskew_b1_pval = str(round(negskew_model.pvalues[1], 3))

        if float(negskew_b1_pval) <= float(0.05):
            negskew_b1_pval = str(negskew_b1_pval) + '**'

        negskew_observ = negskew_model.nobs

        duvol_model = simple_regression('duvol_annual', 'gdpPerCapita')
        print(duvol_model.summary())
        duvol_r2 = str(round(duvol_model.rsquared, 3))
        duvol_b1_pval = str(round(duvol_model.pvalues[1], 3))

        if float(duvol_b1_pval) <= float(0.05):
            duvol_b1_pval = str(duvol_b1_pval) + '**'

        duvol_observ = duvol_model.nobs
        summary = summary.append(
            {'country': country_name, 'cncode': 'ALL', 'duvol_r2': duvol_r2, 'duvol_b1_pval': duvol_b1_pval,
             'duvol_observ': duvol_observ, 'negskew_r2': negskew_r2,
             'negskew_b1_pval': negskew_b1_pval, 'negskew_observ': negskew_observ}, ignore_index=True)

    except ValueError:
        summary = summary.append({'country': country_name, 'cncode': 'ALL', 'duvol_r2': np.nan, 'duvol_b1_pval': np.nan,
                              'duvol_observ': np.nan, 'negskew_r2': np.nan,
                              'negskew_b1_pval': np.nan, 'negskew_observ': np.nan}, ignore_index=True)



    print(summary)
    # summary.to_csv('output.csv')

def hypothesis_3_aggregate():

    negskew_model = multiple_regression('negskew_annual', ['corruption', 'governmentEffectiveness', 'politicalStability', 'regulatoryQuality', 'ruleOfLaw', 'voiceAccountability'])
    duvol_model = simple_regression('duvol_annual', ['corruption', 'governmentEffectiveness', 'politicalStability', 'regulatoryQuality', 'ruleOfLaw', 'voiceAccountability'])

    print(negskew_model.summary())
    print(duvol_model.summary())

def hypothesis_4_aggregate():
    negskew_model = multiple_regression('negskew_annual', ['idv'])
    duvol_model = simple_regression('duvol_annual', ['idv'])
    duvol_model1 = multiple_regression('duvol_annual', ['idv'])


    print(negskew_model.summary())
    print(duvol_model.summary())
    print(duvol_model1.summary())

def hypothesis_5_aggregate():
    negskew_model = multiple_regression('negskew_annual', ['uai', 'lto'])
    duvol_model = multiple_regression('duvol_annual', ['uai', 'lto'])

    print(negskew_model.summary())
    print(duvol_model.summary())

def hypothesis_6_aggregate():
    negskew_model = multiple_regression('negskew_annual', ['ivr'])
    duvol_model = multiple_regression('duvol_annual', ['ivr'])

    print(negskew_model.summary())
    print(duvol_model.summary())


def sample_aggregate(independent_variables, target_variables):
    table_header = ['Frequency', 'Percent']
    data_table = pd.DataFrame()

    years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
             2013, 2014, 2015, 2016, 2017, 2018, 2019]

    for i in range(len(independent_variables)):
        table_header.append(independent_variables[i])
        data_table[str(independent_variables[i])] = data[independent_variables[i]]

    for t in range(len(target_variables)):
        data_table[str(target_variables[t])] = data[target_variables[t]]

    data_table['year'] = data['year']
    data_table = data_table.dropna()
    sample = pd.DataFrame(columns=table_header)

    for year in years:
        ncskew = []
        duvol = []
        independent_data = []

        for i in range(len(independent_variables)):
            independent_data.append([])

        for index, row in data_table.iterrows():
            if int(row['year']) == year:
                ncskew.append(float(row['negskew_annual']))
                duvol.append(float(row['duvol_annual']))

                for i in range(len(independent_variables)):
                    independent_data[i].append(float(row[independent_variables[i]]))

        independent_average = []
        for i in range(len(independent_data)):
            independent_average.append(sum(independent_data[i]) / len(independent_data[i]))

        avg_nskew = sum(ncskew) / len(ncskew)
        avg_duvol = sum(duvol) / len(duvol)

        row = pd.Series(
            {'Frequency': len(ncskew), 'NCSKEW': avg_nskew, 'DUVOL': avg_duvol}, name=str(year))
        sample = sample.append(row)

        for i in range(len(independent_variables)):
            sample.loc[str(year), independent_variables[i]] = independent_average[i]

    sum_frequency = sample['Frequency'].sum()
    for index, row in sample.iterrows():
        sample.loc[sample.index == index, 'Percent'] = round(((row['Frequency'] / sum_frequency) * 100), 2)

    row = pd.Series({'Frequency': sum_frequency, 'Percent': sample['Percent'].sum(), 'DUVOL': sample['DUVOL'].mean(),
                     'NCSKEW': sample['NCSKEW'].mean()}, name='Total')
    sample = sample.append(row)

    for i in range(len(independent_variables)):
        sample.loc['Total', independent_variables[i]] = sample[independent_variables[i]].mean()


    sample.to_csv('sampletable.csv')
    print(sample)

