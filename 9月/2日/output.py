import pandas as pd
import json

# 假设你的Excel文件路径为 "questions.xlsx"
excel_file = r"C:\Users\admin\Documents\WeChat Files\wxid_9penqxgz08n121\FileStorage\File\2024-09\output.xlsx"

# 读取Excel文件
df = pd.read_excel(excel_file)


# 定义一个函数来解析JSON并提取title和document
def parse_json(json_str):
    try:
        data = json.loads(json_str)
        parsed_output = []
        for item in data:
            title = item.get("title", "")
            document = item.get("document", "")
            parsed_output.append({"title": title, "document": document})
        return parsed_output
    except json.JSONDecodeError:
        return []


# 对于每一行，解析右侧的JSON，并将其附加到表格中
for index, row in df.iterrows():
    # 假设右侧JSON在 "Output" 列
    json_str = row["Output"]
    parsed_data = parse_json(json_str)

    # 将解析后的数据写入新的列中
    df.at[index, "Parsed Output"] = str(parsed_data)

# 将结果保存到新的Excel文件
df.to_excel("parsed_output.xlsx", index=False)
