import re
import random

text = """坚定不移 	 54113
随时随地 	 52510
全力以赴 	 36156
丰富多彩 	 34727
余波未平 	 32967
脱颖而出 	 31974
实事求是 	 31565
一如既往 	 30338
众所周知 	 29469
一年一度 	 29188
因地制宜 	 27805
千方百计 	 27561
息息相关 	 25804"""  # 这里是你提供的原始文本

# 使用正则表达式移除所有数字
cleaned_text = re.sub(r'\d+', '', text)

# 定义一个函数来随机插入逗号
def insert_commas(s):
    result = []
    for char in s:
        result.append(char)
        # 以一定的概率在字符后插入逗号
        if random.random() < 0.1:  # 这里0.1是插入逗号的概率，可以根据需要调整
            result.append(',')
    return ''.join(result)

# 调用函数并打印结果
# cleaned_text = insert_commas(cleaned_text)
print(cleaned_text)