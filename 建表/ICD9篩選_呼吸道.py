import pandas as pd
from tqdm import tqdm
from tqdm import trange


df_symtom = pd.read_csv('./不重複病歷_翻譯.csv', dtype={'流水號': str, '診斷': str}, engine='python')  # dtype指定型別無效，之後須強制轉型
df_icd9 = pd.read_csv('./ICD9整數.csv', dtype={'ICD-9': str, '中文傷病名稱': str})

# 過濾掉'診斷'是NaN的病例
df_symtom = df_symtom[df_symtom['診斷'].notnull()]


# 篩選出具有呼吸道相關ICD9的病例
new_df_symtom = pd.DataFrame(columns=df_symtom.columns)
selected = pd.Series(False, index=df_symtom.index)
for i in trange(0, len(df_icd9.index)):
    idx = df_symtom['診斷'].str.contains(df_icd9.at[i,'ICD-9'])
    new_df_symtom = pd.concat([new_df_symtom, df_symtom[idx & ~(selected)]], ignore_index=True)   # 注意：須使用bitwise logical op, 否則會出錯
    selected = selected | idx


# 分出'診斷'中具有多個ICD9的病例
new_df_symtom['診斷'] = new_df_symtom['診斷'].str.split('/').replace(' ', '')   # 以斜線分割原字串, 並刪除空格, 得到icd9的list
df_symtom_singicd = pd.DataFrame(columns=df_symtom.columns)
df_symtom_multicd = pd.DataFrame(columns=df_symtom.columns)
for row, _ in tqdm(new_df_symtom.iterrows(), total=new_df_symtom.shape[0]):
    new_df_symtom.at[row,'診斷'] = ' '.join(list(filter(None, new_df_symtom.at[row,'診斷'])))  # 用filter去掉list內的空字串, 並將list轉為str
    if new_df_symtom.at[row,'診斷'].count(' ') < 1 :   # 單一icd
        df_symtom_singicd = pd.concat([df_symtom_singicd, new_df_symtom.iloc[[row]]], ignore_index=True)
    else:                                      # 多個icd
        df_symtom_multicd = pd.concat([df_symtom_multicd, new_df_symtom.iloc[[row]]], ignore_index=True)


#
# 篩選肺的所有病歷的'診斷'欄位的icd9已改成str list格式
#   "460/786.2///"  =>  "460 786.2"
# 
new_df_symtom.to_csv('./不重複病歷_篩選肺.csv', index=False)
df_symtom_singicd.to_csv('./不重複病歷_篩選肺_單ICD.csv', index=False)
df_symtom_multicd.to_csv('./不重複病歷_篩選肺_多ICD.csv', index=False)