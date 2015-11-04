#!/usr/bin/env python
#coding=utf-8

from MovieSearch import movieSearch
from flask import Flask, render_template, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'never can guess it'

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
        searchResult = movieSearch(keyword)
        form.movieName.data = ''
        return render_template('movie_result.html', searchResult = searchResult, )
    return render_template('movie_search.html', form=form)
    
if __name__ == '__main__':
    manager.run()
