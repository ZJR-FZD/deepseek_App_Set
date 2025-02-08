import requests

# 请求参数
url = "https://cn.apihz.cn/api/zici/baikebaidu.php"
params = {
    "id": "10002402",  # 替换为你的用户ID
    "key": "f136bce1d05404ca8339d153ab5ed161",  # 替换为你的用户KEY
    "words": "汽车"  # 替换为要查询的内容
}

# 发送GET请求
response = requests.get(url, params=params)

# 解析返回的JSON数据
if response.status_code == 200:
    result = response.json()
    if result["code"] == 200:
        print("搜索结果：", result["msg"])
    else:
        print("错误信息：", result["msg"])
else:
    print("请求失败，状态码：", response.status_code)