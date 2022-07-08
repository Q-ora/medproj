import pandas as pd

# 建立DataFrame
df_symtom = pd.read_csv('./不重複病歷.csv')
new_df_symtom = df_symtom
new_df_symtom['中文主訴'] = ''
new_df_symtom['中文客觀'] = ''
new_df_symtom.to_csv('./不重複病歷_翻譯.csv', index=False)