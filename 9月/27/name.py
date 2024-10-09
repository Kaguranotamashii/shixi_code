import requests
import pandas as pd

# 设置请求的URL
url = "https://search-dev.ssk.ai/web/api/user/config"

# 设置请求的headers
headers = {
    "Cookie": "aisession=ra_LtVwvHsklg7YIwfj4na4FUa5bj2Ka.EVzYVSg3ngRbhyGf190ox13zq7t3whoXy%2BIfNsQBwNE",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    "Origin": "https://search-dev.ssk.ai",
    "Referer": "https://search-dev.ssk.ai/"
}

# 设置请求的body
data = {
    "config": {
        "news": False,
        "music": False,
        "style": "prompt"
    }
}

# 创建一个空的DataFrame
df = pd.DataFrame(columns=['Username', 'Response'])

# 打开本地的name.txt文件
with open('name1.txt', 'r', encoding='utf-8') as file:
    for line in file:
        data = {
            "config": {
                "news": False,
                "music": False,
                "style": "prompt"
            },
            "username": line.strip(),
        }

        username = line.strip()  # 去除每行的空白字符
        # data['config']['username'] = username  # 设置用户名
        response = requests.post(url, json=data, headers=headers)  # 发送POST请求

        if response.status_code == 200:
            new_row = pd.DataFrame({'Username': [username], 'Response': [response.json()]})
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            print(f"请求失败：{username} - 状态码：{response.status_code}")

# 将DataFrame保存为Excel文件
df.to_excel('output1.xlsx', index=False)

print("Data has been saved to output.xlsx")
