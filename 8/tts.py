import requests
import pandas as pd
import os

# 定义 URL 和 str
url = "http://36.212.171.121:1080/tts"
str_content = """
你好世界！
你好！
测试！
我是宋宇然，你叫什么名字
"""

# 将 str 按行分割
lines = str_content.strip().split('\n')

# 初始化一个空的 DataFrame
df = pd.DataFrame(columns=['Text', 'Audio Link'])

# 创建一个目录来保存音频文件
output_dir = '../audio_files'
os.makedirs(output_dir, exist_ok=True)

# 遍历每一行文本
for line in lines:
    payload = {
        "text": [line],
        "stream": False,
        "lang": None,
        "skip_refine_text": True,
        "refine_text_only": False,
        "use_decoder": True,
        "audio_seed": 1528,
        "text_seed": 87654321,
        "do_text_normalization": True,
        "do_homophone_replacement": False,
        "params_refine_text": {
            "prompt": "",
            "top_P": 0.7,
            "top_K": 20,
            "temperature": 0.7,
            "repetition_penalty": 1,
            "max_new_token": 384,
            "min_new_token": 0,
            "show_tqdm": True,
            "ensure_non_empty": True,
            "stream_batch": 24
        },
        "params_infer_code": {
            "prompt": "[speed_2]",
            "top_P": 0.1,
            "top_K": 20,
            "temperature": 0.3,
            "repetition_penalty": 1.05,
            "max_new_token": 2048,
            "min_new_token": 0,
            "show_tqdm": True,
            "ensure_non_empty": True,
            "stream_batch": True,
            "spk_emb": None
        }
    }

    # 发送 POST 请求
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        # 生成音频文件名
        audio_file_name = os.path.join(output_dir, f"{line}.mp3")

        # 将音频数据保存为文件
        with open(audio_file_name, 'wb') as f:
            f.write(response.content)

        # 创建音频文件的超链接
        audio_link = f'=HYPERLINK("{os.path.abspath(audio_file_name)}", "Play Audio")'

        # 将文本和音频文件路径添加到 DataFrame
        new_row = pd.DataFrame({'Text': [line], 'Audio Link': [audio_link]})
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        print(f"Failed to get audio for text: {line}")

# 将 DataFrame 保存为 Excel 文件
df.to_excel('output.xlsx', index=False, engine='openpyxl')