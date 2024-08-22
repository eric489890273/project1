from flask import Flask
from flask import render_template

# 建立一個 Flask 應用程式
app = Flask(__name__)


# 定義一個路徑（/page/text）
@app.route('/page/text')
def pageText():
    return render_template('page.html', text="Python Flask !")


# 定義一個路徑（/page/app）
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


# 定義一個路徑（/page/data）
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


# 定義一個路徑（/static）
@app.route('/static')
def staticPage():
    return render_template('static.html')


# 確保程式直接執行時啟動伺服器
if __name__ == '__main__':
    app.run(debug=True)
