import os
import requests
import pandas as pd

# 文件夹路径
folder_path = r'C:\Users\admin\PycharmProjects\pythonProject1\8\21\wav1'  # 替换为音频文件的文件夹路径
save_folder = r'C:\Users\admin\PycharmProjects\pythonProject1\8\21\out'  # 替换为保存处理后音频的文件夹路径
excel_file = "audio_links-shuzi_zimu.xlsx"  # Excel 文件的保存路径
TEST_TEXT= [
    '1,2,3,4,5,6,7,8,9,0',
    'I am a student.',
    'I am a student.',
    'a,b,c,d,e,f,g, q,w,e,r,t,y,u,i,o,p,a,s,d,f,g,h,j,k,l,z,x,c,v,b,n,m',
    '1234',
    '1234512343',
    'abcdefg',
    'dqwd1',
    '231r423f23ed3',
    'back',
    'good'

]
wav=[
    '新民路.wav',
    '小兔子.wav',
    '10秒英文.wav'
]
# 确保保存文件夹存在
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 创建一个列表来存储音频文件名和相对链接
data = []
i=0
# 遍历文件夹中的所有音频文件
for file_name in wav:
    file_name1 = file_name
    if file_name.endswith(".wav"):
        # 获取音频文件路径
        file_path = os.path.join(folder_path, file_name)
        for test in TEST_TEXT:
            file_name=file_name1
            file_name = file_name.replace(".wav", "")
            file_name = file_name + test + '.wav'


            # 第一个请求：上传音频文件
            with open(file_path, 'rb') as audio_file:
                # files = {'file': audio_file}
                # upload_response = requests.post("http://47.57.14.198:8020/upload", files=files)
                # print(f"文件 {file_name} 上传成功.")
                # 将这个字符串的前六位字符截断，然后最后四位字符也截断
                # file_name = file_name[:6] + file_name[-4:]
                # 截断前六位字符
                # file_name1 = file_name[6:]
                # print(f"文件 {file_name} 上传成功.")
                # 截断最后四位字符
                # file_name1 = file_name[:-4]
                # 第二个请求：发送 GET 请求获取处理后的音频

                tts_response = requests.get("http://47.57.14.198:8020/tts",
                                            params={'text': test, 'name': file_name1})

                if tts_response.status_code == 200:
                    # 保存处理后的音频文件
                    processed_file_path = os.path.join(save_folder, f"processed_{file_name}")
                    with open(processed_file_path, 'wb') as processed_file:
                        processed_file.write(tts_response.content)
                    print(f"文件 {processed_file_path} 已保存.")

                    # 创建音频文件的相对超链接（假设 Excel 和音频文件夹在同一层级）
                    relative_link = os.path.join(save_folder, f"processed_{file_name}")
                    excel_link = f'=HYPERLINK("{relative_link}", "Play Audio")'

                    # 将文件名和相对路径的音频超链接添加到数据列表中
                    data.append([file_name + test, excel_link])
                    i = i + 1
                else:
                    print(f"获取处理后音频失败: {tts_response.status_code}")
                    data.append([file_name, "获取失败"])

# 创建 DataFrame 并保存为 Excel 文件
df = pd.DataFrame(data, columns=["原始音频文件名", "音频链接"])

# 使用 openpyxl 写入 Excel 文件并保持公式的正确性
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='音频链接')

print(f"Excel 文件已保存至 {excel_file}.")
