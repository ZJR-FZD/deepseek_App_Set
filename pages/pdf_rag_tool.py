import streamlit as st
from utils_pdf_rag_tool import rag_tool
from langchain.memory import ConversationBufferMemory

st.title("智能PDF问答工具")

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
    uploaded_file = st.file_uploader("请上传你的PDF文件：", type="pdf")

# 初始化会话状态
if "memory_rag" not in st.session_state:
    st.session_state.memory_rag = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )
    st.session_state.messages_rag = [
        {
            "role": "ai",
            "content": "你好，我是PDF分析小助手，上传文件向我提问吧！"
        }
    ]
    st.session_state.documents = []

# 显示历史对话消息（初始显示）和历史资料
num = 0
for message in st.session_state.messages_rag:
    st.chat_message(message["role"]).write(message["content"])
    if message["role"] == "ai":
        if message["content"] != "你好，我是PDF分析小助手，上传文件向我提问吧！":  # 注意超范围问题，第一句ai消息没有相应的相关资料
            with st.expander("相关资料"):
                st.write(st.session_state.documents[num][0].page_content)
            num += 1

# 获取用户输入
question = st.chat_input("对PDF的内容进行提问")
if question:
    if not st.session_state.api_key:
        st.info("请输入你的Deepseek API密钥")
        st.stop()
    if not uploaded_file:
        st.info("请先上传文件！")
        st.stop()

    # 合法后就显示
    st.session_state.messages_rag.append(
        {"role": "human", "content": question}
    )
    st.chat_message("human").write(question)

    # 获取AI的回复
    with st.spinner("AI正在思考中，请稍等···"):
        result = rag_tool(api_key=st.session_state.api_key, memory=st.session_state.memory_rag,
                          uploaded_file=uploaded_file, question=question)

    answer = result["answer"]
    st.session_state.messages_rag.append(
        {"role": "ai", "content": answer}
    )
    st.chat_message("ai").write(answer)

    relavant_docs = result["source_documents"]
    st.session_state.documents.append(relavant_docs)
    with st.expander("相关资料"):
        st.write(relavant_docs[0].page_content)