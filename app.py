
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta
from bson.json_util import dumps

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def listing():
    memoList = list(db.memos.find({}, {'_id':False}))

    # for i in memoList:
    #     i['_id'] = str(i['_id'])

       
    return jsonify({'result':"success", 'msg':'GET 연결 되었습니다.', 'memos':memoList})

@app.route('/memo', methods=['POST'])
def post_articles():
    # port url ?? url_give
    url_receive = request.form['title_give']
    comment_receive = request.form['ctx_give']
    id_receive = request.form['id_give']
    
    memo = {'title' : url_receive, 'ctx': comment_receive, 'id':id_receive}
    
    db.memos.insert_one(memo)
   
    return jsonify({'result':'success', 'msg':"POST 연결 되었습니다."})
    


@app.route('/editmemo', methods=['POST'])
def edit_memo():
    url_receive = request.form['title_give']
    comment_receive = request.form['ctx_give']
    id_receive = request.form['id_give']
    
    memo = {'title' : url_receive, 'ctx': comment_receive, 'id':id_receive}
    objMemo = db.memos.update_one({'id':id_receive}, { '$set': {'title':url_receive, 'ctx': comment_receive} })
   
    return jsonify({'result':'success', 'msg':" 수정 되었습니다."})
    

@app.route('/deletememo', methods=['POST'])
def delete_memo():
    id_receive = request.form['id_give']
    
    objMemo = db.memos.delete_one({'id':id_receive})
   
    return jsonify({'result':'success', 'msg':" 삭제 되었습니다."})
    
    

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5003,debug=True)