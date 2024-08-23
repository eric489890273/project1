from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
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


# 定義一個路徑(/page/text)
@app.route('/page/text')
def pageText():
    return render_template('page.html', text="Python Flask !")


# 定義一個路徑(/page/app)
@app.route('/page/app')
def pageAppInfo():
    appInfo = {  # dict
        'id': 5,
        'name': 'Python - Flask',
        'version': '1.0.1',
        'author': 'Enoxs',
        'remark': 'Python - Web Framework'
    }
    return render_template('page.html', appInfo=appInfo)


# 定義一個路徑(/page/data)
@app.route('/page/data')
def pageData():
    data = {  # dict
        '01': 'Text Text Text',
        '02': 'Text Text Text',
        '03': 'Text Text Text',
        '04': 'Text Text Text',
        '05': 'Text Text Text'
    }
    return render_template('page.html', data=data)


# 定義一個路徑(/static)
@app.route('/static')
def staticPage():
    return render_template('static.html')


# 定義一個路徑(/index)
@app.route('/index')
def index():
    return render_template('index.html')


# 定義一個路徑(/run_script)
@app.route('/run_script', methods=['POST'])
def run_script():
    # 執行外部 Python 檔案
    subprocess.run(['python', 'catch_ETF_info.py'], capture_output=True, text=True)
    # 捕獲並返回腳本的輸出
    return render_template('result.html')


# 定義一個路徑(/back)
@app.route('/back', methods=['POST'])
def back():
    # 重新定向回首頁面
    return redirect(url_for('index'))


# 定義一個路徑(/home)
@app.route('/home')
def home():
    return render_template('home.html')


# 定義一個路徑(/to_volume)
@app.route('/to_volume', methods=['POST'])
def to_volume():
    # 定向至volume頁面
    return redirect(url_for('volume'))


# 定義一個路徑(/volume)
@app.route('/volume')
def volume():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return render_template('volume.html', tables=tables)


# 定義一個路徑(/data)
@app.route('/data')
def data():
    table_name = request.form.get('tables')
    if table_name in inspect(db.engine).get_table_names():



# 確保程式直接執行時啟動伺服器
if __name__ == '__main__':
    app.run(debug=True)
