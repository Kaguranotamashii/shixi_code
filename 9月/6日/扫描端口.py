import nmap
import pandas as pd

# 创建 nmap 扫描器
nm = nmap.PortScanner()

# 扫描 IP 地址和端口范围
ip_address = '192.168.1.40'
nm.scan(ip_address, '1-999999')

# 初始化数据存储
data = []

# 解析扫描结果
for proto in nm[ip_address].all_protocols():
    ports = nm[ip_address][proto].keys()
    for port in ports:
        state = nm[ip_address][proto][port]['state']
        service = nm[ip_address][proto][port].get('name', 'unknown')
        data.append([proto, port, state, service])

# 将结果存储为 pandas DataFrame
df = pd.DataFrame(data, columns=['Protocol', 'Port', 'State', 'Service'])

# 将 DataFrame 保存为 Excel 文件
df.to_excel('port_scan_results.xlsx', index=False)

print("扫描完成，结果已保存到 port_scan_results.xlsx")
