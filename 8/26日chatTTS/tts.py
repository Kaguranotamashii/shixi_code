import requests
import pandas as pd
import os
import re

# 定义 URL 和 str
url = "http://36.212.171.121:1080/tts"
audio_seeds = [1528]
str_content = """
坚定不移
随时随地
全力以赴
丰富多彩
余波未平
算法
数据结构
人工智能
机器学习
深度学习
神经网络
大数据
云计算
物联网
区块链
网络安全
软件工程
操作系统
数据库
编程语言
计算机视觉
自然语言处理
人机交互
虚拟现实
增强现实
量子计算
信息检索
数据挖掘
知识图谱
软件测试
系统分析
项目管理
敏捷开发
金融工程
投资组合
风险管理
财务分析
会计学
市场营销
经济学
管理学
国际贸易
货币银行学
证券投资
保险学
税收筹划
企业战略
人力资源
供应链管理
运营管理
商业智能
电子商务
消费者行为
品牌管理
市场调研
论文写作
学术研究
文献综述
研究方法
数据分析
统计学
实验设计
定量研究
定性研究
案例研究
学术伦理
学术出版
学术会议
学术交流
博士论文
硕士论文
本科论文
学位论文
开题报告
中期报告
答辩
学术期刊
学术专著
细胞生物学
分子生物学
遗传学
生态学
进化生物学
微生物学
植物学
动物学
解剖学
生理学
生物化学
生物物理学
免疫学
发育生物学
神经生物学
行为学
基因组学
蛋白质组学
代谢组学
转录组学
表观遗传学
系统生物学
生物信息学
生物工程
生物技术
生物多样性
保护生物学
环境生物学
海洋生物学
古生物学
药理学
毒理学
病理学
临床生物学
摘要
分析
论证
评估
偏差
案例研究
引用
连贯性
结论
概念
相关性
数据
演绎
定义
设计
论文
经验
认识论
评价
证据
实验
阐述
框架
概括
假设
推理
解释
论证
文献综述
逻辑
方法论
模型
范式
同行评审
视角
现象
理论
原理
结构
知识体系
定性分析
定量分析
范畴
论点
议题
信度
效度
假说
模式
变量
对照组
影响因素
权威
统计
实证研究
因果关系
样本
变量控制
参考文献
系统论
归纳法
认知
社会结构
社会学
伦理学
美学
修辞
语义学
音位学
文法
形态学
语用学
心理学
语言学
思辨
文化
变迁
创新
历史背景
社会变革
文化认同
理念
社会互动
意识形态
权力结构
话语分析
社会阶层
公共政策
全球化
伦理道德
学术规范
研究方法
实验设计
科学方法
数据处理
学术批评
知识产权
思想体系
学术写作
概念框架
"""
# 将 str 按行分割
lines = str_content.strip().split('\n')

# 初始化一个空的 DataFrame
df = pd.DataFrame(columns=['Text', 'Audio Link'])

# 创建一个目录来保存音频文件
output_dir = 'audio_files1'
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
    name = 'TTS接口测试output_'+str(audio_seed)+'.xlsx'
    df.to_excel(name, index=False, engine='openpyxl')
