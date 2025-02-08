import requests
import os
from langchain.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek

# 自定义百度百科API包装器
class BaiduBaikeAPIWrapper:
    def __init__(self, user_id="10002402", api_key="f136bce1d05404ca8339d153ab5ed161"):
        # 初始化用户ID和API密钥
        self.user_id = user_id
        self.api_key = api_key

    def run(self, subject):
        # 百度百科搜索API的URL
        url = "https://cn.apihz.cn/api/zici/baikebaidu.php"
        # 请求参数
        params = {
            "id": self.user_id,  # 用户ID
            "key": self.api_key,  # API密钥
            "words": subject  # 要查询的内容
        }
        try:
            # 发送GET请求
            response = requests.get(url, params=params)
            # 检查响应状态码
            response.raise_for_status()
            # 解析返回的JSON数据
            result = response.json()
            if result["code"] == 200:
                return result["msg"]
            else:
                return f"错误信息：{result['msg']}"
        except requests.RequestException as e:
            # 打印错误信息
            print(f"请求百度百科API时出错: {e}")
            return "请求出错"

# 根据主题和时长，规定创造性，获得视频的标题和脚本
def generate_script(subject, video_length, creativity, api_key):
    try:
        # 初始化模型
        model = ChatDeepSeek(model="deepseek-chat", api_key=api_key,
                             temperature=creativity)

        # 获得视频的标题
        title_template = ChatPromptTemplate.from_messages(
            [
                ("human", "请为主题为‘{subject}’的视频起一个吸引人且独特的标题，只需一个标题")
            ]
        )
        title = (title_template | model).invoke(
            {
                "subject": subject
            }
        ).content

        # 调用百度百科的API获得相关信息
        search = BaiduBaikeAPIWrapper()
        search_result = search.run(subject)

        # 获得视频的脚本内容
        script_template = ChatPromptTemplate.from_messages(
            [
                ("human",
                 f"""你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
                 视频标题：{title}，视频时长：{video_length}分钟，人的正常语速约为每分钟200字，
                 所以生成的脚本长度必须在{video_length * 200 - 20}到{video_length * 200 + 20}字之间。
                 要求开头抓住眼球，中间提供干货内容，结尾有惊喜，脚本格式请按照【开头、中间，结尾】分隔。
                 整体内容的表达方式要尽量轻松有趣，吸引年轻人。
                 脚本内容可以结合以下百度百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
                 ```{search_result}```
                 注意：脚本长度不应该包括百度百科内容的字数。
                  """)
            ]
        )

        script = (script_template | model).invoke(
            {
                "title": title,
                "duration": video_length,
                "baidu_search": search_result,
                "min_length": video_length * 200 - 20,
                "max_length": video_length * 200 + 20
            }
        ).content

        return search_result, title, script
    except Exception as e:
        print(f"生成脚本时出错: {e}")
        return None, None, None

# 示例调用
# print(generate_script("deepseek大模型", 0.5, 0.7, os.getenv("OPENAI_API_KEY")))