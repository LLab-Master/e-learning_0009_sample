from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html',
                           message='hello Jinja2')

@app.route('/sample1')
def sample1():
    profile = {'name':'yamada','age':32}
    return render_template('sample1.html'
                           ,profile=profile)



if __name__ == '__main__':
    app.run()
