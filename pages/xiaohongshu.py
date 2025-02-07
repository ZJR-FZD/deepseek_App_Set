# 网站页面

import streamlit as st
from utils_xiaohongshu import xiaohongshu_generator

st.title("🍠小红书爆款文案生成器")

# 创建输入框，使用会话状态中的 api_key 作为默认值
with st.sidebar:
    input_api_key = st.text_input("请输入Deepseek API 密钥：", value=st.session_state.api_key, type="password")
    st.markdown("[获取Deepseek API 密钥](https://platform.deepseek.com/usage)")

# 如果输入框内容有变化，更新会话状态中的 api_key
if input_api_key != st.session_state.api_key:
    st.session_state.api_key = input_api_key
    st.success("API Key 已更新")


subject = st.text_input("请输入主题：")
temperature = st.slider("请输入创造性（数字越小越严谨，数字越大越天马行空）：",
                        min_value=0.0,max_value=1.0,value=0.5,step=0.1)

submit = st.button("生成文案")
if submit and not st.session_state.api_key:
    st.info("请先输入Deepseek API密钥")
    st.stop()
if submit and not subject:
    st.info("请先输入文案的主题")
    st.stop()
if submit:
    with st.spinner("AI正在思考中，请稍等···"):
        result = xiaohongshu_generator(api_key=st.session_state.api_key,subject=subject,temperature=temperature)
    st.success("文案已生成")

    column1,column2 = st.columns(2)
    with column1:
        num = 0
        for title in result.titles:
            num += 1
            st.markdown(f"##### 标题{num}：")
            st.write(title)
    with column2:
        st.markdown("##### 小红书正文")
        st.write(result.content)
