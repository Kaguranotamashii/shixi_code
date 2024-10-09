import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def ping(ip):
    try:
        response = os.system(f"ping -n 1 {ip}")
        if response == 0:
            print(ip+"存在")
            return (ip, "在线")
        else:
            return (ip, "离线")
    except Exception as e:
        return (ip, "异常")

def main():
    # 创建一个空的DataFrame
    df = pd.DataFrame(columns=["IP地址", "状态"])

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for i in range(255):
            for j in range(255):
                ip = f"192.168.{i}.{j}"
                futures.append(executor.submit(ping, ip))

        results = []
        for future in futures:
            results.append(future.result())

        # 将结果添加到DataFrame
        for result in results:
            new_row = pd.DataFrame({"IP地址": [result[0]], "状态": [result[1]]})
            df = pd.concat([df, new_row], ignore_index=True)

    # 保存到Excel文件
    df.to_excel("ping_results.xlsx", index=False)
    print("Ping测试完成，结果已保存到ping_results.xlsx")

if __name__ == "__main__":
    main()