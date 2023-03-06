# import re

# def remove_postal_code(address):
#     m = re.search(r'(市|区|町|村)', address[4:])
#     if m:
#         index = m.start() + 5
#         print(index)
#         return address[:index]
#     else:
#         return address

# address = "東京都港区品川区"
# new_address = remove_postal_code(address)
# print(new_address)  # "東京都港区"



# モジュールのインポート
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools # 2次元リストを1次元化
 
# 凝縮型の階層的クラスタリング
from sklearn.cluster import AgglomerativeClustering
# デンドログラム（樹形図）の作成
from scipy.cluster.hierarchy import dendrogram
 
# # 高解像度ディスプレイのための設定
# from IPython.display import set_matplotlib_formats
# # from matplotlib_inline.backend_inline import set_matplotlib_formats # バージョンによってはこちらを有効に
# set_matplotlib_formats('retina')

import unicodedata
from janome.tokenizer import Tokenizer
import sqlite3
import os
import re


# SQLITEに接続
os.chdir('../')
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()



# 市区町村までを取得する関数
def remove_postal_code(address):
    m = re.search(r'(市|区|町|村|郡)', address[4:])
    if m:
        index = m.start() + 5
        return address[:index]
    else:
        return address


      
# 職種と勤務地でグルーピング
cursor.execute('''
            SELECT title, id, job, location FROM aggggry_app_jobs
                ''')
result = cursor.fetchall()

columns_group = ['ID', '職種名', '勤務地']
data_group = np.empty((0,3))
# １レコードごとに取得して勤務地を整形し、data_groupに格納
for r in result:
    r = list(r)[1:]
    r[2] = remove_postal_code(r[2]) # 勤務地を整形
    data_group = np.append(data_group, np.array([r]), axis=0)
# 職種✖勤務地で一意のデータフレームを作成
df_group = pd.DataFrame(data_group, columns=columns_group)
df_group = df_group.groupby(['職種名', '勤務地'], as_index=False).count()



# IDに対してグループIDをラベリング
columns_label1 = ['タイトル', 'ID', 'ラベル１']
data_label1 = np.empty((0,3))
# １レコードごとに取得してdf_groupの情報と比較してグループIDをラベリング。その情報をdata_label1に格納。
for r in result:
    r = list(r)
    job = r[2]
    location = r[3]
    r.append('null') #ラベル１の列を作成
    for index, row in df_group.iterrows():
        if job==row['職種名'] and location==row['勤務地']:
            r[4] = index #ラベル１の列にdf_groupのインデックスを格納
    r.pop(2) # 職種列を削除
    r.pop(2) # 勤務地列を削除
    data_label1 = np.append(data_label1, np.array([r]), axis=0)
# 全レコードのタイトル、ID、ラベル１（職種✖勤務地）のデータフレーム作成
df_label1 = pd.DataFrame(data_label1, columns=columns_label1) 
print(df_label1)



# グループごとにデータを取得してクラスタリング


  





