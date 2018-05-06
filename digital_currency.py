# -*- coding: utf-8 -*-
"""
Pycharm Editor: Yiming Liu
This is a temporary script file.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 当列太多时不换行
pd.set_option('expand_frame_repr',False)
# 导入三家交易所的数据
df_okex_currency = pd.read_csv('E:\pyseven\digital_currency_project\data\changed_okex_day_data.csv',parse_dates=True,index_col='candle_begin_time')
df_binance_currency =pd.read_csv('E:/pyseven/digital_currency_project/data/binance_day_data.csv',parse_dates=True,index_col='candle_begin_time')
df_huobipro_currency = pd.read_csv('E:\pyseven\digital_currency_project\data\huobipro_day_data.csv',parse_dates=True,index_col='candle_begin_time')

# 将okex的symbol中间的 ‘_’ 删除
# df_okex_currency['symbol'] = df_okex_currency['symbol'].apply(lambda x:x.replace('_',''))
# df_okex_currency['symbol'] = df_okex_currency['symbol'].str.replace('_','')
# 将删除‘_'后的文件导出csv文件
# df_okex_currency.to_csv('E://pyseven//digital_currency_project//data//changed_okex_day_data.csv')

# ============================分别找出三个交易所的基准币============================
# okex的基准币
# huobipro_temp_list = list()
# for i in df_huobipro_currency['symbol'].value_counts().index:
#     if i.endswith('usdt'):
#         huobipro_temp_list.append(i)
#
# df_huobipro_currency_basic = df_huobipro_currency.loc[df_huobipro_currency['symbol'].isin(huobipro_temp_list)]
# df_huobipro_currency_basic.to_csv('E://pyseven//digital_currency_project//data//df_huobipro_currency_basic.csv')
# print(df_okex_currency_basic)

# ============================三大交易所每天的成交量对比============================
# huobipro成交量计算
# def huobipro_everday_total_volume(df_huobipro_currency):
#     '''
#
#     :param df_huobipro_currency:
#     :return:
#     '''
#     usdt_list = list()
#     for i in df_huobipro_currency['symbol'].value_counts().index:
#         if i.endswith('usdt'):
#             usdt_list.append(i) # usdt_list是huobipro交易所所有后缀为usdt的币种
#
#     df_huobipro_currency_usdt = df_huobipro_currency.loc[df_huobipro_currency['symbol'].isin(usdt_list)]
#     # 求每天的汇兑中间价
#     df_huobipro_currency_usdt['middle_rate'] = (df_huobipro_currency_usdt.loc[:,'high'] + df_huobipro_currency_usdt.loc[:,'low'])/2
#     df_huobipro_currency_usdt.reset_index(inplace=True)
#     df_huobipro_currency_usdt.rename(columns = {'symbol':'exchange_symbol'},inplace=True)
#     df_huobipro_currency_usdt = df_huobipro_currency_usdt[['candle_begin_time','exchange_symbol','middle_rate']]
#     df_huobipro_currency.reset_index(inplace=True)
#     df_total_coin_temp = pd.DataFrame()
#     for i in df_huobipro_currency['symbol'].value_counts().index:
#         if not i.endswith('usdt'):
#             df_everycoin_temp = df_huobipro_currency.loc[df_huobipro_currency['symbol']==i]
#             df_everycoin_temp['temp_symbol'] = np.array(df_everycoin_temp['symbol']) + np.array(['usdt'] * len(df_everycoin_temp))
#         else:
#             df_everycoin_temp['temp_symbol'] = df_huobipro_currency['symbol'].copy()
#         for ii in df_huobipro_currency_usdt['exchange_symbol'].value_counts().index:
#             for iii in df_everycoin_temp['temp_symbol']:
#                 if ii in iii:
#                     df_everycoin_temp['exchange_symbol'] = np.array([ii] * len(df_everycoin_temp))
#         df_total_coin_temp = df_total_coin_temp.append(df_everycoin_temp)
#
#     df_huobipro_currency_middle_rate = pd.merge(left=df_total_coin_temp,right=df_huobipro_currency_usdt,on=['candle_begin_time','exchange_symbol']
#                            ,how='inner',sort=False)
#     df_huobipro_currency_middle_rate['exchange_volume'] = df_huobipro_currency_middle_rate['middle_rate']*df_huobipro_currency_middle_rate['volume']
#     grouped_symbol_huobipro = df_huobipro_currency_middle_rate.groupby(by='candle_begin_time')
#     huobipro_everday_total_volume_temp = grouped_symbol_huobipro['exchange_volume'].sum()
#     huobipro_everday_total_volume = huobipro_everday_total_volume_temp.to_frame()
#     huobipro_everday_total_volume.rename(columns={ 'exchange_volume':'huobipro_total_volume'},inplace=True)
#     return huobipro_everday_total_volume
#
#
# # binance成交量计算
# def binance_everday_total_volume(df_binance_currency):
#     '''
#
#     :param df_binance_currency:
#     :return:
#     '''
#     usdt_list = list()
#     for i in df_binance_currency['symbol'].value_counts().index:
#         if i.endswith('USDT'):
#             usdt_list.append(i) # usdt_list是huobipro交易所所有后缀为usdt的币种
#
#     df_binance_currency_usdt = df_binance_currency.loc[df_binance_currency['symbol'].isin(usdt_list)]
#     # 求每天的汇兑中间价
#     df_binance_currency_usdt['middle_rate'] = (df_binance_currency_usdt.loc[:,'high'] + df_binance_currency_usdt.loc[:,'low'])/2
#     df_binance_currency_usdt.reset_index(inplace=True)
#     df_binance_currency_usdt.rename(columns = {'symbol':'exchange_symbol'},inplace=True)
#     df_binance_currency_usdt = df_binance_currency_usdt[['candle_begin_time','exchange_symbol','middle_rate']]
#
#     df_binance_currency.reset_index(inplace=True)
#     df_total_coin_temp = pd.DataFrame()
#     for i in df_binance_currency['symbol'].value_counts().index:
#         if not i.endswith('USDT'):
#             df_everycoin_temp = df_binance_currency.loc[df_binance_currency['symbol']==i]
#             df_everycoin_temp['temp_symbol'] = np.array(df_everycoin_temp['symbol']) + np.array(['USDT'] * len(df_everycoin_temp))
#         else:
#             df_everycoin_temp['temp_symbol'] = df_binance_currency['symbol'].copy()
#         for ii in df_binance_currency_usdt['exchange_symbol'].value_counts().index:
#             for iii in df_everycoin_temp['temp_symbol']:
#                 if ii in iii:
#                     df_everycoin_temp['exchange_symbol'] = np.array([ii] * len(df_everycoin_temp))
#         df_total_coin_temp = df_total_coin_temp.append(df_everycoin_temp)
#
#     df_binance_currency_middle_rate = pd.merge(left=df_total_coin_temp,right=df_binance_currency_usdt,on=['candle_begin_time','exchange_symbol']
#                            ,how='inner',sort=False)
#     df_binance_currency_middle_rate['exchange_volume'] = df_binance_currency_middle_rate['middle_rate']*df_binance_currency_middle_rate['volume']
#     grouped_symbol_binance = df_binance_currency_middle_rate.groupby(by='candle_begin_time')
#     binance_everday_total_volume_temp = grouped_symbol_binance['exchange_volume'].sum()
#     binance_everday_total_volume = binance_everday_total_volume_temp.to_frame()
#     binance_everday_total_volume.rename(columns={ 'exchange_volume':'binance_total_volume'},inplace=True)
#     return binance_everday_total_volume
#
# # okex成交量计算
# def okex_everday_total_volume(df_okex_currency):
#     '''
#
#     :param df_okex_currency: okex交易所原始数据
#     :return: okex交易所每日以usdt表示的总成交量
#     '''
#     usdt_list = list()
#     for i in df_okex_currency['symbol'].value_counts().index:
#         if i.endswith('_usdt'):
#             usdt_list.append(i) # usdt_list是okex交易所所有后缀为_usdt的币种
#
#     df_okex_currency_usdt = df_okex_currency.loc[df_okex_currency['symbol'].isin(usdt_list)]
#     # 求每天的汇兑中间价
#     df_okex_currency_usdt['middle_rate'] = (df_okex_currency_usdt.loc[:,'high'] + df_okex_currency_usdt.loc[:,'low'])/2
#     df_okex_currency_usdt.reset_index(inplace=True)
#     df_okex_currency_usdt.rename(columns = {'symbol':'exchange_symbol'},inplace=True)
#     df_okex_currency_usdt = df_okex_currency_usdt[['candle_begin_time','exchange_symbol','middle_rate']]
#
#     # 在原始数据添加一列汇兑的symbol
#     df_okex_currency.reset_index(inplace=True)
#     for i in range(len(df_okex_currency)):
#         underline_location = df_okex_currency.loc[i,'symbol'].find('_')
#         df_okex_currency.loc[i,'exchange_symbol'] = df_okex_currency.loc[i,'symbol'][(underline_location+1):] + '_usdt'
#     # 将汇兑价格与原始数据每行对应合并
#     df_okex_currency_middle_rate = pd.merge(left=df_okex_currency,right=df_okex_currency_usdt,on=['candle_begin_time','exchange_symbol']
#                    ,how='inner',sort=False)
#     df_okex_currency_middle_rate['exchange_volume'] = df_okex_currency_middle_rate['middle_rate']*df_okex_currency_middle_rate['volume']
#     grouped_symbol_okex = df_okex_currency_middle_rate.groupby(by='candle_begin_time')
#     okex_everday_total_volume_temp = grouped_symbol_okex['exchange_volume'].sum()
#     okex_everday_total_volume = okex_everday_total_volume_temp.to_frame()
#     okex_everday_total_volume.rename(columns={ 'exchange_volume':'okex_total_volume'},inplace=True)
#     return okex_everday_total_volume
#
# # 将三个交易所每日成交量合并
# total_everday_return_temp = pd.merge(okex_everday_total_volume(df_okex_currency), binance_everday_total_volume(df_binance_currency),left_index=True,right_index=True,how='outer')
# total_everday_return = pd.merge(total_everday_return_temp,huobipro_everday_total_volume(df_huobipro_currency), left_index=True, right_index=True,how='outer')
#
# # 作图对比
# # plt.plot(total_everday_return.index,total_everday_return[['okex_total_volume','binance_total_volume','huobipro_total_volume']])
# # total_everday_return.plot()
# # plt.show()
#
# total_everday_return.fillna(value=0,inplace=True)
# total_everday_return.to_csv('E://pyseven//digital_currency_project//data//total_everyday_return.csv')
# # print(total_everday_return)
# exit()
# # total_everday_return.plot(['okex_total_volume',  'binance_total_volume' , 'huobipro_total_volume'])
# # print(total_everday_return)
#
#
# # ============================三大交易所每日成交币对之和对比============================
# grouped_everyday_okex = df_okex_currency.groupby(by='candle_begin_time')
# okex_everday_total_volume_temp = grouped_everyday_okex['symbol'].count()
# okex_everday_total_volume = okex_everday_total_volume_temp.to_frame()
# okex_everday_total_volume.rename(columns={ 'symbol':'okex_everyday_dealnum'},inplace=True)
#
# grouped_everyday_binance = df_binance_currency.groupby(by='candle_begin_time')
# binance_everday_total_volume_temp = grouped_everyday_binance['symbol'].count()
# binance_everday_total_volume = binance_everday_total_volume_temp.to_frame()
# binance_everday_total_volume.rename(columns={ 'symbol':'binance_everyday_dealnum'},inplace=True)
#
# grouped_everyday_huobipro = df_huobipro_currency.groupby(by='candle_begin_time')
# huobipro_everday_total_volume_temp = grouped_everyday_huobipro['symbol'].count()
# huobipro_everday_total_volume = huobipro_everday_total_volume_temp.to_frame()
# huobipro_everday_total_volume.rename(columns={ 'symbol':'huobipro_everyday_dealnum'},inplace=True)
#
# total_everday_dealnum_temp = pd.merge(okex_everday_total_volume,binance_everday_total_volume,
#                                       left_index=True,right_index=True,how='outer')
# total_everday_dealnum = pd.merge(total_everday_dealnum_temp,huobipro_everday_total_volume,
#                                  left_index=True,right_index=True,how='outer')
# total_everday_dealnum.fillna(value=0,inplace=True)
# total_everday_dealnum.plot()
# plt.show()
# exit()
#
#
# # ============================三大交易所上市币的数量对比============================
def coin_mumber(df):
    '''

    :param df:
    :return:
    '''
    coin_number = len(df['symbol'].value_counts().index)
    return coin_number
# oke_coin_number = coin_mumber(df_okex_currency)
# binance_coin_number = coin_mumber(df_binance_currency)
# huobipro_coin_number = coin_mumber(df_huobipro_currency)

print(df_okex_currency['symbol'].value_counts())

exit()

# rects=plt.bar(left=(1,2,3),height=(oke_coin_number,binance_coin_number,huobipro_coin_number),color= ('b','g','r'),width=0.2,align = 'center',yerr=0.000001)
# plt.xticks((1,2,3),('okex_pubilc_coins','binance_public_coins','huobipro_public_coins'))
# plt.show()
# exit()


# # ============================三大交易所上市币每天平均涨幅对比============================
def everyday_change(df):
    '''

    :param df:
    :return:
    '''
    df['everday_change']  = (df['close']/df['open']) - 1.0
    df = df[df['everday_change'] <= 100] #除去当日涨跌幅超过100倍的数据
    grouped_exchange = df.groupby('candle_begin_time')
    exchange_everday_mean_change = grouped_exchange['everday_change'].mean()
    return exchange_everday_mean_change
okex_everyday_change = everyday_change(df_okex_currency)
okex_everyday_change = okex_everyday_change.to_frame()
okex_everyday_change.rename(columns ={'everday_change':'okex_everyday_change'},inplace=True)
okex_everyday_change['okex_everyday_deposit_curve'] = okex_everyday_change['okex_everyday_change']+1.0
okex_everyday_change['okex_everyday_deposit_curve'] = okex_everyday_change['okex_everyday_deposit_curve'].cumprod()
okex_everyday_change['okex_everyday_deposit_curve'] = okex_everyday_change['okex_everyday_deposit_curve'] - 1.0

#
binance_everyday_change = everyday_change(df_binance_currency)
binance_everyday_change = binance_everyday_change.to_frame()
binance_everyday_change.rename(columns ={'everday_change':'binance_everyday_change'},inplace=True)
binance_everyday_change['binance_everyday_deposit_curve'] = binance_everyday_change['binance_everyday_change']+1.0
binance_everyday_change['binance_everyday_deposit_curve'] = binance_everyday_change['binance_everyday_deposit_curve'].cumprod()
binance_everyday_change['binance_everyday_deposit_curve'] = binance_everyday_change['binance_everyday_deposit_curve'] - 1.0

#
huobipro_everyday_change = everyday_change(df_huobipro_currency)
huobipro_everyday_change = huobipro_everyday_change.to_frame()
huobipro_everyday_change.rename(columns ={'everday_change':'huobipro_everyday_change'},inplace=True)
huobipro_everyday_change['huobipro_everyday_deposit_curve'] = huobipro_everyday_change['huobipro_everyday_change']+1.0
huobipro_everyday_change['huobipro_everyday_deposit_curve'] = huobipro_everyday_change['huobipro_everyday_deposit_curve'].cumprod()
huobipro_everyday_change['huobipro_everyday_deposit_curve'] = huobipro_everyday_change['huobipro_everyday_deposit_curve'] - 1.0
#
contrast_everyday_change_temp = pd.merge(okex_everyday_change,binance_everyday_change,left_index=True,right_index=True,how='outer')
contrast_everyday_change = pd.merge(contrast_everyday_change_temp,huobipro_everyday_change,left_index=True,right_index=True,how='outer')
contrast_everyday_change.to_csv('E://pyseven//digital_currency_project//data//exchange_deposit_curve.csv')


# contrast_everyday_change.plot()
figure_1 = plt.figure()
ax1 = figure_1.add_subplot(3,1,1)
ax1.plot(okex_everyday_change, 'b', label = 'okex_everyday_change')
ax1.legend()
ax2 = figure_1.add_subplot(3,1,2)
ax2.plot(binance_everyday_change,'g',label = 'binance_everyday_change')
ax2.legend()
ax3 = figure_1.add_subplot(3,1,3)
ax3.plot(huobipro_everyday_change,'r',label = 'huobipro_everyday_change')
ax3.legend()
plt.show()
exit()


# # ============================三大交易所上市币破发数量对比============================
def break_initial_number_percent(df):
    '''

    :param df:
    :return:
    '''
    df.reset_index(inplace=True)
    grouped_kinds =df.groupby('symbol')
    # okex每只股票最后一天的收盘价
    df_last_close = grouped_kinds['close'].last()
    df_last_close_temp = df_last_close.to_frame()
    # 交易所每只股票第一天的开盘价
    df_initial_open = grouped_kinds['open'].first()
    df_initial_open_temp = df_initial_open.to_frame()
    df_open_close_temp = pd.merge(df_last_close_temp,df_initial_open_temp,left_index=True,right_index=True)
    df_open_close_temp.loc[df_open_close_temp['close'] < df_open_close_temp['open'],'break_initial'] = 1
    df_open_close_temp.fillna(value=0,inplace=True)
    # 计算okex交易所上市币破发数量及比率 1为破发 0为未破发
    initial_break_number = df_open_close_temp['break_initial'].value_counts().loc[1]
    initial_break_percent = df_open_close_temp['break_initial'].value_counts().loc[1]/float(len(df_open_close_temp))
    return (initial_break_number,initial_break_percent)
    # return  initial_break_number
okex_break_initial_num = break_initial_number_percent(df_okex_currency)
binance_break_initial_num = break_initial_number_percent(df_binance_currency)
huobipro_break_initial_num = break_initial_number_percent(df_huobipro_currency)
# plt.bar(left=(1,2,3), height=(okex_break_initial_num,binance_break_initial_num,huobipro_break_initial_num),width=0.2, align='center',yerr = 0.000001)
# plt.xticks((1,2,3),('okex_break_initial_num','binance_break_initial_num','huobipro_break_initial_num'))
# plt.title('break initial number of three exchanges')
# plt.show()
print(okex_break_initial_num,binance_break_initial_num,huobipro_break_initial_num)
exit()


