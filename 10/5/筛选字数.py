# 打开原始文件1.txt进行读取
with open('2.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 创建一个新的文本文件，用于存放筛选后的内容
with open('filtered_lines2.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        # 去除每行的换行符，然后检查长度
        if len(line.strip()) > 8:
            # 如果长度大于10，写入到新文件中
            new_file.write(line)