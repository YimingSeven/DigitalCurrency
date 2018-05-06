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
# 导入三家交易所的数据
df_okex_currency = pd.read_csv('E:\pyseven\digital_currency_project\data\changed_okex_day_data.csv',parse_dates=True,index_col='candle_begin_time')
df_binance_currency =pd.read_csv('E:/pyseven/digital_currency_project/data/binance_day_data.csv',parse_dates=True,index_col='candle_begin_time')
df_huobipro_currency = pd.read_csv('E:\pyseven\digital_currency_project\data\huobipro_day_data.csv',parse_dates=True,index_col='candle_begin_time')

df_okex_currency['symbol'] = df_okex_currency['symbol'].str.upper()
df_huobipro_currency['symbol'] = df_huobipro_currency['symbol'].str.upper()


def filter_data_dealed_num(df_okex_currency):
    '''

    :param df_okex_currency:
    :return:
    '''
    # 筛选两遍 第一遍筛选出usdt结尾的数据
    df_okex_currency_usdt_1 = df_okex_currency.loc[df_okex_currency['symbol'].str.endswith('USDT')]
    df_okex_currency_usdt_1['symbol_dealed'] = df_okex_currency_usdt_1['symbol'].str[:-4].copy()
    # 第二遍筛选
    df_okex_currency_usdt_2 = df_okex_currency.loc[~ df_okex_currency['symbol'].str.endswith('USDT')]
    df_okex_currency_usdt_2['symbol_dealed'] = df_okex_currency_usdt_2['symbol'].str[:-3].copy()
    # 将两次筛选的数据合并
    df_okex_currency_temp = df_okex_currency_usdt_1.append(df_okex_currency_usdt_2)
    df_okex_second_dealed_num = df_okex_currency_temp['symbol_dealed'].value_counts()
    df_okex_second_dealed_num = df_okex_second_dealed_num.to_frame()
    df_okex_second_dealed_num.reset_index(inplace=True)
    df_okex_second_dealed_num.rename(columns={'symbol_dealed': 'symbol_' + df_okex_currency['exchange'][0] + '_dealed',
                                              'index':df_okex_currency['exchange'][0]+'_public_coin'},inplace=True)
    return df_okex_second_dealed_num
symbol_okex_dealed = filter_data_dealed_num(df_okex_currency)
symbol_binance_dealed = filter_data_dealed_num(df_binance_currency)
symbol_huobipro_dealed = filter_data_dealed_num(df_huobipro_currency)
symbol_total_dealed_temp = symbol_okex_dealed.join(symbol_binance_dealed,how ='outer')
symbol_total_dealed = symbol_total_dealed_temp.join(symbol_huobipro_dealed,how = 'outer')

symbol_total_dealed.to_csv('E://pyseven//digital_currency_project//data//每个交易所已上市交易币数量.csv')
# print(symbol_total_dealed)
# exit()



