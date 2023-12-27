from flask import Flask

app = Flask(__name__)
app.config['DATABASE_URI'] = './test.db'
app.config['SECRET_KEY'] ='pg0MMXM2V8BgTvIXk7ikHA'
