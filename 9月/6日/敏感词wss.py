import requests
import websocket
import time
import json
import openpyxl

# 配置文件路径和固定参数
file_path = "words.txt"
session_id = "e82ab5f1-19e5-4247-bca2-715b78131ff5"
page = "souyisou"
topic = "remote"
q_lang = ""
a_lang = "中文"

# 结果保存到Excel
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Results"
sheet.append(["Question", "Documents", "AnswerId", "Event Names", "Event Summary", "Organizations", "Descriptions"])

# 读取文件中的每一行问题
with open(file_path, 'r', encoding='GBK') as file:
    questions = file.readlines()

# 遍历每个问题
for question in questions:
    question = question.strip()
    # 步骤1：发送搜索请求
    search_url = "https://search-dev.ssk.ai/web/api/search"
    search_params = {
        "question": question,
        "sessionId": session_id,
        "page": page,
        "topic": topic,
        "q_lang": q_lang,
        "a_lang": a_lang
    }
    search_response = requests.get(search_url, params=search_params).json()

    if search_response['code'] == 200:
        documents = search_response['data'].get('documents', [])
        answer_id = search_response['data'].get('answerId', "")
        doc_titles = "\n".join([doc['title'] for doc in documents])
    else:
        continue  # 跳过失败的请求

    # 步骤2：发送WS初始化请求获取sid
    ws_init_url = "https://search-dev.ssk.ai/ws/"
    ws_init_params = {
        "sessionId": session_id,
        "answerId": answer_id,
        "EIO": 4,
        "transport": "polling",
        "t": "P76AFZS"
    }
    # 生成带有占位符的 URL
    # url_with_placeholders = f"https://search-dev.ssk.ai/ws/?sessionId=session_id_value&answerId=answer_id_value&EIO=4&transport=polling&t=P76AFZS"

    ws_init_response = requests.get(ws_init_url, params=ws_init_params)
    ws_init_response.raise_for_status()  # 检查请求是否成功

    sid = json.loads(ws_init_response.text[1:])['sid']

    # 步骤3：通过WebSocket获取chunk内容
    ws_url = f"wss://search-dev.ssk.ai/ws?sessionId={session_id}&answerId={answer_id}&EIO=4&transport=websocket&sid={sid}"
    print(ws_url)
    ws = websocket.WebSocket()
    ws.connect(ws_url)

    # 监听WebSocket消息，提取chunk内容
    while True:
        message = ws.recv()
        if 'chunk' in message:
            data = json.loads(message[1:])  # WebSocket消息前有一位额外字符
            if data.get('end', False):
                break
            chunk = data.get('chunk', "")
            # 保存答案信息...
        else:
            break
    ws.close()

    # 步骤4：事件提取
    event_extraction_url = "https://search-dev.ssk.ai/web/api/eventExtraction"
    event_extraction_params = {"answerId": answer_id}
    event_extraction_response = requests.get(event_extraction_url, params=event_extraction_params).json()
    if event_extraction_response.get('errCode') == 0:
        events = event_extraction_response['data']
        event_names = "\n".join([event['事件名称'] for event in events])
        event_summaries = "\n".join([event['概括'] for event in events])
    else:
        event_names = event_summaries = ""

    # 步骤5：实体提取
    entity_extraction_url = "https://search-dev.ssk.ai/web/api/entityExtraction"
    entity_extraction_params = {"answerId": answer_id}
    entity_extraction_response = requests.get(entity_extraction_url, params=entity_extraction_params).json()
    if entity_extraction_response.get('errCode') == 0:
        organizations = entity_extraction_response['data']['orgnization']
        org_names = "\n".join([org['机构名称'] for org in organizations])
        org_descriptions = "\n".join([org['描述'] for org in organizations])
    else:
        org_names = org_descriptions = ""

    # 将提取结果保存到Excel
    sheet.append([question, doc_titles, answer_id, event_names, event_summaries, org_names, org_descriptions])

# 保存最终Excel
workbook.save("result.xlsx")
