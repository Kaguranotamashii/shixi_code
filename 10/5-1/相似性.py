import pandas as pd

# 读取Excel文件
file_path = '相似度1.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 判断C列是否包含B列的内容，并将结果存储在D列
df['是否包含'] = df.apply(lambda row: 'Yes' if str(row['预期文件']) in str(row['来源']) else 'No', axis=1)

# 保存修改后的Excel文件
output_file_path = 'output_excel_file1.xlsx'  # 替换为你想要保存的文件路径
df.to_excel(output_file_path, index=False)

print("处理完成，结果已保存到:", output_file_path)