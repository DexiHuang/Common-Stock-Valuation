import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew


def first_part():

    # 读取csv文件，并将‘Date’列解析为日期时间格式,并设为索引
    StockPrices = pd.read_csv('./data/SPY.csv', parse_dates=['Date'], index_col='Date')

    # 将数据按日期这一列排序（保证后续计算收益率的正确性）
    StockPrices = StockPrices.sort_values(by='Date')

    # 打印数据的前5行
    print(StockPrices.head())

    # 增加一列'Returns', 存储每日的收益率
    StockPrices['Returns'] = StockPrices['SPY'].pct_change()
    clean_returns = StockPrices['Returns'].dropna()

    # 绘图
    plt.figure(figsize=(16, 5), dpi=450)
    plt.plot(clean_returns,color='darkorange')
    plt.savefig('./result/risk and return analysis/SPY日收益率的时间序列图.png', dpi=450)
    plt.show()

    mean_return_daily = np.mean(clean_returns)
    print("日平均收益：", mean_return_daily)
    mean_return_annualized = ((1 + mean_return_daily) ** 252) - 1
    print("平均年化收益：", mean_return_annualized)
    plt.hist(clean_returns, bins=75)
    plt.show()

    # 计算标准差
    sigma_daily = np.std(clean_returns)
    print("标准差: ", sigma_daily)

    # 计算方差
    variance_daily = sigma_daily ** 2
    print("方差: ", variance_daily)

    # 计算年化标准差
    sigma_annualized = sigma_daily * np.sqrt(252)
    print("年化标准差：", sigma_annualized)

    # 计算年化方差
    variance_annualized = sigma_annualized ** 2
    print("年化方差：", variance_annualized)

    returns_skewness = skew(clean_returns)
    print("偏度：", returns_skewness)


def second_part():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取股票数据
    stock_data = pd.read_csv("./data/HaierR.csv",
                             parse_dates=['Date'],  # 将Date列解析为时间格式
                             index_col=['Date']  # 设置Date列为索引
                             ).dropna()  # 丢弃包含缺失值的行

    # 读取标普500数据
    benchmark_data = pd.read_csv("./data/SHYY.csv",
                                 parse_dates=['Date'],
                                 index_col=['Date']
                                 ).dropna()
    plt.figure(figsize=(16, 5), dpi=450)
    stock_data.plot(subplots=True)
    #plt.savefig('./result/risk and return analysis/股票数据.png', dpi=450)
    plt.show()

    # 计算每日股票回报率
    stock_returns = stock_data.pct_change()
    plt.figure(figsize=(16, 5), dpi=450)
    plt.plot(stock_returns)
    #plt.savefig('./result/risk and return analysis/Haier和SPY日收益率的时间序列图.png', dpi=450)
    plt.show()

    # 计算标普500指数回报率
    sp_returns = benchmark_data['SHY'].pct_change()
    sp_returns.plot()
    plt.show()

    # 每日超额回报
    excess_returns = stock_returns.sub(sp_returns, axis=0)  # 做减法
    plt.figure(figsize=(16, 5), dpi=450)
    plt.plot(excess_returns)
    # plt.savefig('./result/risk and return analysis/Haier每日超额回报.png', dpi=450)
    plt.show()

    avg_excess_return = excess_returns.mean()
    print('超额回报的均值:', avg_excess_return)
    _ = avg_excess_return.plot.bar(title='超额回报的均值')
    plt.show()

    # 计算标准差
    sd_excess_return = excess_returns.std()
    print('超额回报标准差',sd_excess_return)
    # 日夏普比率（.div 做除法）
    daily_sharpe_ratio = avg_excess_return.div(sd_excess_return)

    # 年化夏普比率（.mul 做乘法）
    annual_factor = np.sqrt(252)
    annual_sharpe_ratio = daily_sharpe_ratio.mul(annual_factor)
    print("年化夏普比率", annual_sharpe_ratio)


second_part()
