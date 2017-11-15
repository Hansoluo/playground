from flask import Flask,render_template,redirect,url_for,session,request
import re
from model import *
from collections import Counter
from datetime import datetime

app = Flask(__name__)

def init_db():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def main():
    """主页面，查询用户数据渲染页面，按钮跳转页面"""
    drafts = Draft.query.filter_by(author_id="user_id").all()
    a = []
    for i in drafts:
        a.append(i.tag)
    tag_list = Counter(a).most_common()

    if 'new_draft' in request.form.keys():
        return render_template('draft.html')
    elif 'tag' in request.form.keys():
        tag_drafts = Draft.query.filter_by(tag=request.form['tag']).all()
        return render_template('tag.html', tag_drafts=tag_drafts, tag_list=tag_list)
    else:
        nothing = 1
        return render_template('home.html', drafts=drafts, tag_list=tag_list,nothing=nothing)

# @app.route('/tag', methods=['GET','POST'])
# def tag():
#     """点击标签，刷新主页面"""
#     if 'tag' in request.form.keys():
#         print(request.form)
#         drafts = Draft.query.filter_by(tag=request.form['tag']).all()
#         return render_template('tag.html', drafts=drafts)

@app.route('/draft', methods=['GET','POST'])
def draft():
    """写素材页面，写完保存到数据库
       回到主页面按钮和开新页面按钮"""
    if 'save' in request.form.keys():
        tag = tag_extract(request.form['draft_data'])
        draft = Draft(body=request.form['draft_data'],
                      author_id="user_id",
                      timestamp=datetime.now().strftime('%Y-%m-%d %H:%M'),
                      tag=tag)
        db.session.add(draft)
        db.session.commit()
        return redirect(url_for('draft'))
    elif 'new_draft' in request.form.keys():
        return render_template('draft.html')
    return render_template('draft.html')

def tag_extract(draft):
    """从素材中提取多个标签，有则返回第一个标签，无则返回<未标注>"""
    tag1 = re.findall(r"#[\u4e00-\u9fa5_a-zA-Z0-9]+#", draft)
    a = []
    if tag1:
        for i in tag1:
            tag2 = re.sub(r'\W', '', i)
            a.append(tag2)
    else:
         a.append("未标注")

    return a[0]

if __name__ == '__main__':
    init_db()
    app.run(host="127.0.0.1", port=8080, debug=True)
