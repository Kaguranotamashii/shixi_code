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
早上好，今天的天气真是great。
你的新iPhone看起来很酷，多少钱买的？
我喜欢听周杰伦的“青花瓷”，旋律非常beautiful。
周末我们去shopping吧，我需要买些新衣服。
你的英语口语进步了很多，真的很impressive。
这个项目的deadline是下周，我们需要尽快finish所有的任务。
我最近在读一本叫做"The Art of War"的书，它是关于strategy的。
你能帮我check一下这个email吗？我不确定我是否reply了。
我喜欢在周末去hiking，尤其是去那些有beautiful scenery的地方。
你的presentation准备得怎么样了？别忘了加入一些visual aids。
这个report的data需要我们仔细analyze。
我昨天download了一个app，它可以帮我practice英语。
你能帮我book一个table吗？我想邀请一些friends来dinner。
这个website的设计非常user-friendly，我很快就找到了我想要的信息。
我需要去bank deposit一些钱，你能陪我去吗？
我喜欢在cafe里sit一会儿，享受一下morning的阳光。
你能帮我translate这句话吗？我想发给我的一个foreign friend。
这个document需要我们team一起review。
我最近在study一个online course，是关于marketing的。
这个meeting的agenda是什么？我需要prepare我的部分。
我喜欢在evening散步，因为那时候的天气比较cool。
你能帮我print这些documents吗？我马上需要用到。
这个project的budget需要我们仔细manage。
我昨天watch了一个movie，它的故事非常touching。
这个recipe的ingredients你能帮我check一下吗？我不确定我是否买全了。

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
df.to_excel("output_audio_中英混合"+role+"_links.xlsx", index=False)
