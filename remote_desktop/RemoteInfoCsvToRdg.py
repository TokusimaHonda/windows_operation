# coding: utf-8
import os
import glob
import sys
import pandas as pd
import pathlib

#このファイルのパス
current_file_path = os.path.dirname(os.path.abspath(__file__))

#rdgのひな型ファイルを読み込み
txt_header_hinagata = open(os.path.join(current_file_path,"rdg_hinagata/rdg_hinagata_header.txt"),'r')
contents_header_hinagata = txt_header_hinagata.read()
txt_header_hinagata.close

txt_main_hinagata = open(os.path.join(current_file_path,"rdg_hinagata/rdg_hinagata_main.txt"),'r')
contents_main_hinagata = txt_main_hinagata.read()
txt_main_hinagata.close

txt_footer_hinagata = open(os.path.join(current_file_path,"rdg_hinagata/rdg_hinagata_footer.txt"),'r')
contents_footer_hinagata = txt_footer_hinagata.read()
txt_footer_hinagata.close


#引数にフォルダを指定する。
args = sys.argv
if(len(args)>1):
    #csv_dir_path = repr(args[1])
    csv_dir_path = pathlib.WindowsPath(repr(args[1]))
else:
    #テスト用パス
    csv_dir_path = pathlib.WindowsPath(r"\\Server0001\Dir01\yyyymm_all")


"""
CSV情報
1列目：対象サーバIPアドレス
2列目：ユーザID　（domain\mntadm01-mig**）
3列目：パスワード
4列目：サーバ名
"""

csv_list = sorted(csv_dir_path.glob('*.csv'))
for csv_file in csv_list:
    #CSVを読み込み
    df = pd.read_csv(csv_file,engine='python',names=('IP','login_id','password','srvname'))

    #ヘッダーとフッターのひな型を読み込み置換
    contents_header_replace = contents_header_hinagata
    contents_header_replace = contents_header_replace.replace("**ServerGr**",csv_file.stem)
    contents_footer_replace = contents_footer_hinagata
    
    #メインのひな型を読み込み置換
    contents_main_merge = ""
    for index,row in df.iterrows():
        replace_displayname = ""
        replace_ip = row['IP']
        replace_domain = str(row['login_id']).split("\\")[0]
        replace_username = str(row['login_id']).split("\\")[1]
        replace_password = row['password']

        replace_srvname = str(row['srvname']).split("-")[1]
        replace_displayName = str(row['srvname']).split("-")[1] + "_" + replace_username
        
        
        
        contents_main_replace = contents_main_hinagata
        contents_main_replace = contents_main_replace.replace("**displayName**",replace_displayName).replace("**IP**",replace_ip).replace("**USERNAME**",replace_username).replace("**PASSWORD**",replace_password).replace("**DOMAIN**",replace_domain)
        contents_main_merge = contents_main_merge + contents_main_replace
    
    #マージ
    contents_rdg = contents_header_replace + contents_main_merge + contents_footer_replace
    
    #ファイル出力
    contents_rdg_path = (pathlib.Path(csv_file.parent)).joinpath(csv_file.stem + ".rdg")
    with open(contents_rdg_path,mode = 'w',encoding = 'shift-jis') as f:
        f.write(contents_rdg)
    

sys.exit()

