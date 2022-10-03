import pandas as pd

# 读取股票数据
stock_data = pd.read_csv("./data/SHY.csv",
                         parse_dates=['Date'],  # 将Date列解析为时间格式
                         index_col=['Date']  # 设置Date列为索引
                         ).dropna()  # 丢弃包含缺失值的行

# 读取标普500数据
benchmark_data = pd.read_csv("./data/SPY.csv",
                             parse_dates=['Date'],
                             index_col=['Date']
                             ).dropna()
print(stock_data.head())
print(benchmark_data.head())
data1 = pd.merge(stock_data, benchmark_data,on='Date')
data1.to_csv("./data/SHY_SPY.csv")
print(data1.head())
