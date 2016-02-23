# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SearchForm(Form):
    movieName = StringField('电影名:', validators=[Required(), Length(min=1, max=20)])
    submit = SubmitField('搜索')
