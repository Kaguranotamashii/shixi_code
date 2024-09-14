import requests
import pandas as pd
import os
import re

# 定义 URL 和 str
url = "http://36.212.171.121:1080/tts"
audio_seeds = [1528]
str_content = """
小美：你觉得我们是不是应该更进一步了？小杰：我也这么想，但我有点紧张。
老王：对最近的选举有什么看法？小李：我觉得候选人的政策都不够具体。
小张：你准备怎么复习这次考试？小赵：我想先整理笔记，然后做些练习题。
小陈：我们下次旅行去哪里好呢？小林：我一直想去日本，你觉得怎么样？
小刘：你周末打算怎么过？小黄：我想带家人去郊外野餐。
小杨：你相信一见钟情吗？小吴：我相信，但我更相信日久生情。
小周：你对国际形势怎么看？小郑：我觉得合作比对抗更有利于发展。
小孙：你最近在学什么新技能？小钱：我在尝试学习编程。
小冯：你上次旅行有什么特别经历吗？小褚：我在巴黎差点迷路了，但最后找到了埃菲尔铁塔。
小卫：你家里最近有什么新鲜事？小蒋：我弟弟刚考上大学，全家都很高兴。
小沈：你觉得恋爱中最重要的是什么？小韩：我觉得是信任和沟通。
小杨：你对环保政策有什么建议？小朱：我认为应该加强公众教育，提高环保意识。
小秦：你有什么学习法推荐吗？小尤：我觉得定期复习很重要。
帮我会议设备重新调试。
帮我会议环境调整到明亮宽敞。
帮我会议议题简化处理。
原以为自己已经放下了，直到看到那张熟悉的照片，才发现心里依旧疼痛难忍。
独自坐在咖啡馆的角落，望着窗外的细雨，感受到一种无法言喻的孤独。
看着旧时的照片，那些曾经熟悉的面孔，如今却都变得遥不可及。
曾经说好一起走到最后的人，如今却走散在时间的洪流中，留下的只有无尽的遗憾。
今天收到一封老朋友的信，读到最后才知道他已经不在了，心里的痛像被针刺一般。
想到已经好久没有联系的朋友，翻遍了通讯录却不敢拨出那个号码。
今天在家里翻出一件旧衣服，满是回忆，穿在身上却再也找不回当初的感觉。
曾经热闹的群聊如今只剩下零星的几句话，曾经的我们到底去了哪里？
原本热闹的家庭聚会，因为少了一个重要的人而显得格外冷清。
收拾房间时，意外发现了一封旧信，读完后心情沉重了许多。
今天在路上看到一对牵手的老人，突然想起了自己已经离世的外公外婆，心里难过得无以复加。
昨晚做了一个美好的梦，梦中和他重逢了，醒来时泪水湿透了枕头，好伤心。
今天在街上偶遇了一位老同学，互相微笑点头后，却再也没有说出一句话，心里说不出的落寞。
突然发现朋友圈里某位常常互动的朋友消失了，翻看他最后的动态，才知道他已经离开了这个世界。
今天整理老家的旧物，发现了一本小时候的日记，那时的无忧无虑仿佛是另一个世界。
午后看了一场电影，剧情不紧不慢，节奏适中。
今天的会议讨论了几个问题，结论也在意料之中。
整理了电脑里的文件，和往常一样。
这杯茶水的温度刚好，能喝。
出门前检查了天气，和预报的一样，没有太多变化。
早晨起床后，拉开窗帘，阳光照进来，暖意刚好。
中午在街边小店吃了顿饭，味道很普通，没什么特别的。
收到了一封短信，内容是例行通知，没有引起特别的注意。
早上散步回来，空气清新，但也没什么特别的感受。
读了一篇博客，内容很实用，但也没什么新意。
下午的时间在阅读中度过，书中的内容平实，有点小收获。
今天下班回家，发现房间里依旧只有我一个人，空荡荡的感觉让人无法忍受伤感。
曾经一起畅谈未来的朋友，如今却成了陌路人，心里满是难以言说的痛。
今天在公园里看到一对老夫妻，想起了自己的父母，他们却再也无法牵手走在一起了。
昨天夜里失眠了，脑海里不断浮现出那些曾经的画面，心里满是无法排解的痛苦。
收到朋友发来的一张合照，照片里的人已经不在了，心里一阵难过。
今天看到一则旧时的新闻，才知道那个曾经和我一起奋斗的人已经去世了，心里难以承受。
在网上看到了朋友的婚礼照片，心里却满是无法言说的失落与痛苦。
今天在家里翻出了一本老相册，翻看时泪水止不住地流了下来，心里满是怀念与感伤。
走在街上看到一个熟悉的身影，心跳加速地追上去，才发现认错了人，心里满是难以言说的失落。
今天和家人通了电话，听到他们的声音心里满是酸楚，已经很久没有回家陪他们了。
在公司里看着那些熟悉的面孔，突然意识到自己已经在这里待了这么多年，心里满是感慨与伤感。
今天收到了一张朋友的结婚请柬，看到他脸上的笑容，心里却满是失落与痛苦。
昨晚梦到了已经去世的亲人，梦里我们又回到了从前，醒来时心里满是悲伤。
每天起床，我都会微笑迎接新的一天。
无论是晴天还是雨天，我都会保持积极心态。
努力工作，不断学习，是我克服困难的方式。
保持健康的生活习惯，如按时吃饭和适量运动。
充足睡眠让我精力充沛，迎接每一个挑战。
实现目标，无论是个人成长还是职业发展。
因为我相信耐心和不放弃的力量。
勇敢面对挫折，从中吸取教训，继续前进。
失败是成功之母，每一次跌倒都是成长的机会。
珍惜时间，合理规划日程，确保陪伴家人。
家庭和友情是我最宝贵的财富，我会用行动去关爱。
"""
# 将 str 按行分割
lines = str_content.strip().split('\n')

# 初始化一个空的 DataFrame
df = pd.DataFrame(columns=['Text', 'Audio Link'])

# 创建一个目录来保存音频文件
output_dir = 'audio_files日常对话'
os.makedirs(output_dir, exist_ok=True)

# 定义一个函数来清理文件名
def clean_filename(filename):
    # 检验下如果太长了就缩短十个字符加上......
    if len(filename) > 10:
        filename = filename[:30] + "......省略若干个字符"

    # 去除非法字符
    return re.sub(r'[\\/*?:"<>|\t\n]', "", filename)


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
            audio_link = f'=HYPERLINK("{audio_file_name}", "Play Audio")'

            # 将文本和音频文件路径添加到 DataFrame
            new_row = pd.DataFrame({'Text': [line], 'Audio Link': [audio_link]})
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            print(f"Failed to get audio for text: {line}")

    # 将 DataFrame 保存为 Excel 文件
    name = 'TTS接口测试output_日常对话'+str(audio_seed)+'.xlsx'
    df.to_excel(name, index=False, engine='openpyxl')
