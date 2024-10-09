import requests
import pandas as pd

# 定义请求的URL和请求头
url = 'http://localhost:8501/recommend_topic'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# 读取Excel文件
input_file = 'input.xlsx'
output_file = 'output.xlsx'

df = pd.read_excel(input_file)

# 初始化结果列表
results = []

# 遍历每一行数据
for index, row in df.iterrows():
    user_question = row['user_question']
    history = row['history']

    # 构建请求数据
    data = {
        "user_question": user_question,
        "history": [history]
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, json=data)

    # 解析响应
    if response.status_code == 200:
        response_data = response.json()
        topic = response_data.get('topic', '')
        is_success = response_data.get('is_success', False)
    else:
        topic = ''
        is_success = False

    # 将结果添加到列表中
    results.append({
        'user_question': user_question,
        'history': history,
        'is_success': is_success,
        'topic': topic
    })

# 将结果写入新的Excel文件
output_df = pd.DataFrame(results)
output_df.to_excel(output_file, index=False)

print(f"Results have been written to {output_file}")

