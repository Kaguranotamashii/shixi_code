import requests
import json
import pandas as pd

# 读取Excel文件
input_file = "1.xlsx"
output_file = "相似度1.xlsx"

# 读取问题
df = pd.read_excel(input_file)


# 定义API请求函数
def get_similarity_search_result(query):
    url = "http://192.168.2.51:8000/similarity_search"
    payload = json.dumps({
        "query": query,
        "top_k": 5000,
        "search_score": 0.95
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # 检查HTTP状态码是否为200
        print(response.json())

        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None


# 遍历每个问题并获取答案
answers = []
for index, row in df.iterrows():
    question = row['问题']  # 假设问题列名为'问题'
    answer = get_similarity_search_result(question)
    if answer is not None:
        print(answer)
        # 只保留source和score字段
        filtered_answer = [{'source': item['source'], 'score': item['score']} for item in answer]
        answers.append(filtered_answer)
    else:
        answers.append(None)

# 将答案写入DataFrame
df['来源'] = answers

# 将结果写回Excel文件
df.to_excel(output_file, index=False)

print("答案已写入到", output_file)

#这里再运行本地的相似性.py
