def remove_empty_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 检查行是否为空或仅包含空白字符
            if line.strip():
                outfile.write(line)

# 使用示例
input_file = 'input.txt'  # 替换为你的输入文件名
output_file = 'output.txt'  # 替换为你的输出文件名
remove_empty_lines(input_file, output_file)