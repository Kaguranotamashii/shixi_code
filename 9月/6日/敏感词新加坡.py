import requests
import json
import websocket
import openpyxl

# 创建Excel文件
wb = openpyxl.Workbook()
ws = wb.active
ws.append(["Question", "Documents", "AnswerId", "Event Name", "Event Summary", "Organization", "Description"])

# 基本配置信息
session_id = "e82ab5f1-19e5-4247-bca2-715b78131ff5"
page = "souyisou"
topic = "remote"
answer=""
q_lang = "新加坡"
a_lang = "中文"


documents_content=""
event_data = ""
org_data = ""
# 读取words.txt中的问题
with open("words.txt", "r", encoding="GBK") as file:
    questions = file.readlines()

# 遍历每个问题，发送请求并处理响应
for question in questions:
    question = question.strip()
    print(f"Processing question: {question}")
    # 发送第一个GET请求
    url_search = "https://search-dev.ssk.ai/web/api/search"
    params_search = {
        "question": question,
        "sessionId": session_id,
        "page": page,
        "topic": topic,
        "q_lang": q_lang,
        "a_lang": a_lang
    }
    response_search = requests.get(url_search, params=params_search)
    data_search = response_search.json()

    if data_search.get("code") == 200:
        documents = data_search["data"].get("documents", [])
        answer_id = data_search["data"].get("answerId", "")

        #到这里直接就是敏感内容了直接打断下面的
        if not documents and not answer_id:
            answer=data_search["data"].get("answer", "")
            event_data = ""
            org_data = ""
            documents_content=""
            print(documents_content)
        else:
            # 提取文档内容
            documents_content = "\n".join([f'{doc["title"]}: {doc["document"]}' for doc in documents])

            # 发送第二个GET请求 (event extraction)
            url_event = "https://search-dev.ssk.ai/web/api/eventExtraction"
            params_event = {
                "answerId": answer_id
            }
            response_event = requests.get(url_event, params=params_event).text
            #{"errCode":0,"errMsg":"success","data":[{"情感分析":"中性","事件类型":"游戏更新","时间":"5.0版本发布时","概括":"《原神》发布全新5.0版本「荣花与炎日之途」，提供新的游戏内容和体验。","来源":"[citation:1]","事件名称":"《原神》5.0版本更新"},{"情感分析":"中性","事件类型":"游戏介绍","时间":"不详","概括":"《原神》是一款开放世界冒险RPG，由米哈游开发，玩家在名为「提瓦特」的幻想世界中探索。","来源":"[citation:4][citation:5]","事件名称":"《原神》游戏概述"},{"情感分析":"中性","事件类型":"游戏制作","时间":"2017年1月底立项","概括":"《原神》由上海米哈游网络科技股份有限公司制作发行，项目于2017年1月底立项。","来源":"[citation:5]","事件名称":"《原神》项目立项"},{"情感分析":"中性","事件类型":"百科词条","时间":"不详","概括":"元神是道家修炼术语，代表通过修炼形成的独立存在，与灵魂和内丹术概念类似。","来源":"[citation:2][citation:3]","事件名称":"元神概念解释"},{"情感分析":"中性","事件类型":"游戏云化","时间":"不详","概括":"《云·原神》是米哈游推出的云游戏版本，利用实时云端技术，无需下载完整游戏即可体验《原神》。","来源":"[citation:8]","事件名称":"《云·原神》云游戏版本发布"}]}
            data_event = json.loads( response_event)


            # data_event = response_event.json()


            if data_event.get("errCode") == 0:
                event_data = "\n".join([f'{event["事件名称"]}: {event["概括"]}' for event in data_event["data"]])

            # 发送第三个GET请求 (entity extraction)
            url_entity = "https://search-dev.ssk.ai/web/api/entityExtraction"
            params_entity = {
                "answerId": answer_id
            }
            response_entity = requests.get(url_entity, params=params_entity)
            data_entity = response_entity.json()

            if data_entity.get("errCode") == 0:
                if data_entity.get("data") is not None and isinstance(data_entity["data"], dict):
                    if "orgnization" in data_entity["data"]:
                        org_data = "\n".join(
                            [f'{org["机构名称"]}: {org["描述"]}' for org in data_entity["data"]["orgnization"]]
                        )
                    else:
                        org_data = ""
                else:
                    org_data = ""

            # 写入Excel
        ws.append([question, answer,documents_content, event_data, org_data])




    else:
        print(f"Failed to process question: {question}")

# 保存Excel文件
wb.save(f"output{q_lang}.xlsx")
