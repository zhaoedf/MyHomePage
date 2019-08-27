import click
import os
import sys
from datetime import datetime

from flask import Flask,render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditor, CKEditorField


from datetime import timedelta


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
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
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

class message(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    mail = db.Column(db.String(40))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow,index=True)

class blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.Text)

class MesForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('Message', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()


admin = Admin(app, name='Flask-CKEditor demo')
admin.add_view(PostAdmin(blog, db.session))



@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')



@app.route('/',methods=['GET','POST'])
def hello_world():

    if request.method == 'POST':
        print(1)
        name = request.form.get('name')
        mail = request.form.get('mail')
        content = request.form.get('content')
        print(content)

        mes = message(name=name,mail=mail,body=content)
        db.session.add(mes)
        db.session.commit()

        flash('success！')

        return redirect((url_for('hello_world')))

    return render_template('index.html')

# @app.route('/admin', methods=['GET','POST'])
# def admin():
#     pass

@app.cli.command()
def delete_cache():
    pass



if __name__ == '__main__':
    app.run()
