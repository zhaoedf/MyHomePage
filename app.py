import click
import os
import sys
import datetime

from flask import Flask,render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_admin import Admin,AdminIndexView,expose
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditor, CKEditorField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user




# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = datetime.timedelta(seconds=1)
# app.config['DEBUG'] = True

db = SQLAlchemy(app, use_native_unicode='utf8')

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


bootstrap = Bootstrap(app)
ckeditor = CKEditor(app)
# Customized Post model admin
class PostAdmin(ModelView):
    # override form type with CKEditorField
    form_overrides = dict(text=CKEditorField)
    create_template = 'blogEdit.html'
    edit_template = 'blogEdit.html'

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class PostMessage(ModelView):
    form_overrides = dict(text=CKEditorField)
    create_template = 'blogEdit.html'
    edit_template = 'blogEdit.html'

class UserCheck(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))



class Message(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    mail = db.Column(db.String(40))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow,index=True)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow,index=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值

class MesForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('Message', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()


admin = Admin(app, name='Admin',index_view=MyAdminIndexView())
admin.add_view(PostAdmin(Blog, db.session))
admin.add_view(PostMessage(Message,db.session))
admin.add_view(UserCheck(User,db.session))


login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view='app.login'


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username)
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')



@app.route('/',methods=['GET','POST'])
def hello_world():

    if request.method == 'POST':
        print(1)
        name = request.form.get('name')
        mail = request.form.get('mail')
        content = request.form.get('content')
        print(content)

        mes = Message(name=name,mail=mail,body=content)
        db.session.add(mes)
        db.session.commit()

        flash('success！')

        return redirect((url_for('hello_world')))

    return render_template('index.html')

# @app.route('/admin', methods=['GET','POST'])
# def admin():
#     pass



@app.route('/blogDisplay',methods=['GET','POST'])
def blogAllDisplay():
    page = request.args.get('page',1,type=int)

    pagination = Blog.query.order_by(Blog.timestamp.desc()).paginate(page,3,error_out=False)

    blogs = pagination.items

    return render_template('blogDisplay.html',blogs=blogs,paginate=pagination)

@app.route('/blogContent/<int:blog_id>')
def blogContentShow(blog_id):
   blog = Blog.query.get_or_404(blog_id)
   blog.timestamp += datetime.timedelta(hours=8)

   return render_template('blogContent.html',blog=blog)


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象

@app.route('/login', methods=['GET','POST'])
def login():
    print(1)
    if request.method == 'POST':
        print(2)
        username = request.form['username']
        password = request.form['password']
        print(username,password)

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        print(username == user.username,user.validate_password(password))
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            print(1)
            return redirect(url_for('admin.index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面


    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    return 'log out successfully!'
    return redirect(url_for('hello_world'))  # 重定向回首页



@app.route('/adm')
@login_required
def admin_fliter():
    return render_template('admin.html')

@app.cli.command()
def delete_cache():
    pass



if __name__ == '__main__':
    app.run()
