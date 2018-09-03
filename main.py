import csv
from datetime import datetime


from flask import Flask, render_template, request

app = Flask(__name__)

# ファイル名
DATA_FILE = "memo.csv"
# 1ページの件数
ROWS_NUM_PER_PAGE = 10

def save_data(memo,created_at):
    """記録データを保存します
    :param memo: メモ
    :type memo: str
    :param created_at: 日時
    :type created_at:str
    :return: None
    """
    with open (DATA_FILE,mode='a',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([created_at,
                            memo])

def load_data():
    """記録データを返します"""
    result=[]
    with open (DATA_FILE,mode='r',encoding='utf-8')as csv_file:
        csv_reader=csv.DictReader(csv_file,
                                 fieldnames=['created_at','memo'])
        for row in csv_reader:
            result.append(dict(row))

    return result




@app.route("/", methods=['GET', 'POST'])
def index():
    res = {}

    if request.method=='POST':
        #メモが書かれている場合は記録する
        memo=request.form.get('memo','')
        if memo:
            created_at=datetime.now().strftime("%Y-%m-%d")
            save_data(memo,created_at)

    #入力値のファイルからの取り出し
    data=load_data()
    data=data[::-1]#逆順に変換

    #ページ番号取得
    page=int(request.args.get('page',1))
    res['page']=int(page)
    if page>1:
        res['previous_page']=page-1
    if page * ROWS_NUM_PER_PAGE <len(data):
        res['next_page']=page+1

    #開始行番号取得
    start_row_no = (page -1)* ROWS_NUM_PER_PAGE
    #ページ分のデータの取得
    res['list']=data[start_row_no: (start_row_no + ROWS_NUM_PER_PAGE)]

    return render_template('index.html', res=res)
if __name__ == '__main__':
    # プライベートIPアドレス192.168.33.10の8000番ポートでアプリケーションを実行します
    app.run('192.168.33.10', 8000, debug=True)
