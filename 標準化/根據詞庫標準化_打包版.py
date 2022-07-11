import collections
from os import write
import pandas as pd
from tqdm import tqdm as tq
import re
import ahocorasick as ac
drop_L=['仍', '仍會', '仍會有', '會有', '有'
, '會', '稍', '稍微', '稍有', '部', '即會有'
, '即', '亦', '作', '未改善','又','偶','約']

def standard(sentence):
    global end,total,total_ch,symtom_num_total_dic
    progress.update(1)
    string=''
    #計算字數
    total+=len(sentence)
    #計算中文字數
    total_ch+=len(rule.sub('',sentence))
    #for D in drop_L:
    #    sentence=sentence.replace(D,'')
    #print(sentence)
###################AC######################
    dic_simple={}
    #以AC自動機，計算簡化版的dic並排列
    for sym in AC.iter(sentence):
        #i是有可能的原始症狀，格式為tuple(index,原始症狀)
        dic_simple[sym[1][0]]={
            '詞':sym[1][1],
        }
    dic_simple={k:v for k, v in sorted(dic_simple.items(), key=lambda item: len(item[1]['詞']), reverse=True)}
##########################################
    for ind in dic_simple:
        #根據ind，將原始症狀取出
        s=dic_dict['詞'][ind]
        if(s in sentence):
            #完成字數
            end+=len(s)
            #症狀句
            # sentence = sentence.replace(s,'_')
            std=dic_dict['標準症狀'][ind]
            string=string+std
    sym_list=list(set(string.split('。')[:-1]))
    string='。'.join(sym_list)+'。'
    # for sym in sym_list:
    #     symtom_num_total_dic[sym]=symtom_num_total_dic.get(sym,0)+1
    #sentence=rule.sub('',sentence)
    #sentence=rule2.sub('',sentence)
    return string,sentence

# def ICD(S):
#     global ICD_num
#     if('/' in S):
#         for icd in S.split('/'):
#             try:
#                 FL=float(icd)
#                 if(FL>=530 and FL <580):
#                     ICD_num+=1
#                     return
#             except:
#                 pass

#re規則編譯
rule = re.compile(u"[^\u4e00-\u9fa50-9０-９]")
rule2 = re.compile(u'[0-9０-９]{3,}')

#讀詞庫，前處理
df_dic=pd.read_csv('./系統詞庫.csv',index_col=0)
df_dic.rename(columns={'原始症狀':'詞'}, inplace=True)
df_dic['詞長度']=df_dic[['詞']].applymap(lambda x: len(str(x)))
df_dic['詞']=df_dic['詞'].str.replace('痠','酸')
df_dic['詞']=df_dic['詞'].str.replace('饑','飢')
df_dic['詞']=df_dic['詞'].str.replace('粘','黏')
df_dic['詞']=df_dic['詞'].str.replace('后','後')
df_dic['詞']=df_dic['詞'].str.replace('糢','模')
df_dic['詞']=df_dic['詞'].str.replace('曨','嚨')
df_dic['詞']=df_dic['詞'].str.replace('溼','濕')
df_dic['詞']=df_dic['詞'].str.replace('脕','脘')
df_dic['詞']=df_dic['詞'].str.replace('炫','眩')
df_dic['詞']=df_dic['詞'].str.replace('食欲','食慾')
df_dic['詞']=df_dic['詞'].str.replace('性慾','性欲')
df_dic['詞']=df_dic['詞'].str.replace('癡','痴')
df_dic.to_csv('./系統詞庫.csv')
# #讀五群症狀庫，前處理
# df_symtom=pd.read_csv('./資料/五群症狀轉換表.csv',converters={'同義症狀':eval})
# print(df_symtom.info())
# symtom_num_dic=dict.fromkeys(df_symtom['五群症狀'].to_list(),0)
# symtom_num_total_dic=dict.fromkeys(df_symtom['五群症狀'].to_list(),0)
#for D in drop_L:
#    df_dic.replace(D,'',inplace=True)
##df_all=pd.read_csv('./查詢結果/消化系統疾病.csv',index_col=0,dtype=str)
#df_all=pd.read_csv('./標準化/全set流水序.csv',index_col=0,dtype=str)
df_all=pd.read_csv('./不重複病歷_翻譯.csv',index_col=0,dtype=str,engine='python')
##df_all=pd.read_csv('./全set病歷序.csv',index_col=0,dtype=str)
################################
print('去重複')
df_all.fillna('',inplace=True)
df_all = df_all.drop_duplicates(subset=['病歷號','生日','性別'],keep='first')
#df_all = df_all.sort_values(by=['病歷號','生日']).drop_duplicates(subset=['病歷號','生日'])
df_all=df_all[df_all['性別']!='']
#df_all=df_all[df_all['生日']!='']
df_all['中文症狀和']=df_all['中文主訴']+df_all['中文客觀']
df_all=df_all.drop(columns=['中文主訴','中文客觀'])
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('痠','酸')
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('饑','飢')
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('粘','黏')
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('后','後')
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('糢','模')
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('曨','嚨')
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('溼','濕')
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('脕','脘')
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('炫','眩')
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('食欲','食慾')
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('性慾','性欲')
df_all['中文症狀和']=df_all['中文症狀和'].str.replace('癡','痴')
print(df_all.info())
##df_all.drop_duplicates(subset=['病歷號'],inplace=True)
#####################################################
# df_dic.sort_values(by=['長度'],ignore_index=True,inplace=True,ascending=False)
df_dic.fillna('',inplace=True)
dic_dict=df_dic.to_dict()  # {column -> {index -> value}}
AC = ac.Automaton()
print(df_dic.info())
for ind in df_dic.index:
    w=df_dic.at[ind,'詞']
    AC.add_word(w,(ind,w))
