'''
需先登入中醫養生系統，進入 中醫辨證 > 中醫症狀詞庫 > 原始症狀維護
點擊"已定義症狀"，查看資料總筆數
執行時需輸入要取得的詞庫資料筆數
存檔於"系統詞庫.csv"
'''

import re
import time
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


hostname = 'https://zeus.cs.ccu.edu.tw:8443'
login_url = 'https://zeus.cs.ccu.edu.tw:8443/tcm_latest/login.do'
username = 'lab202202'
password = 'lab202202'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}
payload = {
    'username': username,
    'password': password,
}

# login
session = requests.Session()
result = session.post(login_url, headers=headers, data=payload)
time.sleep(1)
# print(result.text)

# 取得詞庫url並GET
soup = BeautifulSoup(result.text,'html.parser')
sel = soup.select('ul.dropdown-menu a')
url = ''
for s in sel:
    if s.text == '中醫症狀辭庫2.0':
        url = hostname + s['href']
result2 = session.get(url, headers=headers)
time.sleep(1)
# print(result2.text)

# 進入'原始症狀維護'
soup = BeautifulSoup(result2.text,'html.parser')
sel = soup.select('ul.nav a')
for s in sel:
    if s.text == '原始症狀維護':
        url = hostname + s['href']
result3 = session.get(url, headers=headers)
time.sleep(1)
# print(result3.text)

# 取得"已定義症狀"的資料
allow_input = False
if allow_input:
    count = str(input('請輸入查詢筆數:'))
else:
    count = 63136
request_payload = {"page": "1", "count": count, "action": "FatchSymptomsMappingData", "table": "MappingData"}
result4 = session.post(url, headers=headers, json=request_payload)
time.sleep(1)
# print(result4.text)

# save as 系統詞庫.csv
result4_dict = json.loads(result4.text) # to dictionary
symptom_table_dict = {}
for i in range(len(result4_dict['data'])): # result4_dict['data'] is a list
    symptom_table_dict[i] = {
        '原始症狀': result4_dict['data'][i]['original_symptoms'],
        '標準症狀': result4_dict['data'][i]['standard_symptoms'],
    }
symptom_table_df = pd.DataFrame.from_dict(symptom_table_dict, orient='index')
print(symptom_table_df)
symptom_table_df.to_csv('./系統詞庫.csv')


