import pandas as pd
import requests
import time
import os
import shutil
start_time = time.time()
i = 0
#
file_path = '../doc/语料1_temp.xlsx.xlsx'
temp_file_path = 'doc/语料1_temp.xlsx'
#  语料1_temp.xlsx覆盖语料1.xlsx，语料1_temp.xlsx不要删除
# shutil.copyfile(temp_file_path, file_path)

df = pd.read_excel(file_path)

if df.empty:
    print("DataFrame is empty.")
else:
    for index, row in df.iterrows():
        question = row['question']
        answer = row['answer']

        if pd.notna(answer):
            continue

        url = 'http://36.212.171.121:8000/chat_stream'
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ],
            "max_tokens": 32768
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            df.at[index, 'answer'] = response.text
            i += 1
            print(f"第{i}个 Updated answer for question: {question}")

            # 使用with语句来写入文件
            with pd.ExcelWriter(temp_file_path) as writer:
                df.to_excel(writer, index=False)

# 重命名临时文件为原文件
os.replace(temp_file_path, file_path)

end_time = time.time()
print("End time:", end_time)
print("Duration:", end_time - start_time)
print("更新完成")
