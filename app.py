from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pymysql
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "My_Key"
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/member')
def getmember():
    return render_template('member.html')

@app.route('/blog/<id>')
def getblog(id):
    return render_template('blog.html')


@app.route('/login')
def getlogin():
    return render_template('login.html')

@app.route('/blog/<id>/post')
def getpost(id):
    return render_template('post.html')

@app.route('/blog/<blog_id>/page/<page_id>')
def getpage(blog_id,page_id):
    return render_template('page.html')

@app.route('/comment/<post_id>', methods=["GET","POST"])
def all_comment(post_id):

    if request.method == 'GET':
        db = pymysql.connect(host='localhost', user='root', password='111111',
                             db='miniproject2', charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()

        filt1 = (post_id)

        sql = "SELECT * FROM comment WHERE post_id = %s "

        cur.execute(sql,filt1)
        comment_list = cur.fetchall()
        db.close()

        return jsonify({'comment':comment_list})
    else:
        db = pymysql.connect(host='localhost', user='root', password='111111',
                             db='miniproject2', charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()

        blog_id = request.form['id']
        user_id = request.form['user_id']
        comment = request.form['comment']

        comment_filter = (blog_id,post_id,user_id,comment)

        sql = "INSERT INTO comment (id, post_id, user_id, comment) VAlUES(%s, %s, %s, %s)"
        cur.execute(sql, comment_filter)
        db.commit()
        db.close()

        return jsonify({'msg': '저장 완료!'})



@app.route("/member/join", methods=["POST"])
def join_member():
    user_id = request.form['user_id']
    user_password = request.form['user_password']
    user_pw = bcrypt.generate_password_hash(user_password)
    user_name = request.form['user_name']
    user_nickname = request.form['user_nickname']
    user_image = request.form['user_image']


    doc = (user_id, user_pw, user_name, user_nickname, user_image)

    db = pymysql.connect(host='localhost', user='root', password='111111',
                         db='miniproject2', charset='utf8')
    cur = db.cursor()

    sql = "INSERT INTO users (user_id, user_password, user_name, user_nickname, user_img) VAlUES(%s, %s, %s, %s, %s)"
    cur.execute(sql,doc)
    db.commit()
    db.close()

    return jsonify({'msg': '저장 완료!'})

@app.route("/page/id", methods=["GET"])
def id_get():

    db = pymysql.connect(host='localhost', user='root', password='111111',
                         db='miniproject2', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()

    sql = "SELECT * FROM test1"
    cur.execute(sql)
    member_list = cur.fetchall()
    db.close()
    return jsonify({'member':member_list})


@app.route("/blog/data/<blog_id>", methods=["GET", "POST"])
def get_blog_data(blog_id):

    if request.method == "POST":
        if 'sorted' in session:
            session.pop('sorted',None)
        else:
            sorted = request.form['sorted']
            session['sorted'] = sorted

        return redirect(url_for('getblog',id=blog_id))
    else:
        db = pymysql.connect(host='localhost', user='root', password='111111',
                             db='miniproject2', charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()

        sql = '''SELECT u.user_nickname, p.* FROM users u
        LEFT JOIN posts p ON u.id = p.id
        WHERE u.id = %s
        '''

        sort = 0
        if 'sorted' in session:
            sql = sql + "ORDER BY good DESC"
            sort = 1

        cur.execute(sql,blog_id)
        blog_data = cur.fetchall()
        db.close()

        return jsonify({'blog_data':blog_data, 'sort':sort})





@app.route("/login/checkid", methods=["POST"])
def logincheck():
    login_id = request.form['login_id']
    login_password = request.form['login_password']
    doc = (login_id)

    db = pymysql.connect(host='localhost', user='root', password='111111',
                         db='miniproject2', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()


    sql = "SELECT * FROM users WHERE user_id = %s"
    cur.execute(sql,doc)
    member_list = cur.fetchall()
    db.close()

    if len(member_list) > 0:
        user_password = member_list[0]['user_password']
        if bcrypt.check_password_hash(user_password, login_password):
            login_permission = True
        else:
            login_permission = False

    return jsonify({'login_permission':login_permission})



@app.route("/mypage")
def go_mypage():
    return render_template('mypage.html')


@app.route("/id", methods=["POST"])
def get_session_id():
    user_id = request.form['user_id']

    db = pymysql.connect(host='localhost', user='root', password='111111',
                         db='miniproject2', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()

    sql = "SELECT id FROM users WHERE user_id = %s"

    cur.execute(sql,user_id)
    id = cur.fetchall()
    db.close()

    return jsonify({'id':id})


@app.route("/post/upload", methods=["POST"])
def post_upload():
    user_id = request.form['user_id']
    id = request.form['id']

    post_title = request.form['post_title']
    post_text = request.form['post_text']

    doc = (id, user_id, post_title, post_text, 0)

    db = pymysql.connect(host='localhost', user='root', password='111111',
                         db='miniproject2', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()

    sql = "INSERT INTO posts (id, user_id, post_title, post_text, good) VAlUES(%s, %s, %s, %s, %s)"
    cur.execute(sql,doc)
    db.commit()
    db.close()

    return jsonify({'msg': '저장 완료!'})



@app.route("/blog/page/<page_id>/data", methods=["GET"])
def get_page_data(page_id):

    db = pymysql.connect(host='localhost', user='root', password='111111',
                         db='miniproject2', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()
    filt1 = (page_id)
    sql = "SELECT * FROM posts WHERE post_id = %s"

    cur.execute(sql,filt1)
    page_data = cur.fetchall()
    db.close()

    return jsonify({'page_data':page_data})

@app.route("/blog/good/<post_id>/good", methods=["POST"])
def good(post_id):
    good = request.form['good']


    db = pymysql.connect(host='localhost', user='root', password='111111',
                         db='miniproject2', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()

    good_filter = (good,post_id)

    sql = "UPDATE posts SET good = %s WHERE post_id = %s"

    cur.execute(sql,good_filter)
    db.commit()
    db.close()

    return jsonify({})

@app.route("/data", methods=["GET"])
def recommend_blog():

    db = pymysql.connect(host='localhost', user='root', password='111111',
                         db='miniproject2', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()

    sql = '''SELECT u.id, u.user_nickname, sum(p.good) as sum FROM users u LEFT JOIN posts p ON u.id = p.id
    GROUP BY u.id ORDER BY sum DESC '''

    cur.execute(sql)
    recommend_blog_data = cur.fetchall()
    db.close()

    return jsonify({'recommend_blog_data':recommend_blog_data})



@app.route("/mypage/<id>", methods=["GET"])
def get_mypage_data(id):

    db = pymysql.connect(host='localhost', user='root', password='111111',
                         db='miniproject2', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()

    sql = "SELECT * FROM users WHERE id = %s"

    cur.execute(sql,id)
    mypage_data_list = cur.fetchall()
    db.close()

    return jsonify({'mypage_data':mypage_data_list})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)