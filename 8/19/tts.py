import requests
import pandas as pd
import os
import re

# 定义 URL 和 str
url = "http://36.212.171.121:1080/tts"
audio_seeds = [1528, 1185, 1397, 11]
str_content = """
你好，今天天气如何？
我想去海边散步。
《黑神话：悟空》，一款由游戏科学开发的西游题材单机·动作·角色扮演游戏。
君不见黄河之水天上来，奔流到海不复回。 君不见高堂明镜悲白发，朝如青丝暮成雪。 人生得意须尽欢，莫使金樽空对月。 天生我材必有用，千金散尽还复来。
魃魈魁鬾魑魅魍魉，又双叒叕。火炎焱燚，水沝淼㵘，㙓。𨰻火炎焱燚，水沝淼㵘，㙓。𨰻娉婷袅娜涕泗滂沱，呶呶不休不稂不莠。卬，咄嗟蹀躞耄耋饕餮，囹圄蘡薁觊觎龃龉。狖轭鼯轩怙恶不悛，其靁虺虺腌臜孑孓。
大家好，我是宋宇然，一名即将迈入大学四年级的计算机科学与技术专业的学生，就读于北京信息科技大学。在这里，我不仅沉浸在代码的世界里，探索技术的无限可能，也享受着校园生活的多姿多彩。我热爱电影，每部作品都是一个全新的世界，让我体验不同的生活和文化。音乐对我来说，是生活中不可或缺的调味品，无论是激昂的摇滚还是轻柔的爵士，都能带给我灵感和放松。至于篮球，那是我释放激情和压力的方式，每一次投篮都是对自我挑战的尝试。我期待着在接下来的日子里，无论是在学术上还是个人兴趣上，都能够不断进步，实现自我超越。希望在未来的学习和生活中，能够与大家共同成长，创造更多美好的回忆。
1234567890qwertyuiopasdfghjklzxcvb
!@#$%^&*(){}:"<>?/.,;'[]
！@#￥%……&*（）——+{}|：“《》？
Despite the relentless rain, the determined hikers pressed on, seeking the summit's panoramic view
In the heart of the bustling market, the aroma of fresh bread wafted through the air, enticing passersby
Wjrm qhvjzq, xir rplejc yqirg
Ykocx zsuwjm, vjg qmbkqs jcmvn
Tjv qmcu qzhjki, lqirg rjv vjg zcv
他建议我们尝试一些organic food，说这对健康有好处。
这个app的设计非常user-friendly，即使是初学者也能快速上手。
我们的目标是提高customer satisfaction，同时reduce operational costs
这个课程将涵盖基础的mathematical concepts和一些实际的applications。
他提议我们去郊外的camping site，体验一下outdoor life
わたしはがくせいです。
彼は日本人ではありません
昨日はとても暑かったです
哇，这真是太棒了！
我真的好难过，希望一切都能好起来。
你确定这个决定是对的吗？
尊敬的客户，感谢您选择我们的服务。我们致力于为您提供最优质的体验，如果您有任何问题，请随时联系我们。
无论遇到什么困难，只要我们团结一致，一定能够克服所有的挑战，实现我们的目标。
侬晓得伐？额寻到了一份新工作。
小囡，侬听妈妈话，勿要淘气。
聽講今日有場好嘅電影，你有興趣一齊去睇嗎？
今晚我煮咗你最鍾意食嘅糖醋排骨，快啲嚟食啦。
q
w
e
r
t
y
u
i
o
p
a
s
d
f
g
h
j
k
l
z
x
c
v
b
n
m
nm
test
wow
abc
bbc
1
2
3
4
5
6
7
8
9
0
10
21
32
43
54
65
76
87
98
100
2134
99999
1234567890
99,999
12,123,234,44444
1,2,3,4,5,6,7,8,9
10,11,12,13,14,15,16
1,123,123456

"""

# 将 str 按行分割
lines = str_content.strip().split('\n')

# 初始化一个空的 DataFrame
df = pd.DataFrame(columns=['Text', 'Audio Link'])

# 创建一个目录来保存音频文件
output_dir = 'audio_files'
os.makedirs(output_dir, exist_ok=True)

# 定义一个函数来清理文件名
def clean_filename(filename):
    # 检验下如果太长了就缩短十个字符加上......
    if len(filename) > 10:
        filename = filename[:10] + "......省略若干个字符"

    # 去除非法字符
    return re.sub(r'[\\/*?:"<>|]', "", filename)

for audio_seed in audio_seeds:
    # 遍历每一行文本
    for line in lines:
        payload = {
            "text": [line],
            "stream": False,
            "lang": None,
            "skip_refine_text": True,
            "refine_text_only": False,
            "use_decoder": True,
            "audio_seed": audio_seed,
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
            # 生成音频文件名并清理
            clean_line = clean_filename(line)
            audio_file_name = os.path.join(output_dir, f"{str(audio_seed)}_{clean_line}.mp3")
            print(f"Audio saved to {audio_file_name}")
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
    name = 'TTS接口测试output_'+str(audio_seed)+'.xlsx'
    df.to_excel(name, index=False, engine='openpyxl')
