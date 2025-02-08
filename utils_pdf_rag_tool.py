from langchain_community.document_loaders import PyPDFLoader
# 修正导入语句，正确的模块名是 langchain.text_splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_deepseek import ChatDeepSeek
from langchain.chains import ConversationalRetrievalChain
import os

def rag_tool(api_key, memory, uploaded_file, question):
    # 将文件内容写入到本地，才能有文件路径（用户上传的文件直接储存在内存里，无路径）
    file_content = uploaded_file.read()  # 返回文件的二进制数据
    print(type(file_content))
    temp_file_path = "temp.pdf"
    with open(temp_file_path, "wb") as fwb:  # 以二进制写入方式打开文件，并创建文件对象（与文件进行交互的接口）
        fwb.write(file_content)  # 写入上面读取到的文件内容

    try:
        # 加载
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()
        # 分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "！", "？", "，", "", "、", " ", ""]
        )
        texts = text_splitter.split_documents(docs)
        # 嵌入模型，使用 HuggingFaceEmbeddings 封装 SentenceTransformer
        embeddings_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        # 嵌入并储存
        db = FAISS.from_documents(texts, embeddings_model)
        # 检索
        retriever = db.as_retriever()

        # 模型
        model = ChatDeepSeek(model="deepseek-chat", api_key=api_key)

        # 创建带记忆的检索增强对话链（有了检索器、模型、记忆）
        chain = ConversationalRetrievalChain.from_llm(
            llm=model,
            retriever=retriever,
            memory=memory,
            return_source_documents=True
        )

        result = chain.invoke(
            {
                "chat_history": memory.load_memory_variables({})["chat_history"],
                "question": question
            }
        )
        return result
    finally:
        # 删除临时文件
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)