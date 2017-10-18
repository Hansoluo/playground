#encoding:utf-8
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'drafts.db')

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 素材表：素材编号、内容、用户编号、编辑时间、标签
class Draft(db.Model):
    __tablename__ = 'drafts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.String(80), index=True, default=datetime.utcnow)
    author_id = db.Column(db.String(80), unique=False)
    tag = db.Column(db.String(80), unique=False)

    def __init__(self, body, timestamp, author_id, tag):
        self.body = body
        self.timestamp = timestamp
        self.author_id = author_id
        self.tag = tag
