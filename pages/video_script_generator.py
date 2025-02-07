# 网站的主页
import streamlit as st
from utils_video import generate_script

st.title("视频脚本生成器")

if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
    
# 创建输入框，使用会话状态中的 api_key 作为默认值
with st.sidebar:
    input_api_key = st.text_input("请输入Deepseek API 密钥：", value=st.session_state.api_key, type="password")
    st.markdown("[获取Deepseek API 密钥](https://platform.deepseek.com/usage)")

# 如果输入框内容有变化，更新会话状态中的 api_key
if input_api_key != st.session_state.api_key:
    st.session_state.api_key = input_api_key
    st.success("API Key 已更新")

# 输入其他信息
subject = st.text_input("请输入视频的主题：")
video_length = st.number_input("请输入视频的大致时长（单位：分钟）",min_value=0.1,step=0.1)
creativity = st.slider("请输入视频脚本的创造力（数字越小越严谨，数字越大越天马行空）：",
                       min_value=0.0,max_value=1.0,value=0.5,step=0.1)

# 提交按钮（需要校验，点击提交按钮前输入了api密钥，并且输入了视频主题）
submit = st.button("生成脚本")
if submit and not st.session_state.api_key:
    st.info("请输入你的Deepseek API密钥")
    st.stop() #stop让后面的代码不再执行
if submit and not subject:
    st.info("请输入视频的主题")
    st.stop()
if submit:
    with st.spinner("AI正在思考中，请稍等···"): #“思考中”组件，只要缩进里的代码没有执行完，就一直有个加载的效果
        search_result,title,script = generate_script(subject,video_length,creativity,st.session_state.api_key)
    st.success("视频脚本已生成！")

    st.subheader("标题：")
    st.write(title)
    st.subheader("视频脚本：")
    st.write(script)
    with st.expander("维基百科搜索结果："): #折叠展开组件
        st.info(search_result)


