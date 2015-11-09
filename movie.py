#!/usr/bin/env python
#coding=utf-8

from MovieSearch import movieSearch
from flask import Flask, render_template, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager, Shell
from flask.ext.wtf import Form
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
manager = Manager(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'never can guess it'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12342234yanze@localhost/moviedb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

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

class Movieresult(object):
    
    def __init__(self, moviesite, description, link):
        self.moviesite = moviesite
        self.description = description
        self.link = link

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
        #searchResult = movieSearch(keyword)
        searchResult = Movieinfo.query.filter(Movieinfo.description.ilike('%{}%'.format(keyword))).all()
        searchCount = len(searchResult)
        movieResult = []
        for m in searchResult:
            movie = Movieresult(moviesite=m.moviesite, description=m.description, link=eval(m.link))
            movieResult.append(movie)
        form.movieName.data = ''
        return render_template('movie_result.html', searchResult = movieResult, count=searchCount)
    return render_template('movie_search.html', form=form)
    
if __name__ == '__main__':
    manager.run()
