import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option("display.max_rows", 500)  # 设定显示最大的行数

# df = pd.read_csv('E:/pyseven/digital_currency_project/data/okex_day_data.csv', parse_dates=['candle_begin_time'])
# df = df.loc[df['candle_begin_time']=='2017-12-28']
#
# print(df.sort_values(['high','close']))
#
# exit()
# =====导入数据
all_data = pd.DataFrame()
for exchange in ['okex', 'binance', 'huobipro']:
    print(exchange)
    # 读取数据
    df = pd.read_csv('E:/pyseven/digital_currency_project/data/' + exchange + '_day_data.csv', parse_dates=['candle_begin_time'])
    # 排序
    df.sort_values(by=['symbol', 'candle_begin_time'], inplace=True)
    df.reset_index(inplace=True, drop=True)

    # 整理symbol
    df['symbol'] = df['symbol'].str.upper()
    df['symbol'] = df['symbol'].str.replace('_', '')

    # 找出base coin，例如btc/usdt交易对中，usdt是base coin
    df.loc[df['symbol'].str[-4:] == 'USDT', 'base_coin'] = 'USDT'
    df['base_coin'].fillna(value=df['symbol'].str[-3:], inplace=True)

    # trade coin，例如btc/usdt交易对中，btc是trade coin
    df.loc[df['symbol'].str[-4:] == 'USDT', 'trade_coin'] = df['symbol'].str[:-4]
    df['trade_coin'].fillna(value=df['symbol'].str[:-3], inplace=True)

    # 删除volume为0的日期。有的币上市之后，成交量为0，删除。
    df = df[df['volume'] > 0]

    # 将每个交易对上市第一天删除
    df = df.groupby('symbol').apply(lambda group: group.iloc[1:])
    df.reset_index(inplace=True, drop=True)

    # 对于没有quote_volume的数据，估算quote_volume。okex交易所没有quate_volume
    # quate_volume的含义距离：btc/usdt交易对中，volume指的是成交了多少个btc，quate_volume指的是成交量多少个usdt
    if 'quote_volume' not in df.columns:
        print(exchange)
        df['quote_volume'] = df['volume'] * (df['open'] + df['close']) / 2  # 使用最高和最低价的中间价估算。

    # 选取列
    df = df[['exchange', 'symbol', 'trade_coin', 'base_coin', 'candle_begin_time', 'open','close', 'volume', 'quote_volume']]

    # 合并数据
    all_data = all_data.append(df, ignore_index=True)

# =====找出基准价格
# 找出基准货币的类型，也就是base_coin的类型
base_coin_list = list(all_data['base_coin'].drop_duplicates())
base_coin_list.remove('USDT')

# 找出基准货币每天相当于与usdt的价格，使用几家交易所收盘价的均值
df = all_data[(all_data['trade_coin'].isin(base_coin_list)) & (all_data['base_coin'] == 'USDT')]
base_coin_price = df.groupby(['trade_coin', 'candle_begin_time'])[['close']].mean()  # 几家交易所收盘价的均值
base_coin_price.reset_index(inplace=True)
base_coin_price.rename(columns={'close': 'price', 'trade_coin': 'base_coin'}, inplace=True)

# 计算每个货币相对于usdt的成交量，例如对于eos/btc交易对，使用这个交易对的quote_volume * 当天btc的usdt价格
all_data = pd.merge(left=all_data, right=base_coin_price, left_on=['base_coin', 'candle_begin_time'],
                    right_on=['base_coin', 'candle_begin_time'], how='left')
all_data.loc[all_data['base_coin'] == 'USDT', 'price'] = 1
all_data = all_data[all_data['price'].notnull()]
all_data.reset_index(inplace=True, drop=True)
all_data['base_coin_volume'] = all_data['quote_volume'] * all_data['price']

