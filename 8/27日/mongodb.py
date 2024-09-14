from pymongo import MongoClient

# 连接到MongoDB服务器
client = MongoClient('mongodb://root:song111711@124.222.202.20:27017/')

# 选择数据库
db = client['mydatabase']

# 选择集合（类似于SQL中的表）
collection = db['mycollection']

# 插入一条文档（类似于SQL中的记录）
document = {
    "name": "Alice",
    "age": 25,
    "email": "alice@example.com"
}

# 插入文档到集合中
insert_result = collection.insert_one(document)
print(f"Inserted document ID: {insert_result.inserted_id}")

# 查询集合中的所有文档
documents = collection.find()
for doc in documents:
    print(doc)

# 关闭连接
client.close()