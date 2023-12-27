from flask import Flask, render_template, request, session, abort

from config import app
from models import MyJSONEncoder,User,UserManager
from forms import UserForm

app.json_encoder = MyJSONEncoder
user_manager = UserManager(app.config['DATABASE_URI'])

#トップ画面
@app.route('/')
def index():
    return render_template('index.html')

#ユーザ一覧
@app.route('/user/list')
def user_list():
    users = user_manager.get_user_all()
    return render_template('user_list.html',users=users)


@app.route('/login')
def login():
    form = LoginForm

#ユーザ追加
@app.route('/user/add',methods=['GET','POST'])
def input():
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            password = form.password.data
            age = form.age.data
            address = form.address.data
            user = User(name,password,age,address)
            session['user'] = user
            return render_template('confirm.html', user=user)


    return render_template('input.html', form=form)


#ユーザ追加完了
@app.route('/done')
def done():
    user_dict = session.get('user')
    if not user_dict:
        abort(400)

    '''
    登録処理
    '''
    user = User(user_dict.get('name'),
                user_dict.get('password'),
                user_dict.get('age'),
                user_dict.get('address'))
    user_manager.add_user(user)

    session.pop('user',None) #セッションクリア
    return render_template('done.html',user=user)


#ユーザ削除
@app.route('/user/delete/<int:id>')
def delete(id=None):
    if not id:
        abort(400)

    user_manager.delete_user(id)

    return render_template('delete_done.html')

#ユーザ更新
@app.route('/user/update/<int:id>',methods=['GET','POST'])
def update(id=None):
    if not id:
        abort(400)

    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            password = form.password.data
            age = form.age.data
            address = form.address.data
            user = User(name, password, age, address)
            session['user'] = user
            return render_template('edit_confirm.html', user=user)

    # 'GET' or validation Error
    user = user_manager.get_user_one(id)
    form.name.data = user[1]
    form.password.data = user[2]
    form.age.data = user[3]
    form.address.data = user[4]
    session['user_id'] = user[0]

    return render_template('edit.html' , form=form)

#ユーザ更新完了
@app.route('/edit_done')
def edit_done():
    user_dict = session.get('user')
    id = session.get('user_id')
    if not user_dict:
        abort(400)

    '''
    登録処理(更新処理)
    '''
    user =  User()
    user.id = id
    user.name = user_dict.get('name')
    user.password = user_dict.get('password')
    user.age = user_dict.get('age')
    user.address = user_dict.get('address')

    user_manager.update_user(user)

    session.pop('user',None) #セッションクリア
    session.pop('user_id',None)

    return render_template('edit_done.html',user=user)
