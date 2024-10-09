
import pandas as pd
import json

# 读取原始Excel文件
input_file = 'input.xlsx'
df = pd.read_excel(input_file)

# 新的DataFrame用于保存提取的title和url
output_data = {'Title': [], 'URL': []}

# 遍历Excel文件中的每一行
for index, row in df.iterrows():
    text = row['Content']
    # 查找"type":"source"的索引
    source_index = text.find('"type":"source"')

    # 如果找到了"type":"source"
    if source_index != -1:
        try:
            # 向前查找左大括号 '{' 的索引
            left_brace_index = text.rfind('{', 0, source_index)

            # 初始化括号计数
            brace_count = 0
            right_brace_index = left_brace_index

            # 从左大括号之后开始查找匹配的右大括号
            for i in range(left_brace_index, len(text)):
                if text[i] == '{':
                    brace_count += 1
                elif text[i] == '}':
                    brace_count -= 1

                # 当计数归零时，意味着找到了匹配的右大括号
                if brace_count == 0:
                    right_brace_index = i
                    break

            # 检查是否找到了有效的左右括号
            if left_brace_index != -1 and right_brace_index != -1:
                json_string = text[left_brace_index:right_brace_index + 1]

                print(json_string)

                # 将当前行内容解析为JSON
                data = json.loads(json_string)

                # 检查JSON中是否有"type":"source"
                if data.get("type") == "source":
                    for document in data.get('documents', []):
                        # 提取title和url
                        title = document.get('title', 'No Title')
                        url = document.get('url', 'No URL')
                        output_data['Title'].append(title)
                        output_data['URL'].append(url)
        except json.JSONDecodeError:
            print(f"Invalid JSON in row {index}")
            continue
    else:
        print('未找到"type":"source"')

# 将提取到的数据保存为新的Excel文件
output_df = pd.DataFrame(output_data)
output_file = 'extracted_titles_urls.xlsx'
output_df.to_excel(output_file, index=False)

print(f"Extracted data saved to {output_file}")