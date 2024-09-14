import os
import base64

import openpyxl
import requests
import json
import pandas as pd
from io import BytesIO
from PIL import Image

# 定义文件夹路径和接口URL
folder_path = r'C:\Users\admin\Downloads\图片助手(ImageAssistant)_批量图片下载器\人脸_高兴_-_搜索_图片\PNG'
api_url = 'http://192.168.1.30:6001/emotion'

# 用于存储结果的列表
results = []

# 遍历文件夹中的所有PNG图片
for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        # 构建文件的完整路径
        file_path = os.path.join(folder_path, filename)

        # 读取图片文件并转换为Base64编码
        with open(file_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # 构建请求的JSON数据
        payload = {
            "type": "c3",
            "items": [
                {
                    "type": "imageData",
                    "data": encoded_string
                }
            ]
        }

        # 发送POST请求
        response = requests.post(api_url, json=payload)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应JSON数据
            response_data = response.json()
            # 将图片文件名和响应数据添加到结果列表中
            results.append((filename, response_data))
        else:
            print(f"Failed to get response for {filename}: {response.status_code}")

# 创建DataFrame
df = pd.DataFrame(results, columns=['图片', '返回数据'])


# 定义一个函数来显示图片
def embed_image(data):
    img_data = base64.b64decode(data)
    img = Image.open(BytesIO(img_data))
    img = img.resize((100, 100))  # 调整图片大小
    return img


# 将图片嵌入到DataFrame中
df['图片'] = df['图片'].apply(lambda x: embed_image(base64.b64encode(open(os.path.join(folder_path, x), 'rb').read())))

# 保存DataFrame到Excel文件
with pd.ExcelWriter('results2.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Results', index=False)

    # 获取工作表
    worksheet = writer.sheets['Results']

    # 添加图片到单元格
    for idx, row in df.iterrows():
        img = row['图片']
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        img = openpyxl.drawing.image.Image(img_bytes)
        img.width = 100
        img.height = 100
        worksheet.add_image(img, f'A{idx + 2}')

print("结果已保存到 results.xlsx 文件中。")