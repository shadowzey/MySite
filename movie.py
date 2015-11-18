#!/usr/bin/env python
#coding=utf-8

from MovieSearch import movieSearch
from flask import Flask, render_template, redirect, url_for, request
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager, Shell
from flask.ext.wtf import Form
from flask.ext.moment import Moment
from flask.ext.mail import Mail
from flask.ext.paginate import Pagination
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
manager = Manager(app)
mail = Mail(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'never can guess it'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12342234yanze@localhost/moviedb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['SHADOW_MAIL_SUBJECT_PREFIX'] = '[Shadow]'
app.config['SHADOW_MAIL_SENDER'] = 'Shadow Admin <yanze000@hotmail.com>'

db = SQLAlchemy(app)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['SHADOW_MAIL_SUBJECT_PREFIX'] + subject, 
                  sender=app.config['SHADOW_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

def make_shell_context():
    return dict(app=app, db=db, Movieinfo=Movieinfo)

manager.add_command("shell", Shell(make_context=make_shell_context))

class Movieinfo(db.Model):
    __tablename__ = 'movieinfo'

    linkmd5id = db.Column(db.String(32), primary_key=True)
    moviesite = db.Column(db.String(20), nullable=False, server_default=db.text("'NULL'"))
    description = db.Column(db.Text)
    link = db.Column(db.Text)
    updated = db.Column(db.DateTime)


class SearchForm(Form):
    movieName = StringField('电影名:', validators=[Required(), Length(min=2, max=20)])
    submit = SubmitField('搜索')    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movie', methods=['GET','POST'])
def movie_index():
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.movieName.data
        searchResult = Movieinfo.query.filter(Movieinfo.description.ilike('%{}%'.format(keyword))).all()
        for s in searchResult:
            s.links = eval(s.link)
        searchCount = len(searchResult)
        form.movieName.data = ''
#        return render_template('movie_result.html', searchResult = searchResult, count=searchCount, keyword=keyword)
        return movie_result(keyword, searchResult, searchCount)
    return render_template('movie_search.html', form=form)

@app.route('/movie/result')
def movie_result(keyword, searchResult, searchCount):
    search = False
    q = request.args.get('q')
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    
    pagination = Pagination(page=page, total=searchCount, search=search, record_name='搜索结果')
    return render_template('movie_result.html',
                           searchResult=searchResult,
                           pagination=pagination,
                           keyword=keyword,
                           searchCount=searchCount
                           )

    
if __name__ == '__main__':
    manager.run()
