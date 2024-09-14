import os
import requests
import pandas as pd
import re
import difflib

# 定义请求的URL
url = 'http://10.27.0.3:26401/audio_extraction'

# 定义保存文件的目录
directory = 'audio1'

# 初始化结果列表
results = []


# 函数用于计算准确率
def calculate_accuracy(original_text, response_text):
    # 去掉符号和数字
    original_text_clean = re.sub(r'\W+', '', original_text)
    original_text_clean = re.sub(r'[0-9\W]', '', original_text_clean)
    original_text= original_text_clean
    # 去除符号_
    original_text_clean = re.sub(r'_', '', original_text_clean)
    response_text_clean = re.sub(r'\W+', '', response_text)

    print(original_text_clean  + "  " + response_text_clean)
    # 使用difflib计算文本相似度
    similarity = difflib.SequenceMatcher(None, original_text_clean, response_text_clean).ratio()
    return round(similarity * 100, 2)


# 遍历目录中的MP4文件
for filename in os.listdir(directory):
    if filename.endswith(".mp3"):
        # 过滤掉文件名前面的数字和语言信息
        filtered_filename = re.sub(r'^\d+_(中文|日语|英文)(男|女)_', '', filename).replace('.mp3', '')

        print("正在处理文件：", filename)
        # 文件路径
        file_path = os.path.join(directory, filename)

        # 请求API
        try:
            with open(file_path, 'rb') as file:
                response = requests.post(url, files={'file': file})
                print("响应状态码：", response.status_code)

            # 检查请求是否成功
            if response.status_code == 200:
                response_json = response.json()
                response_text = response_json.get('text', '')

                # 计算准确率
                accuracy = calculate_accuracy(filtered_filename, response_text)
                print("准确率：", accuracy)

                original_text_clean = re.sub(r'\W+', '', filtered_filename)
                original_text_clean = re.sub(r'[0-9\W]', '', original_text_clean)



                # 保存结果
                results.append({
                    'File Name':   original_text_clean,
                    'Response Text': response_text,
                    'Accuracy (%)': accuracy
                })
            else:
                results.append({
                    'File Name': filtered_filename,
                    'Response Text': 'Request failed',
                    'Accuracy (%)': 'N/A'
                })

        except Exception as e:
            print("请求出错：", str(e))
            results.append({
                'File Name': filtered_filename,
                'Response Text': f'Error: {str(e)}',
                'Accuracy (%)': 'N/A'
            })

# 将结果保存到Excel
df = pd.DataFrame(results)
df.to_excel('audio_extraction_results.xlsx', index=False)

print("测试完成，结果保存到audio_extraction_results.xlsx")
