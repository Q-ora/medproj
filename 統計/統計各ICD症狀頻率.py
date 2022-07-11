import os
import pandas as pd


def frequency(std_symtom):
    global syd_dict
    std_symtom_list = [s for s in std_symtom['標準症狀'].split('。') if s != '']
    for syd in std_symtom_list:
        if syd not in syd_dict:
            syd_dict[syd] = [1, 0] # [次數, 占比]
        else:
            syd_dict[syd][0] += 1

# 建立目錄存放每個表格
# 目錄名: ICD9
dirpath = './ICD9'
if os.path.isdir(dirpath):
    print('目錄已存在:' + dirpath)
else:
    os.mkdir(dirpath)

homedir = '../建表/ICD9/'
for filename in os.listdir(homedir):
    df_symtom = pd.read_csv(os.path.join(homedir, filename), engine='python')

    # 檢查該ICD的病歷數是否超過100，有超過100才統計症狀次數
    if len(df_symtom.index) < 100:
        continue

    # 統計病歷中所有有出現的症狀的次數
    syd_dict = {}
    df_symtom[['標準症狀']].apply(frequency, axis=1)
    # 計算占比
    n = sum(v[0] for k, v in syd_dict.items())
    for syd in syd_dict.keys():
        syd_dict[syd][1] = syd_dict[syd][0] / n
        syd_dict[syd][1] = round(syd_dict[syd][1], 4)

    print('=========================', filename, '=========================', sep='')
    sorted_syd_list = sorted(syd_dict.items(), key=lambda x: x[1][0], reverse=True)
    sorted_syd_list = [(x,y,z) for x,[y,z] in sorted_syd_list]
    for syd, times, freq in sorted_syd_list:
        print(syd, ': ', times, ', ', freq, sep='')
    sorted_syd_df = pd.DataFrame(sorted_syd_list, columns=['標準症狀','次數','占比'])
    sorted_syd_df.to_csv(os.path.join(dirpath, filename), index=True)
