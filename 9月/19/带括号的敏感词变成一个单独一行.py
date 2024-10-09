
# 尝试使用utf-8编码读取文件
try:
    with open('GFW补充词库.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
except UnicodeDecodeError:
    # 如果utf-8也不行，尝试忽略错误
    with open('GFW补充词库.txt', 'r', encoding='gbk', errors='ignore') as f:
        content = f.read()
        print(content)

# 将句子里面带有,间隔的单独成为一个列表
words = content.split(',')
# 将列表里面的数据打印本地文件敏感词GFW。txt
with open('敏感词GFW.txt', 'w') as f:
    for word in words:
        f.write(word + '\n')