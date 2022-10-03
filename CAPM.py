import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

spy = pd.read_csv("./data/000001.SS.csv",
                         parse_dates=['Date'],  # 将Date列解析为时间格式
                         index_col=['Date']  # 设置Date列为索引
                         ).dropna()  # 丢弃包含缺失值的行

Rf_annual=0.0385#以2017年中国一年期的国债利率为无风险利率
Rf_daily=(1+Rf_annual)**(1/365)-1##年利率转化为日利率

Rm = np.log(spy['SSE']/spy['SSE'].shift(1))
Rm = Rm.dropna()
print(Rm.describe())

Haier = pd.read_csv("./data/Haie_CAPM.csv",
                         parse_dates=['Date'],  # 将Date列解析为时间格式
                         index_col=['Date']  # 设置Date列为索引
                         ).dropna()  # 丢弃包含缺失值的行

Ri_Haier = np.log(Haier['Haier']/Haier['Haier'].shift(1))
Ri_Haier = Ri_Haier.dropna()
print(Ri_Haier.describe())

plt.scatter(Ri_Haier,Rm)
plt.savefig('./result/CAPM/海尔与大盘风险溢价的散点图.png', dpi=450)
plt.show()

Rm_add = sm.add_constant(Rm)   # 增加常数列
model_shjc = sm.OLS(endog=Ri_Haier,exog=Rm_add)
result_shjc = model_shjc.fit()  # 拟合
print(result_shjc.summary())
print(result_shjc.params)