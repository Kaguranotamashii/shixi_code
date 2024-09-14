import os
import requests
import pandas as pd


# 定义一个清理文件名的函数，确保文件名不会包含非法字符
def clean_filename(filename):
    return "".join(c if c.isalnum() else "_" for c in filename)


# 设置存放音频文件的目录
output_dir = "output_audio"
os.makedirs(output_dir, exist_ok=True)

# 初始化一个 DataFrame 用于保存文本和音频链接
df = pd.DataFrame(columns=['Text', 'Audio Link'])

# 定义多行字符串，表示要请求的文本，每行一段内容
multi_line_text = """
你好こんにちは，今天的天气真好。
我想去日本旅行にっぽんりょこう。
这个苹果很好吃りんごおいしい。
我喜欢寿司すし，你呢？
你看过这部电影吗？えいが。
请给我一杯咖啡ください、コーヒーを一杯。
你的名字是？あなたの名前は？
这本书很有趣本ほんおもしろい。
我喜欢听音乐音楽を聴きたい。
你有空吗？時間ありますか？

"""

# API的URL和默认的音频文件命名种子
api_url = 'http://10.27.0.2:50001/api/inference/sft'
audio_seed = 1
role='中文男'
# 遍历每行文本
for line in multi_line_text.strip().split('\n'):
    # 去除两边的空白字符（包括换行符）
    line = line.strip()

    # 如果该行文本不为空，继续处理
    if line:
        # 准备发送给API的请求数据
        data = {
            'tts': line,
            'role': role
        }

        # 向API发送POST请求
        response = requests.post(api_url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        # 检查请求是否成功
        if response.status_code == 200:
            # 清理文本以创建有效的音频文件名
            clean_line = clean_filename(line)
            audio_file_name = os.path.join(output_dir, f"{str(audio_seed)}_{role}_{clean_line}.mp3")

            # 保存音频数据到文件
            with open(audio_file_name, 'wb') as f:
                f.write(response.content)

            print(f"音频保存至 {audio_file_name}")

            # 创建音频文件的超链接，用于插入到Excel中
            audio_link = f'=HYPERLINK("{audio_file_name}", "Play Audio")'

            # 将文本和超链接添加到 DataFrame
            new_row = pd.DataFrame({'Text': [line], 'Audio Link': [audio_link]})
            df = pd.concat([df, new_row], ignore_index=True)

            # 增加音频文件命名种子，以确保文件名唯一
            audio_seed += 1
        else:
            # 请求失败时打印错误信息
            print(f"获取音频失败，文本内容: {line}")

# 保存最终的 DataFrame 到 Excel 文件
df.to_excel("output_audio_中日混合"+role+"_links.xlsx", index=False)
