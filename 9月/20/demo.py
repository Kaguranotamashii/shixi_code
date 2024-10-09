import requests
import pandas as pd

# 读取本地文件
with open('lv.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 初始化数据列表
data_list = []


# 发送请求并处理每一行
for line in lines:
    query = line.strip()
    url = "http://36.213.14.38:20008/travel_similarity_search"
    data = {
        "query": query,
        "top_k": 20,
        "search_score": 0.9
    }
    response = requests.post(url, json=data)

    # 检查请求是否成功
    if response.status_code == 200:
        results = response.json()
        print(f"请求成功，查询内容：{query}")

        # 准备数据
        for item in results:
            data_list.append({
                'Question': query,  # 每一行都显示提问的问题
                'Title': item['title'],
                'Author': item['author'],
                'Category': item['category'],
                'Content': item['content'],
                'URL': item['url'],
                'Score': item['score']
            })
    else:
        print(f"请求失败，状态码：{response.status_code}, 查询内容：{query}")

# 转换为DataFrame
df = pd.DataFrame(data_list)

# 写入Excel文件
df.to_excel('results.xlsx', index=False)
print("数据已写入Excel文件。")