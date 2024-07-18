# 导入所需的库
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt

# 设置一个标题
st.title('六七月数据报表')
#@st.cache
all_data = pd.read_csv('data/非标六七月汇总.csv')
df = pd.DataFrame(all_data)
df = df.drop('偷子', axis=1) #由于偷子列暂时没有数据，所以先删除掉

df.head(20)
#填充日期，用上一行的数据
df.isna()
df = df.fillna(method='pad')
df = df.drop('ROI', axis=1)
df = df.drop('结算cac', axis=1)
df = df.drop(df.index[[13, 77]])  # 把两行没有接量的私域行删除了

df = df.reset_index(drop=True)# 索引重排
# 显示数据表
st.write("全部数据：")
st.dataframe(df)

#根据不同的渠道做不同的表

dataframes_hua = {}
dataframes_TMK = {}
dataframes_SDK = {}
dataframes_si = {}

for i in range(0, 96):
    if df['渠道'][i] == '花骡直播':
        a = len(dataframes_hua)
        dataframes_hua[a] = df.loc[i]
    if df['渠道'][i] == 'TMK短信':
        b = len(dataframes_TMK)
        dataframes_TMK[b] = df.loc[i]
    if df['渠道'][i] == 'SDK聚合':
        c = len(dataframes_SDK)
        dataframes_SDK[c] = df.loc[i]
    if df['渠道'][i] == '私域':
        d = len(dataframes_si)
        dataframes_si[d] = df.loc[i]

dataframes_hua = pd.DataFrame(dataframes_hua)
dataframes_hua = dataframes_hua.transpose() # 转置
st.write("花骡直播：")
st.dataframe(dataframes_hua)

dataframes_TMK = pd.DataFrame(dataframes_TMK)
dataframes_TMK = dataframes_TMK.transpose() # 转置
st.write("TMK短信：")
st.dataframe(dataframes_TMK)

dataframes_SDK = pd.DataFrame(dataframes_SDK)
dataframes_SDK = dataframes_SDK.transpose() # 转置
st.write("SDK聚合：")
st.dataframe(dataframes_SDK)

dataframes_si = pd.DataFrame(dataframes_si)
dataframes_si = dataframes_si.transpose() # 转置
st.write("私域：")
st.dataframe(dataframes_si)

# 设置侧边栏     Tips:所有侧边栏的元素都必须在前面加上 sidebar，不然会在主页显示
st.sidebar.expander('')  # expander必须接受一个 label参数，我这里留了一个空白
st.sidebar.subheader('在下方选择调节你的参数')  # 副标题
# st.selectbox:创造一个下拉选择框的单选题，接收参数: (题目名称， 题目选项)
channel = st.sidebar.selectbox('1.选择渠道:', ['花骡直播', 'TMK短信', 'SDK聚合', '私域',])
columns = st.sidebar.radio('2.选择要查看的影响因素:', ['全部客户', '加微率', '导学课到课率', '导学课完课率', '正价转化率'])


#selected_channel = st.selectbox('选择渠道', channel, key=1)
#selected_column = st.selectbox('选择Y轴指标', columns, key=2)
#st.set_option('deprecation.showPyplotGlobalUse', False) #

def plot_chart(data, column):
    data.set_index('日期', inplace=True)  # 设置日期为索引
    plt.figure(figsize=(10, 6))
    for h5id in data['H5id'].unique():
        plt.plot(data[data['H5id'] == h5id].index,
                 data[data['H5id'] == h5id][column], label=h5id)
    plt.rcParams["font.family"] = ["sans-serif"]
    plt.rcParams["font.sans-serif"] = ['SimHei']
    plt.title(f'{column}')
    plt.xlabel('日期')
    plt.ylabel(column)
    plt.legend()  # 显示图例
    plt.grid(True)  # 显示网格
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot()  # 使用Streamlit显示matplotlib图表

# 根据用户选择绘制图表
if channel == '花骡直播':
    st.title('花骡直播')
    plot_chart(dataframes_hua, columns)
if channel == 'TMK短信':
    st.title('TMK短信')
    plot_chart(dataframes_TMK, columns)
if channel == 'SDK聚合':
    st.title('SDK聚合')
    plot_chart(dataframes_SDK, columns)
if channel == '私域':
    st.title('私域')
    plot_chart(dataframes_si, columns)

# 添加滑块，后期可以选择日期
from datetime import datetime
start_time = st.slider(
     "请选择开始时间",
     value=datetime(2024, 1, 1, 9, 30),
     format="MM/DD/YY - hh:mm")
st.write("开始时间:", start_time)

