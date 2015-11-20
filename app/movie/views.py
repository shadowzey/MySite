# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request
from . import movie
from ..models import Movieinfo
from .forms import SearchForm

@movie.route('/', methods=['GET','POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.movieName.data
        searchResult = Movieinfo.query.filter(Movieinfo.description.ilike('%{}%'.format(keyword))).all()
        for s in searchResult:
            s.links = eval(s.link)
        searchCount = len(searchResult)
        form.movieName.data = ''
        return render_template('movie/movie_result.html', searchResult = searchResult, count=searchCount, keyword=keyword)
    return render_template('movie/movie_search.html', form=form)

