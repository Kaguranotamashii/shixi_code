import pandas as pd

# 读取Excel文件
file_path = '1sorted_audio_extraction_results.xlsx'  # 请将此路径替换为您的Excel文件的实际路径
df = pd.read_excel(file_path)

# 假设Excel文件有三列：源文本、返回的文本、得分率 (%)
# 确保列名与Excel文件中的列名一致
# 例如，如果列名分别是 '源文本', '返回的文本', '得分率 (%)'
df.columns = ['源文本', '返回的文本', '得分率 (%)']

# 计算得分率的平均值
average_score_rate = df['得分率 (%)'].mean()

print(f"得分率的平均值是: {average_score_rate}%")