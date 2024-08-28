from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
import urllib
import subprocess
import urllib.parse

# 建立一個 Flask 應用程式
app = Flask(__name__)


# 設置資料庫連接 URL
server = r'userTwhs\SQLEXPRESS'
database = 'stockinformation'
username = 'testaccount'
password = 'Ab1234!?'
params = urllib.parse.quote_plus(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc:///?odbc_connect={params}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy 對象
db = SQLAlchemy(app)


# 定義一個路徑(/)
@app.route('/')
def home():
    # 重新定向回首頁面
    return redirect(url_for('index'))


# 定義一個路徑(/index)
@app.route('/index')
def index():
    return render_template('index.html')


# 定義一個路徑(/run_script)
@app.route('/run_script', methods=['POST'])
def run_script():
    # 執行外部 Python 檔案
    subprocess.run(['python', 'catch_ETF_volume.py'], capture_output=True, text=True)
    # 捕獲並返回腳本的輸出
    return render_template('result.html')


# 定義一個路徑(/back)
@app.route('/back', methods=['POST'])
def back():
    # 重新定向回首頁面
    return redirect(url_for('index'))


# 定義一個路徑(/to_volume)
@app.route('/to_volume', methods=['POST'])
def to_volume():
    # 定向至volume頁面
    return redirect(url_for('volume'))


# 定義一個路徑(/volume)
@app.route('/volume')
def volume():
    # 獲取所有資料表名稱
    inspector = inspect(db.engine)
    dates = inspector.get_table_names()
    dates = [name.replace('ETF排行', '') for name in dates]
    return render_template('volume.html', dates=dates)


# 定義一個路徑(/data)
@app.route('/data', methods=['POST'])
def data():
    # 獲取所有資料表名稱
    inspector = inspect(db.engine)
    dates = inspector.get_table_names()
    dates = [name.replace('ETF排行', '') for name in dates]
    # 獲取選單送出的值
    table_name = request.form.get('tables')
    # 設定SQL查詢語句並執行
    quary = text(f'SELECT * FROM [ETF排行{table_name}]')
    result = db.session.execute(quary).fetchall()
    # 設定欄位名稱
    columns = ['日期', '排名', '股名', '股號', '股價', '最高', '最低', '價差', '成交量(張)']

    return render_template('data.html', dates=dates, table_name=table_name, columns=columns, rows=result)


# 確保程式直接執行時啟動伺服器
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
