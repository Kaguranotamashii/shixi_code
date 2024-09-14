import requests
import pandas as pd

# API的URL
url = 'http://10.27.0.2:62000/expert/classify'

# 读取txt文件内容
with open('juese.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 准备表格数据
data = {
    'Prompt': [],
    'Expert': []
}

# 遍历每一行并发起请求
for line in lines:
    line = line.strip()  # 去除两边的空白字符
    if line == '':
        # 如果是空行，则插入空行到表格
        data['Prompt'].append('')
        data['Expert'].append('')
        continue

    print('正在处理：', line)
    # 构造请求的payload
    payload = {
        "prompt": line
    }

    # 发起POST请求
    try:
        response = requests.post(url, json=payload, headers={
            'accept': 'application/json',
            'Content-Type': 'application/json'
        })
        response_data = response.json()
        print("response_data:", response_data)

        # 提取expert字段
        expert = response_data.get('expert', 'N/A')
        # print("expert:", expert)

    except Exception as e:
        expert = f"Error: {str(e)}"

    # 将结果添加到表格数据中
    data['Prompt'].append(line)
    data['Expert'].append(expert)

# 创建DataFrame
df = pd.DataFrame(data)

# 将DataFrame导出到Excel文件
df.to_excel('output.xlsx', index=False)

print("数据已保存到 output.xlsx 文件中")
