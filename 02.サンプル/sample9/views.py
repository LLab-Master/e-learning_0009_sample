from flask import Flask, render_template, request, session, abort,redirect,flash

from config import app, login_manager
from models import MyJSONEncoder,User,UserManager
from forms import UserForm, LoginForm

from flask_login import login_required,login_user, logout_user

app.json_encoder = MyJSONEncoder
user_manager = UserManager(app.config['DATABASE_URI'])

#ログイン用のユーザ取得
@login_manager.user_loader
def load_user(user_id):
    if user_id != "None":
        user_data = user_manager.get_user_one(user_id)
        user = User(user_data[1],user_data[2],user_data[3],user_data[4])
        return user

#ログイン画面
@app.route('/secret')
@login_required
def index():
    return render_template('index.html')

#ログイン判定
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_data = user_manager.get_user_one(form.id.data)
        user = User(user_data[1],user_data[2],user_data[3],user_data[4])
        user.id = user_data[0]
        if user is not None:
            if user.password == form.password.data:
                login_user(user, False)
                next = request.args.get('next')
                return redirect(next)
        flash('ユーザ、パスワードが間違っています')
    return render_template('auth/login.html',form=form)

#ログアウト処理
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('secret')

#ユーザ一覧
@app.route('/user/list')
@login_required
def user_list():
    users = user_manager.get_user_all()
    return render_template('user_list.html',users=users)

#ユーザ追加
@app.route('/user/add',methods=['GET','POST'])
@login_required
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
@login_required
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
@login_required
def delete(id=None):
    if not id:
        abort(400)

    user_manager.delete_user(id)

    return render_template('delete_done.html')

#ユーザ更新
@app.route('/user/update/<int:id>',methods=['GET','POST'])
@login_required
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
@login_required
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
