
# 读取name.txt文件中的每一行，并去除重复行，然后保存到name1.txt

# 打开name.txt文件，读取每一行并去除重复行
with open('name.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 去除重复行
unique_lines = list(set(lines))

# 去除每行末尾的换行符
unique_lines = [line.strip() for line in unique_lines]

# 将去重后的结果保存到name1.txt文件
with open('name1.txt', 'w', encoding='utf-8') as file:
    for line in unique_lines:
        file.write(line + '\n')

print("去重后的数据已保存到 name1.txt")