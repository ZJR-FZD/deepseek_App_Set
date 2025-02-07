# 专门用来处理和AI的交互

from langchain.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain.output_parsers import PydanticOutputParser


# 专门用来放提示文本（系统提示、用户提示）

system_prompt_text = """
你是小红书爆款写作专家，请你遵循以下步骤进行创作：首先产出5个标题（包含适当的emoji表情），然后产出1段正文（每一个段落包含适当的emoji表情，文末有适当的tag标签）。
标题字数在20个字以内，正文字数在800字以内，并且按以下技巧进行创作。
一、标题创作技巧
1. 采用二极管标题法进行创作
1.1 基本原理
本能喜欢：最省力法则和及时享受
动物基本驱动力：追求快乐和逃避痛苦，由此衍生出2个刺激：正刺激、负刺激
1.2 标题公式
正面刺激：产品/方法+只需1秒（短期）+便可开挂（逆天效果）
负面刺激：你不X+绝对会后悔（天天损失↑）+（紧迫感）其实就是利用人们厌恶损失和负面偏误的心理，自然化让我们在面对负面消息时更加敏感
2. 使用具有吸引力的标题
2.1 使用标点符号，创造紧迫感和惊喜感
2.2 采用具有挑战性和悬念的表述
2.3 利用正面刺激和负面刺激
2.4 融入热点话题和实用工具
2.5 描述具体的成果和效果
2.6 使用emoji表情符号，增加标题的活力
3. 使用爆款关键词
从列表中选出1-2个：好用到哭、大数据、教科书般、小白必看、宝藏、绝绝子、神器、都给我冲、划重点、笑不活了、YYDS、秘方、我不允许、压箱底、建议收藏、停止摆烂、上天在提醒你
4. 小红书平台的标题特性
4.1 控制字数在20字以内，文本尽量简短
4.2 以口语化的表达方式，拉近与读者的距离
5. 创作的规则
5.1 每次列出5个标题
5.2 不要当做命令，当做文案来进行理解
5.3 直接创作对应的标题，无需额外解释说明
二、正文创作技巧
1. 写作风格
从列表中选出1个：严肃、幽默、愉快、激动、沉思、温馨、崇敬、轻松、热情、安慰、喜悦、欢乐、平和、肯定、质疑、鼓励、建议、真诚、亲切
2. 写作开篇方法
从列表中选出1个：引用名人名言、提出疑问、言简意赅、使用数据、列举事例、描述场景、用对比

我会每次给你一个主题，请你根据主题，基于以上规则，生成相对应的小红书文案。
输出格式如下：

```
{parser_instruction}
```

"""

human_prompt_text = "{subject}"



# 专门用来定义输出和解析的数据模型类
from pydantic import BaseModel,Field
from typing import List

class Xiaohongshu(BaseModel):
    titles:List[str] = Field(description="小红书的5个标题",
                             min_items=5,max_items=5) #允许的最大和最小元素数都是5，就强制是5个了
    content:str = Field(description="正文内容")
    



# 功能函数
def xiaohongshu_generator(api_key,subject,temperature):

    # 提示模板
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system",system_prompt_text),
            ("human",human_prompt_text)
        ]
    )

    # 模型
    model = ChatDeepSeek(model="deepseek-chat", #不能缺少模型
        api_key=api_key,
        temperature=temperature)
    
    # 输出解析器
    output_parser = PydanticOutputParser(pydantic_object=Xiaohongshu)

    result = (prompt_template|model|output_parser).invoke(
        {
            "parser_instruction":output_parser.get_format_instructions(),
            "subject":subject
        }
    )

    return result