'''
# =====计算每天交易币种的数量，eth/btc、eth/usdt，这两个交易对算1个交易币种
rtn = pd.DataFrame()
for exchange, group in all_data.groupby('exchange'):
    group = group.drop_duplicates(subset=['candle_begin_time', 'trade_coin'])
    rtn[exchange] = group.groupby(['candle_begin_time']).size()
print('每天交易币种的数量\n', rtn)
rtn.to_csv('每天交易币种的数量.csv')


# =====计算每天交易对的数量，eth/btc、eth/usdt，算2个交易对
rtn = pd.DataFrame()
for exchange, group in all_data.groupby('exchange'):
    group = group.drop_duplicates(subset=['candle_begin_time', 'symbol'])
    rtn[exchange] = group.groupby(['candle_begin_time']).size()
print('每天交易对的数量\n', rtn)
rtn.to_csv('每天交易对的数量.csv')


# =====计算每天每个交易所所有品种交易量
rtn = pd.DataFrame()
for exchange, group in all_data.groupby('exchange'):
    rtn[exchange] = group.groupby(['candle_begin_time'])['base_coin_volume'].sum()
print('所有币种交易量\n', rtn)
rtn.to_csv('所有币种交易量.csv')


# =====计算主流币种交易量
trade_coin_list = ['BTC', 'ETH', 'LTC', 'XRP', 'EOS']
df = all_data[all_data['trade_coin'].isin(trade_coin_list)]
rtn = pd.DataFrame()
for exchange, group in df.groupby('exchange'):
    rtn[exchange] = group.groupby(['candle_begin_time'])['base_coin_volume'].sum()
print('主流币种交易量\n', rtn)
# rtn.to_csv('主流币种交易量.csv')
'''


# 计算主流币的流动性指标Lt=Vt/|lnPt-lnPt-1| 当天的交易额除上当天对数收益率的绝对值
trade_coin_list = ['BTC', 'ETH', 'LTC', 'XRP', 'EOS']
df = all_data[all_data['trade_coin'].isin(trade_coin_list)]
rtn = pd.DataFrame()
for exchange, group in df.groupby('exchange'):
    group['illiquidity'] = group['base_coin_volume']/(np.abs(np.log(group['close']/group['open'])))
    
    # rtn[exchange] = group.groupby(['candle_begin_time'])['base_coin_volume']

print('主流币种交易量\n', group)

# 动量指标 = (当前收盘的牌价 / 前几个时段收盘的牌价) x 100

'''
# 主流货币成交量占总成交量的比例
trade_coin_list = ['BTC', 'ETH', 'LTC', 'XRP', 'EOS']
df = all_data[all_data['trade_coin'].isin(trade_coin_list)]
rtn = pd.DataFrame()
for exchange, group in df.groupby('exchange'):
    rtn[exchange] = group.groupby(['candle_begin_time'])['base_coin_volume'].sum()

rtn_1 = pd.DataFrame()
for exchange, group in all_data.groupby('exchange'):
    rtn_1[exchange] = group.groupby(['candle_begin_time'])['base_coin_volume'].sum()
rtn_1.rename(columns = {'binance':'binance_total_volume','huobipro':'huobipor_total_volume','okex':'okex_total_volume'},inplace=True)
rtn_temp = pd.merge(rtn,rtn_1,left_index=True,right_index=True)
rtn_temp['binance主流币/总成交'] = rtn_temp['binance']/rtn_temp['binance_total_volume']
rtn_temp['huobipro主流币/总成交'] = rtn_temp['huobipro']/rtn_temp['huobipor_total_volume']
rtn_temp['okex主流币/总成交'] = rtn_temp['okex']/rtn_temp['okex_total_volume']
# rtn_temp.to_csv('主流币成交量占总成交量比率.csv',encoding='gbk') # 导出主流币成交量占总成交量比率


# 每个交易所上的币的破发率
df_temp = pd.DataFrame()
df_initial_break = pd.DataFrame()
for exchange,group in all_data.groupby('exchange'):
    df_temp = group.groupby('symbol').agg({'open':'first','close':'last'})
    df_temp.loc[df_temp['open'] > df_temp['close'],'是否为破发'] = 1
    df_temp.fillna(value=0 , inplace=True)
    initial_break_ratio = len(df_temp[df_temp['是否为破发']==1])/len(df_temp)
    print(exchange+'破发率为：',initial_break_ratio)
'''

# 每个交易所上的币的每日平均涨幅
df_everyday_change = pd.DataFrame()
df_deposit_curve = pd.DataFrame()
for exchange,group in all_data.groupby('exchange'):
    group['每日涨跌幅'] = group['close']/group['open']-1.0
    df_everyday_change[exchange] = group.groupby('candle_begin_time')['每日涨跌幅'].mean()
    df_deposit_curve[exchange] = (df_everyday_change[exchange] + 1.0).cumprod()

df_everyday_change.to_csv('交易所每日上市币平均涨跌幅.csv')
df_deposit_curve.to_csv('交易所资金曲线')




# print(df_initial_break)
# exit()
# print('主流币种交易量\n', all_data)