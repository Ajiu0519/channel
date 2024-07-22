# 导入所需的库
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
#from vega_datasets import data


from matplotlib.font_manager import FontProperties  
font = FontProperties(fname='data/SimHei.ttf')  
plt.title('中文标题', fontproperties=font)  
#plt.font_manager.fontManager.addfont('data/SimHei.ttf') #临时注册新的全局字体
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False#用来正常显示负号
plt.plot([1, 2, 3], [4, 3, 2])    
plt.xlabel('x轴')  
plt.ylabel('y轴')  
st.pyplot(plt)


# 设置一个标题
st.title('六七月数据报表')

data = pd.read_csv("非标六七月汇总 (3).csv", encoding='utf-8')
df = pd.DataFrame(data)
df = df.drop('偷子', axis=1) #由于偷子列暂时没有数据，所以先删除掉

df.head(20)
#填充日期，用上一行的数据
df.isna()
df = df.fillna(method='pad')
df = df.drop('ROI', axis=1)
df = df.drop('结算cac', axis=1)
#df = df.drop(df.index[[13, 77]])  # 把两行没有接量的私域行删除了

#df = df.reset_index(drop=True)# 索引重排
# 显示数据表
st.write("全部数据：")
st.dataframe(df)

#根据不同的渠道做不同的表
st.set_option('deprecation.showPyplotGlobalUse', False)
dataframes_hua = {}
dataframes_TMK = {}
dataframes_SDK = {}
dataframes_si = {}

for i in range(0, len(df)):
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
st.sidebar.subheader('在下方选择')  # 副标题
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
    plt.rcParams["font.family"] = ["MICROSS"]
    plt.rcParams["font.sans-serif"] = ['SimHei']
    #plt.title(f'{column}')
    plt.xlabel('data')
    #plt.ylabel(column)
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

# 新建板块
st.sidebar.subheader('在下方选择板块')  # 副标题
# st.selectbox:创造一个下拉选择框的单选题，接收参数: (题目名称， 题目选项)
#channel = st.sidebar.selectbox('1.选择影响因素:', ['花骡直播', 'TMK短信', 'SDK聚合', '私域',])
selected_metric = st.sidebar.radio('1.选择要查看的影响因素:', ['全部客户', '加微率', '导学课到课率', '导学课完课率', '正价转化率'])

st.title('按渠道对比')
summary_df = df[df['H5id'] == '汇总']
if not summary_df.empty:
    plt.figure(figsize=(10, 6))
    if selected_metric == '全部客户':
        plt.ylim(0, 500)  # 确保y轴从0开始并包含整个数据范围
    if selected_metric == '加微率' or selected_metric == '导学课到课率' or selected_metric == '导学课完课率' or selected_metric == '正价转化率':
        plt.ylim(0, 1)
    for channel, channel_data in summary_df.groupby('渠道'):
        print(channel_data)
        plt.plot(channel_data['日期'], channel_data[selected_metric], label=channel, marker='o', linestyle='-')
    #plt.title(f'{selected_metric}')
    plt.rcParams["font.family"] = ["MICROSS"]
    plt.rcParams["font.sans-serif"] = ['SimHei']
    plt.xlabel('data')
    #plt.ylabel(f'{selected_metric}')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot()
else:
    st.write('没有找到汇总数据，请检查数据源。')


if selected_metric == '全部客户':
    st.markdown('整体趋势：  \n在六月到七月期间，全部客户数量呈现出一定的波动，各渠道对“全部客户”数量的影响程度不一，其中某些渠道可能表现更为突出或不足。  \n渠道表现：  \n'
             'SDK聚合：SDK聚合的折线相对较低或波动较小，表明该渠道在吸引客户方面的效果可能不如其他渠道显著,这可能与渠道特性、营销策略或市场环境等因素有关。  \n  \n'
             'TMK短信：TMK短信渠道的折线相对较高、增长趋势明显，表明该渠道在吸引客户方面表现较好，值得进一步关注和优化。  \n  \n'
             '私域：私域渠道的折线表现可能因具体策略而异，代表了一种长期维护和转化的客户关系方式。其效果可能不如其他渠道短期内显著，但对于客户忠诚度和复购率有重要影响。  \n  \n'
             '花骡直播：花骡直播渠道的表现可能因直播内容、主播影响力及观众互动情况等因素而异。如果折线波动较大，可能表明该渠道的效果受多种因素影响，需要精细化管理和运营。  \n  \n'
            )
if selected_metric == '加微率':
    st.markdown('整体趋势：  \n在六月到七月期间，加微率呈波动不明显， 其中“花骡直播”的总体加微情况要优于其他渠道，而且加微率较为稳定， \n私域的加微率总体较低，可能由于私域渠道由于其大多数客户都已经被锁定，导致新增较慢的情况。'
            )
if selected_metric == '导学课到课率':
    st.markdown('整体趋势：  \n在六月到七月期间，导学到课率除了“SDK聚合”以外其他渠道都较为稳定， 其中“花骡直播”的总体到课情况较好，“私域”的到课情况整体低于其他渠道'
            )
if selected_metric == '导学课完课率':
    st.markdown('整体趋势：  \n导学完课率除了“SDK聚合”以外其他渠道都较为稳定， 其中“花骡直播”和TMK短信的总体完课率总体情况较稳定，“私域”的完课情况较为稳定'
            )
if selected_metric == '正价转化率':
    st.markdown('整体趋势：  \n“花骡直播”的转化率较为突出，能稳定在1%以上，其他渠道转化率都有提高空间'
            )
