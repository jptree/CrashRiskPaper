import pandas as pd

pd.set_option('display.max_rows', 1500)
pd.set_option('display.max_columns', 90500)
pd.set_option('display.width', 1000)

world_bank = pd.read_csv('WorldBankData.csv', encoding='latin1')


#
# # df = pd.DataFrame()
# # for chunk in pd.read_csv('WorldBankData.csv', chunksize=1000):
# #     df = pd.concat([df, chunk], ignore_index=True)
# #
# # print(df)
#
#
#
#
#
# # print(world_bank.T)
#
#
# negskew = pd.read_csv('NEGSKEW Annual.csv')
# negskew.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
# negskew = negskew.set_index("Date")
#
#
#
#
# # # print(world_bank['BX.PEF.TOTL.CD.WD'])
# # # df = df.concat[]
# # negskew = negskew.set_index('Date')
# # negskew.index.name = 'Date'
# a = world_bank.loc[world_bank['Indicator Code'] == 'NY.GDP.PCAP.PP.KD']
# ddf = pd.DataFrame()
# for index, row in a.iterrows():
#     series = pd.Series(data={'12/1/2000': row['2000'], '12/1/2001': row['2001'], '12/1/2002': row['2002'], '12/1/2003': row['2003'],
#                       '12/1/2004': row['2004'], '12/1/2005': row['2005'], '12/1/2006': row['2006'], '12/1/2007': row['2007'],
#                       '12/1/2008': row['2008'], '12/1/2009': row['2009'], '12/1/2010': row['2010'], '12/1/2011': row['2011'],
#                       '12/1/2012': row['2012'], '12/1/2013': row['2013'], '12/1/2014': row['2014'], '12/1/2015': row['2015'],
#                       '12/1/2016': row['2016'], '12/1/2017': row['2017'], '12/1/2018': row['2018'], '12/1/2019': row['2019']},
#                        name=row['Country Name'])
#
#
#     ddf[row['Country Name']] = series
#
#
#
# negskew = negskew.join(ddf)
#
#
# mList = []
# for x in negskew:
#     if "_NEGSKEW" not in x:
#         mList.append(x)
#         # print(x)
#
# mList.append('Date')
#
# negskew = negskew.reset_index().melt(id_vars=mList, value_name='NEGSKEW', var_name=['MSCI Country Index']).set_index(['MSCI Country Index', 'Date'])
#
# print(negskew.head)
# negskew.to_csv('test.csv')


neg = pd.read_csv('')