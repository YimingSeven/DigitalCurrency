# -*- coding: utf-8 -*-
"""
Pycharm Editor: Mr.seven
This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 当列太多时不换行
pd.set_option('expand_frame_repr',False)

# 导入三家交易所的基准币数据
df_okex_basic_currency = pd.read_csv('E:\pyseven\digital_currency_project\data\df_okex_currency_basic.csv',parse_dates=True,index_col='candle_begin_time')
df_binance_basic_currency =pd.read_csv('E:/pyseven/digital_currency_project/data/df_binance_currency_basic.csv',parse_dates=True,index_col='candle_begin_time')
df_huobipro_basic_currency = pd.read_csv('E:\pyseven\digital_currency_project\data\df_huobipro_currency_basic.csv',parse_dates=True,index_col='candle_begin_time')

# 导入三家交易所的原始数据
df_okex_currency = pd.read_csv('E:\pyseven\digital_currency_project\data\changed_okex_day_data.csv',parse_dates=True,index_col='candle_begin_time')
df_binance_currency =pd.read_csv('E:/pyseven/digital_currency_project/data/binance_day_data.csv',parse_dates=True,index_col='candle_begin_time')
df_huobipro_currency = pd.read_csv('E:\pyseven\digital_currency_project\data\huobipro_day_data.csv',parse_dates=True,index_col='candle_begin_time')

# df_okex_currency.drop(df_okex_currency[df_okex_currency['symbol'] == 'ltcbtc'].index,inplace=True)
# print(df_okex_basic_currency)
# exit()
# ============================以okex为例，计算主法币的交易量============================
df_okex_basic_currency['basic_currency'] = df_okex_basic_currency['symbol'].str.replace('usdt','')
df_binance_basic_currency['basic_currency'] = df_binance_basic_currency['symbol'].str.replace('USDT','')
df_huobipro_basic_currency['basic_currency'] = df_huobipro_basic_currency['symbol'].str.replace('usdt','')
# print(df_okex_basic_currency)
# exit()
# 在原始数据中筛选出主法币的成交对
def filter_basic_coin(df_okex_basic_currency,df_okex_currency):
    '''

    :param df_okex_basic_currency:
    :param df_okex_currency:
    :return:
    '''
    df_okex_basic_deal = pd.DataFrame(columns=df_okex_currency.columns)
    # print(df_okex_basic_currency[['basic_currency','symbol']].value_counts().index)
    # exit()
    for i in df_okex_basic_currency['basic_currency'].value_counts().index:
        # basic_str_lenth = len(i)
        # 若在基准币中已有的原数据的symbol，则跳过进行下一循环
        if any(df_okex_currency[df_okex_currency['symbol'].str.startswith(i)]['symbol'].isin(df_okex_basic_deal['symbol'].value_counts().index)):
            # print(i)
            continue
        else:
            # print(df_okex_basic_deal['symbol'].value_counts().index)
            df_okex_basic_deal = df_okex_basic_deal.append(df_okex_currency[df_okex_currency['symbol'].str.startswith(i)])
        # 将上一个基准币从原数据中删除
        # df_okex_currency.drop(df_okex_currency[df_okex_currency['symbol'].str.startswith(i)].index,inplace=True)
    df_okex_basic_deal['symbol'] = df_okex_basic_deal['symbol'].str.upper()
    df_okex_basic_deal.index.rename('candle_begin_time',inplace=True)
    return df_okex_basic_deal

# df_okex_basic_deal = filter_basic_coin(df_okex_basic_currency,df_okex_currency)
# print(df_okex_basic_deal)
# exit()

# okex成交量计算
# def okex_everday_total_volume(df_okex_currency):
#     '''
#
#     :param df_okex_currency: okex交易所原始数据
#     :return: okex交易所每日以usdt表示的总成交量
#     '''
#     usdt_list = list()
#     for i in df_okex_currency['symbol'].value_counts().index:
#         if i.endswith('USDT'):
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

# huobipro成交量计算
def huobipro_everday_total_volume(df_huobipro_currency, df_binance_currency):
    '''

    :param df_huobipro_currency:
    :return:
    '''
    usdt_list = list()
    for i in df_huobipro_currency['symbol'].value_counts().index:
        if i.endswith('USDT'):
            usdt_list.append(i) # usdt_list是huobipro交易所所有后缀为usdt的币种

    df_binance_currency_usdt = df_binance_currency.loc[df_binance_currency['symbol'].isin(usdt_list)]
    # 求每天的汇兑中间价
    df_binance_currency_usdt['middle_rate'] = (df_binance_currency_usdt.loc[:,'high'] + df_binance_currency_usdt.loc[:,'low'])/2
    df_binance_currency_usdt.reset_index(inplace=True)
    df_binance_currency_usdt.rename(columns = {'symbol':'exchange_symbol'},inplace=True)
    df_binance_currency_usdt = df_binance_currency_usdt[['candle_begin_time','exchange_symbol','middle_rate']]
    df_huobipro_currency.reset_index(inplace=True)
    df_total_coin_temp = pd.DataFrame()
    for i in df_huobipro_currency['symbol'].value_counts().index:
        if not i.endswith('USDT'):
            df_everycoin_temp = df_huobipro_currency.loc[df_huobipro_currency['symbol']==i]
            df_everycoin_temp['temp_symbol'] = np.array(df_everycoin_temp['symbol']) + np.array(['USDT'] * len(df_everycoin_temp))
        else:
            df_everycoin_temp['temp_symbol'] = df_huobipro_currency['symbol'].copy()
        for ii in df_binance_currency_usdt['exchange_symbol'].value_counts().index:
            for iii in df_everycoin_temp['temp_symbol'].value_counts().index:
                if ii in iii:
                    df_everycoin_temp['exchange_symbol'] = np.array([ii] * len(df_everycoin_temp))
        df_total_coin_temp = df_total_coin_temp.append(df_everycoin_temp)

    df_huobipro_currency_middle_rate = pd.merge(left=df_total_coin_temp,right=df_binance_currency_usdt,on=['candle_begin_time','exchange_symbol']
                           ,how='inner',sort=False)
    df_huobipro_currency_middle_rate['exchange_volume'] = df_huobipro_currency_middle_rate['middle_rate']*df_huobipro_currency_middle_rate['volume']
    grouped_symbol_huobipro = df_huobipro_currency_middle_rate.groupby(by='candle_begin_time')
    huobipro_everday_total_volume_temp = grouped_symbol_huobipro['exchange_volume'].sum()
    huobipro_everday_total_volume = huobipro_everday_total_volume_temp.to_frame()
    huobipro_everday_total_volume.rename(columns={ 'exchange_volume':'huobipro_total_volume'},inplace=True)
    return huobipro_everday_total_volume

# okex基准货币日成交额
df_okex_basic_deal = filter_basic_coin(df_okex_basic_currency,df_okex_currency)
df_okex_basic_deal_total_volume = huobipro_everday_total_volume(df_okex_basic_deal,df_okex_basic_deal)
df_okex_basic_deal_total_volume.rename(columns = {'huobipro_total_volume':'okex_total_volume'},inplace=True)

# binance基准币日成交额
df_binance_basic_deal = filter_basic_coin(df_binance_basic_currency,df_binance_currency)
df_binance_basic_deal_total_volume = huobipro_everday_total_volume(df_binance_basic_deal,df_binance_basic_deal)
df_binance_basic_deal_total_volume.rename(columns = {'huobipro_total_volume':'binance_total_volume'},inplace=True)

# huobipro基准币日成交额
df_huobipro_basic_deal = filter_basic_coin(df_huobipro_basic_currency,df_huobipro_currency)
df_huobipro_basic_deal_total_volume = huobipro_everday_total_volume(df_huobipro_basic_deal,df_huobipro_basic_deal)

# 合并三个交易所数据
df_exchange_basic_deal_total_volume_temp = pd.merge(df_okex_basic_deal_total_volume,df_binance_basic_deal_total_volume
                                                    ,left_index=True,right_index=True,how='outer')
df_exchange_basic_deal_total_volume = pd.merge(df_exchange_basic_deal_total_volume_temp,df_huobipro_basic_deal_total_volume,
                                               left_index=True,right_index=True,how='outer')
# 导出数据
df_exchange_basic_deal_total_volume.to_csv('E://pyseven//digital_currency_project//data//df_exchange_basic_deal_total_volume0405.csv')


#
# # 导入三家交易所的数据
# df_okex_currency = pd.read_csv('E:\pyseven\digital_currency_project\data\changed_okex_day_data.csv',parse_dates=True,index_col='candle_begin_time')
# df_binance_currency =pd.read_csv('E:/pyseven/digital_currency_project/data/binance_day_data.csv',parse_dates=True,index_col='candle_begin_time')
# df_huobipro_currency = pd.read_csv('E:\pyseven\digital_currency_project\data\huobipro_day_data.csv',parse_dates=True,index_col='candle_begin_time')
#
# # 将symbol列变为大写
# df_okex_currency['symbol'] = df_okex_currency['symbol'].str.upper()
# df_huobipro_currency['symbol'] = df_huobipro_currency['symbol'].str.upper()
#
# # ============================三大交易所每天的成交量对比============================
# # huobipro成交量计算
# def huobipro_everday_total_volume(df_huobipro_currency, df_binance_currency):
#     '''
#
#     :param df_huobipro_currency:
#     :return:
#     '''
#     usdt_list = list()
#     for i in df_huobipro_currency['symbol'].value_counts().index:
#         if i.endswith('USDT'):
#             usdt_list.append(i) # usdt_list是huobipro交易所所有后缀为usdt的币种
#
#     df_binance_currency_usdt = df_binance_currency.loc[df_binance_currency['symbol'].isin(usdt_list)]
#     # 求每天的汇兑中间价
#     df_binance_currency_usdt['middle_rate'] = (df_binance_currency_usdt.loc[:,'high'] + df_binance_currency_usdt.loc[:,'low'])/2
#     df_binance_currency_usdt.reset_index(inplace=True)
#     df_binance_currency_usdt.rename(columns = {'symbol':'exchange_symbol'},inplace=True)
#     df_binance_currency_usdt = df_binance_currency_usdt[['candle_begin_time','exchange_symbol','middle_rate']]
#     df_huobipro_currency.reset_index(inplace=True)
#     df_total_coin_temp = pd.DataFrame()
#     for i in df_huobipro_currency['symbol'].value_counts().index:
#         if not i.endswith('USDT'):
#             df_everycoin_temp = df_huobipro_currency.loc[df_huobipro_currency['symbol']==i]
#             df_everycoin_temp['temp_symbol'] = np.array(df_everycoin_temp['symbol']) + np.array(['USDT'] * len(df_everycoin_temp))
#         else:
#             df_everycoin_temp['temp_symbol'] = df_huobipro_currency['symbol'].copy()
#         for ii in df_binance_currency_usdt['exchange_symbol'].value_counts().index:
#             for iii in df_everycoin_temp['temp_symbol'].value_counts().index:
#                 if ii in iii:
#                     df_everycoin_temp['exchange_symbol'] = np.array([ii] * len(df_everycoin_temp))
#         df_total_coin_temp = df_total_coin_temp.append(df_everycoin_temp)
#
#     df_huobipro_currency_middle_rate = pd.merge(left=df_total_coin_temp,right=df_binance_currency_usdt,on=['candle_begin_time','exchange_symbol']
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
#             for iii in df_everycoin_temp['temp_symbol'].value_counts().index:
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
# #
#
# # 将三个交易所每日成交量合并
# total_everday_return_temp = pd.merge(huobipro_everday_total_volume(df_okex_currency,df_binance_currency), binance_everday_total_volume(df_binance_currency),left_index=True,right_index=True,how='outer')
# total_everday_return = pd.merge(total_everday_return_temp,huobipro_everday_total_volume(df_huobipro_currency,df_binance_currency), left_index=True, right_index=True,how='outer')
# total_everday_return.to_csv('E://pyseven//digital_currency_project//data//base_on_binance_everyday7777777.csv')

