from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'


#url_forのテスト用の記述(生成されたURLをprintで表示)
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))

