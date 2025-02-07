from langchain_deepseek import ChatDeepSeek
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os

def get_chat_response(api_key,prompt,memory): # memory不能是函数的内部局部变量，否则会被清空

    llm = ChatDeepSeek(model="deepseek-chat",api_key=api_key)

    # 利用带记忆的对话链
    chain = ConversationChain(llm=llm,memory=memory)

    result = chain.invoke(
        {
            "input":prompt # 默认提示模板里需要填充input变量
        }
    ) #返回值是一个字典，包含了input、history、response
    return result["response"]

# memory = ConversationBufferMemory(return_messages=True) 记得创建记忆的实例
# print(get_chat_response(os.getenv("OPENAI_API_KEY"),"牛顿提出过那些知名的定律？",memory))
# print(get_chat_response(os.getenv("OPENAI_API_KEY"),"我上一个问题是什么？",memory))