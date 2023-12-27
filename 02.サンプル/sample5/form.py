from flask import Flask, request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired,Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pg0MMXM2V8BgTvIXk7ikHA'

class NameForm(FlaskForm):
    name = StringField('氏名',validators=[DataRequired()
        ,Length(max=4,message='4文字以下を入力して下さい')])
    submit = SubmitField('送信')



@app.route('/sample2',methods=['GET','POST'])
def sample2():
    name = None
    form = NameForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data

    return render_template('sample2.html', form=form, name=name)



@app.route('/')
def index():

    return render_template('index.html',
                           message='hello Jinja2')

@app.route('/go',methods=['POST'])
def hello():
    if request.method == 'POST':
        messsage = request.form['message']
        res = '<h1>'+messsage+'</h1>'
        return res

@app.route('/hello/<name>')
def hello2(name=None):
    return '<h1>{}</h1>'.format(name)

@app.route('/sample1')
def sample1():
    profile = {'name':'yamada','age':32}
    return render_template('sample1.html'
                           ,profile=profile)



if __name__ == '__main__':
    app.run()
