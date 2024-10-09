import openpyxl
from openpyxl.styles import Font

# 打开Excel文件
file_path = '123mgc.xlsx'  # 替换为你的Excel文件路径
workbook = openpyxl.load_workbook(file_path)
sheet = workbook.active

# 遍历每一行
for row in sheet.iter_rows(min_row=2, values_only=False):  # 假设第一行是表头，从第二行开始
    left_cell = row[0]  # 左边的单元格
    right_cell = row[1]  # 右边的单元格
    # 检查右边单元格的字体颜色是否为红色
    if left_cell.font.color==None:
        continue
    print(left_cell.font.color.rgb)
    if left_cell.font.color and left_cell.font.color.rgb == 'FFFF0000':  # 红色
        right_cell.value = '是'
    else:
        right_cell.value = '否'

# 保存修改后的Excel文件
workbook.save('123'+file_path)