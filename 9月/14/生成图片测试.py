import requests
import base64
from pathlib import Path

# API的URL
url = 'http://192.168.2.5:8181/api/pictureDownload'

# 参数列表
types = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
contents = ['男人','女人','白头发老人','跑步的男人','小狗','沙滩','小孩','两个小孩','游泳的男人']  # 这里填写你的内容数组
heights = [256,512,1024,2048]  # 这里填写你的高度数组
widths = [256,512,1024,2048]  # 这里填写你的高度数组
counts = [1]  # 这里填写你的计数数组

# 遍历所有参数组合
for type_ in types:
    for content in contents:
        for height in heights:
            for width in widths:
                for count in counts:
                    # 构造请求体
                    params = {
                        'type': type_,
                        'content': content,
                        'height': height,
                        'width': width,
                        'count': count
                    }

                    # 发送POST请求
                    response = requests.post(url, params=params)

                    # 检查响应状态码
                    if response.status_code == 200:
                        # 解析响应内容
                        response_data = response.json()
                        if response_data['code'] == 200 and 'data' in response_data:
                            data = response_data['data']
                            for i, img_base64 in enumerate(data):
                                # 解码base64图片数据
                                img_data = base64.b64decode(img_base64)

                                # 定义一个字典，将类型代码映射到对应的类型名称
                                type_mapping = {
                                    'a': '人像摄影',
                                    'b': '风景',
                                    'c': '动漫',
                                    'd': '3D',
                                    'e': '赛博朋克',
                                    'f': '油画',
                                    '9': '水彩画',
                                    'h': '儿童绘画',
                                    'i': '水墨画'

                                }




                                # 使用字典映射来获取对应的类型名称
                                if type_ in type_mapping:
                                    type__ = type_mapping[type_]
                                else:
                                    type__ = '未知类型'  # 如果类型代码不在字典中，设置为'未知类型'

                                # 打印结果
                                print(type__)




                                # 构造图片文件名
                                img_name = f"{content}_{type__}{height}x{width}.png"
                                # 构造图片保存路径
                                img_path = Path(content) / img_name
                                # 确保目录存在
                                img_path.parent.mkdir(parents=True, exist_ok=True)
                                # 保存图片到文件
                                with open(img_path, 'wb') as img_file:
                                    img_file.write(img_data)
                                print(f"Image saved: {img_path}")
                        else:
                            print("Failed to get image data.")
                    else:
                        print(f"Request failed with status code: {response.status_code}")