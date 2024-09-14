import pandas as pd

# 读取Excel文件
df = pd.read_excel('语音转文字接口准确度测试.xlsx')

# 确保Accuracy列是数值类型
df['Accuracy (%)'] = pd.to_numeric(df['Accuracy (%)'], errors='coerce')

# 按照Accuracy降序排序
df_sorted = df.sort_values(by='Accuracy (%)', ascending=False)

# 保存到新的Excel文件
df_sorted.to_excel('1sorted_audio_extraction_results.xlsx', index=False)

# 计算Accuracy中80以上的占比
# accuracy_80_plus_count = len(df_sorted[df_sorted['Accuracy (%)'] >= 80]) / len(df_sorted) * 100
# 计算Accuracy中60到80的占比
accuracy_60_80_count = len(df_sorted[(df_sorted['Accuracy (%)'] >=40) & (df_sorted['Accuracy (%)'] < 60)]) / len(df_sorted) * 100

# 打印结果
# print(f"Accuracy 80 and above: {accuracy_80_plus_count:.2f}%")
print(f"Accuracy between 60 and 80: {accuracy_60_80_count:.2f}%")