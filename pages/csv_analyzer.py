import streamlit as st
from utils_csv_analyzer import dataframe_agent
import pandas as pd
import os

def create_chart(input_data, chart_type):
    # 检查"data"字段是否存在且非空
    if "data" not in input_data or not input_data["data"]:
        st.error("没有提供有效的数据来创建图表")
        return
    
    data = input_data["data"]
    
    # 如果数据看起来像是一维的（即单列数据）
    if all(isinstance(i, (int, float)) for i in data):
        df = pd.DataFrame(data, columns=input_data["columns"])
    else:
        # 假设数据是二维的（多列数据）
        df = pd.DataFrame(data, columns=input_data["columns"])
    
    if chart_type == "line":
        st.line_chart(df)
    elif chart_type == "bar":
        st.bar_chart(df)
    # 可以添加更多图表类型的支持
    else:
        st.error(f"不支持的图表类型: {chart_type}")


st.title("CSV数据分析智能工具")

# 创建输入框，使用会话状态中的 api_key 作为默认值
with st.sidebar:
    input_api_key = st.text_input("请输入Deepseek API 密钥：", value=st.session_state.api_key, type="password")
    st.markdown("[获取Deepseek API 密钥](https://platform.deepseek.com/usage)")

# 如果输入框内容有变化，更新会话状态中的 api_key
if input_api_key != st.session_state.api_key:
    st.session_state.api_key = input_api_key
    st.success("API Key 已更新")

with st.sidebar:
    # 上传文件
    csv_file = st.file_uploader("请上传你的csv格式数据文件：", type="csv")

# 展示部分文件数据
if csv_file:
    df = pd.read_csv(csv_file)
    with st.expander("原始数据"):
        st.dataframe(df)

query = st.text_area("请输入你关于以上表格的问题，或数据提取请求，或可视化请求（支持散点图、折线图、条形图）：", disabled=not csv_file)

button = st.button("生成回答")

if button:
    if not st.session_state.api_key:
        st.info("请先输入Deepseek API密钥")
        st.stop()
    if not query:
        st.info("请输入您的问题")
        st.stop()
    
    with st.spinner("AI正在思考中，请稍等···"):
        result_dict = dataframe_agent(api_key=st.session_state.api_key, uploaded_file=csv_file, query=query)
        
        if "answer" in result_dict:
            st.write(result_dict["answer"])
        if "table" in result_dict:
            columns = result_dict["table"]["columns"]
            data = result_dict["table"]["data"]
            df_result = pd.DataFrame(data, columns=columns)
            st.table(df_result)
        if "bar" in result_dict:
            create_chart(result_dict["bar"], "bar")
        if "line" in result_dict:
            create_chart(result_dict["line"], "line")
        if "scatter" in result_dict:
            create_chart(result_dict["scatter"], "scatter")
                
 