AC.make_automaton()
#df_all.fillna('0',inplace=True)
progress=tq(total=len(df_all.index))
end=0
total=0
total_ch=0

#print(df_all.head(1))
df_all['標準症狀t']=df_all['中文症狀和'].apply(standard)
df_all['標準症狀']=df_all['標準症狀t'].apply(lambda t:t[0])
# df_all['剩餘句']=df_all['標準症狀t'].apply(lambda t:t[1])
df_all.drop(columns=['標準症狀t'],inplace=True)
# df_all['剩餘字數']=df_all['剩餘句'].apply(lambda s:len(s))
len_std_total=0
for std_s in df_all['標準症狀'].to_list():
    for sen in std_s:
        len_std_total += len(sen)
print(len_std_total)
print('完成度:',end,'/',total,round(end/total,2))
print('中文完成度:',end,'/',total_ch,round(end/total_ch,2))
##df_all.to_csv('消化系統標準化.csv')
##df_all.to_csv('全病歷標準化.csv')

df_all.to_csv('./不重複標準化.csv')
df_all.sort_values(by=['流水號'])
# df_all[df_all['剩餘字數']==0].to_csv('./完全標準化病歷.csv')
# #將統計後的症狀次數移到dictionary中
# for sym in symtom_num_dic.keys():
#     symtom_num_dic[sym]=symtom_num_total_dic.get(sym,0)
# writer = pd.ExcelWriter('./統計結果/標準化紀錄.xlsx', engine='xlsxwriter')
# df_num=pd.DataFrame.from_dict(symtom_num_dic,'index',columns=['次數'])
# total=df_num['次數'].sum()
# df_num['佔比']=df_num['次數'].apply(lambda x:round(x/total,4))
# df_num.sort_values(by=['次數'],ascending=False,inplace=True)
# df_num.to_excel(writer,sheet_name='五群症狀次數')
# df_num=pd.DataFrame.from_dict(symtom_num_total_dic,'index',columns=['次數'])
# total=df_num['次數'].sum()
# df_num['佔比']=df_num['次數'].apply(lambda x:round(x/total,4))
# df_num.sort_values(by=['次數'],ascending=False,inplace=True)
# df_num.to_excel(writer,sheet_name='所有症狀次數')
# df_num.to_csv('./各種紀錄/標準化症狀次數.csv')
# worksheet = writer.sheets['五群症狀次數']
# worksheet.set_column('A:A',16)
# worksheet = writer.sheets['所有症狀次數']
# worksheet.set_column('A:A',20)
# writer.save()
#########################
# ICD_num=0
# df_all['診斷'].apply(ICD)
# print('消化系統總數',ICD_num)
