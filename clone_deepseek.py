import streamlit as st
from utils_clone import get_chat_response
from langchain.memory import ConversationBufferMemory

st.title("克隆Deepseek")

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

# 初始化会话状态（记忆和消息列表）
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)  
    st.session_state.messages = [
        {
            "role":"ai", "content":"你好，我是你的AI助手，有什么可以帮你的吗？"
        }
    ] #messages为了便于在前端页面上展示对话

# 显示历史对话消息（初始显示）
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 获取用户输入
prompt = st.chat_input()
if prompt:
    if not st.session_state.api_key:
        st.info("请输入你的Deepseek API密钥")
        st.stop()
    st.session_state.messages.append({"role":"human","content":prompt}) #将用户提问封装成消息对象，并添加进messages列表
    st.chat_message("human").write(prompt) # 在页面显示该消息内容

    # 获取AI回复
    with st.spinner("AI正在思考中，请稍等···"):
        response = get_chat_response(api_key=st.session_state.api_key,prompt=prompt,memory=st.session_state.memory)

    st.session_state.messages.append({"role":"ai","content":response}) #将AI的回复封装成消息对象，并添加进messages列表
    st.chat_message("ai").write(response) #在页面上显示该消息内容