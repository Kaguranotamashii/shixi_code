import random
import time
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# 读取问题
with open('key.txt', 'r', encoding='utf-8') as file:
    questions = [question.strip() for question in file.readlines() if question.strip()]

# API请求参数
api_url = "https://search-dev.ssk.ai/web/api/searchV2"
params_template = {
    'append': 'false',
    'sessionId': 'd6728b26-172f-406b-806e-2df480788eba',
    'page': 'souyisou',
    'topic': 'remote',
    'q_lang': '',
    'a_lang': 'undefined',
    'model': 'simple'
}

# 存储问题和答案的哈希表
results = {}


def fetch_answer(question):
    params = params_template.copy()

    # 随机生成0到5秒之间的延时时间
    delay_time = random.uniform(0, 2)
    time.sleep(delay_time)

    params['question'] = question
    print(question)
    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            return question, response.text
        else:
            return question, 'Error: Unable to fetch answer'
    except Exception as e:
        return question, f'Error: {str(e)}'


# 使用ThreadPoolExecutor来并发执行请求
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_question = {}

    for question in questions:
        # 在每次创建线程之前随机延迟
        delay_time = random.uniform(0, 2)
        time.sleep(delay_time)

        future = executor.submit(fetch_answer, question)
        future_to_question[future] = question

    for future in future_to_question:
        # 在每次处理结果之前随机延迟
        delay_time = random.uniform(0, 2)
        time.sleep(delay_time)

        question, answer = future.result()
        results[question] = answer

# 将结果转换为DataFrame并保存到Excel文件
df = pd.DataFrame(list(results.items()), columns=['Question', 'Answer'])
df.to_excel('answers1.xlsx', index=False)

print("Data has been saved to answers1.xlsx")
