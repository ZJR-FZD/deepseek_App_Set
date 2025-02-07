from langchain.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_community.utilities import WikipediaAPIWrapper
import os

# 根据主题和时长，规定创造性，获得视频的标题和脚本
def generate_script(subject, video_length, creativity, api_key):
    model = ChatDeepSeek(model="deepseek-chat",api_key=api_key,
                       temperature=creativity)  # 初始化模型

    # 获得视频的标题
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为主题为‘{subject}’的视频起一个吸引人的标题")
        ]
    )  # 定义提示模板
    title = (title_template | model).invoke(
        {
            "subject": subject
        }
    ).content  # 调用链的invoke，获得最终结果

    # 调用维基百科的API获得相关信息
    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    # 获得视频的脚本内容
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，人的正常语速约为每分钟 200 字，所以生成的脚本长度必须在 {min_length} 到 {max_length} 字之间。
             要求开头抓住眼球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```
             注意：脚本长度不应该包括维基百科内容的字数。
              """)
        ]
    )

    # 计算最小和最大长度
    min_length = video_length * 200 - 20
    max_length = video_length * 200 + 20

    script = (script_template | model).invoke(
        {
            "title": title,
            "duration": video_length,
            "wikipedia_search": search_result,
            "min_length": min_length,
            "max_length": max_length
        }
    ).content

    return search_result, title, script

# 示例调用
# print(generate_script("deepseek大模型", 0.5, 0.7, os.getenv("OPENAI_API_KEY")))