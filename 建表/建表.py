import os
import pandas as pd


df_symtom = pd.read_csv('./不重複病歷_篩選肺_單ICD.csv', dtype={'流水號': str, '診斷': str}, engine='python')  # dtype指定型別無效，之後須強制轉型
df_icd9 = pd.read_csv('./ICD9整數.csv', dtype={'ICD-9': str, '中文傷病名稱': str})

# 建立目錄存放每個表格
# 目錄名: ICD9
dirpath = './ICD9'
if os.path.isdir(dirpath):
    print('目錄已存在:' + dirpath)
else:
    os.mkdir(dirpath)

print('ICD9: 病例數')
for i in range(0, len(df_icd9.index)):
    # 對每個呼吸道相關的整數ICD9建表
    icd9_num = str(df_icd9.at[i,'ICD-9'])
    idx = df_symtom['診斷'].str.contains(icd9_num)
    df_table = df_symtom[idx]
    filepath = dirpath + '/' + icd9_num + '.csv'
    df_table.to_csv(filepath, index=False)
    print(icd9_num + ': ' + str(len(df_table.index)))
