# -*- coding: utf-8 -*-
from app import db

class Movieinfo(db.Model):
    __tablename__ = 'movieinfo'

    linkmd5id = db.Column(db.String(32), primary_key=True)
    moviesite = db.Column(db.String(20), nullable=False, server_default=db.text("'NULL'"))
    description = db.Column(db.Text)
    link = db.Column(db.Text)
    updated = db.Column(db.DateTime)
