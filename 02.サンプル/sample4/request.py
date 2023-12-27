from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    html = '''
    <form action="go" method="post">
        <input type="text" name="message" />
        <input type="submit" value="send" />
    </form>
    '''
    return html

@app.route('/go',methods=['POST'])
def hello():
    if request.method == 'POST':
        messsage = request.form['message']
        res = '<h1>'+messsage+'</h1>'
        return res

if __name__ == '__main__':
    app.run()
