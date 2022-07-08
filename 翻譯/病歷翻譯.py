# 
# 參數:
# 
#   python ./病歷翻譯.py start end
#   i: [start,end)
# 

import sys
import pandas as pd
from googletrans import Translator
import re
from tqdm import trange


def containalpha(s):
    return bool(re.search('[a-z]', s))
    

# 建立DataFrame
df_symtom = pd.read_csv('./不重複病歷_翻譯.csv', dtype={'主訴': str, '客觀': str, '中文主訴': str, '中文客觀': str}, engine='python')  # dtype指定型別無效，之後須強制轉型
new_df_symtom = df_symtom
n_rows, n_cols = new_df_symtom.shape
# df_symtom.info()


# Translator
translator = Translator()
start = int(sys.argv[1])
end = min(int(sys.argv[2]), n_rows)
try:
    for i in trange(start,end):
        if containalpha(str(df_symtom.at[i,'主訴'])):  # 包含英文字母
            if str(df_symtom.at[i,'主訴']).replace(' ','') != '':
                result1 = translator.translate(df_symtom.at[i,'主訴'], src='en', dest='zh-tw')
                new_df_symtom.at[i,'中文主訴'] = result1.text
            if str(df_symtom.at[i,'客觀']).replace(' ','') != '':
                result2 = translator.translate(df_symtom.at[i,'客觀'], src='en', dest='zh-tw')
                new_df_symtom.at[i,'中文客觀'] = result2.text
        else:  # 不包含英文，則不翻譯
            new_df_symtom.at[i,'中文主訴'] = df_symtom.at[i,'主訴']
            new_df_symtom.at[i,'中文客觀'] = df_symtom.at[i,'客觀']
finally:
    new_df_symtom.to_csv('./不重複病歷_翻譯.csv', index=False)



