from langchain_deepseek import ChatDeepSeek
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import json

PROMPT_TEMPLATE = """
    你是一位数据分析助手，你的回应内容取决于用户的请求内容。

    1. 对于文字回答的问题，按照这样的格式回答：
        {"answer": "<你的答案写在这里>"}
    例如：
        {"answer": "订单量最高的产品ID是!MNWC3-067"}

    2. 如果用户需要一个表格，按照这样的格式回答：
        {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...],[value1, value2, ...],...]}}

    3. 如果用户的请求适合返回条形图，按照这样的格式回答：
        {"bar": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

    4. 如果用户的请求适合返回折线图，按照这样的格式回答：
        {"line": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

    5. 如果用户的请求适合返回散点图，按照这样的格式回答：
         {"scatter": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
    注意：我们只支持三种类型的图表："bar", "line" 和 "scatter"。

    请将所有输出作为JSON字符串返回。请注意要将"columns"列表和数据列表中的所有字符串都用双引号包围。
    例如：{"columns": ["Products", "Orders"], "data": [["32085Lip", 245], ["76439Eye", 178]]}

    你要处理的用户请求如下：
    """

def dataframe_agent(api_key, uploaded_file, query):
    model = ChatDeepSeek(model="deepseek-chat",api_key=api_key,
                       temperature=0)
    
    # path 复制文件到本地，得到路径
    file_content = uploaded_file.getvalue() #.read()改成.getvalue()，就能读了
    print(file_content)
    print(type(file_content))
    print(type(file_content))
    file_path = "temp.csv"
    with open(file_path,"wb") as fwb:
        fwb.write(file_content)
 
    
    # agent执行器
    agent_executor = create_csv_agent(
        llm=model,
        path=file_path,
        allow_dangerous_code=True,
        agent_executor_kwargs={
            "handle_parsing_errors": True
        },
        verbose=True
    )

    # 输入 = 我们补充的提示 + 用户输入
    prompt = PROMPT_TEMPLATE + query
    result = agent_executor.invoke({
        "input": prompt
    })

    try : result_dict = json.loads(result["output"]) #实际输出的内容是output键对应的值，然后把它解析成字典，方便前端使用
    finally : print(result["output"])
    return result_dict


    
