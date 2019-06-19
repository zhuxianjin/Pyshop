#coding: utf-8
from flask import *
import pymysql
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

db = pymysql.connect("localhost","root","toor","flask" )
cursor = db.cursor()
global good


def initdb():
    # mysql预处理语句
    sql = """CREATE TABLE users (
        username  CHAR(20) NOT NULL,
        passwd  CHAR(20))"""
    if not (cursor.execute("desc users")):
        cursor.execute(sql)

def regdb(reg_name,reg_pass):
    #reg_pass = reg_pass.encode('utf-8')
    reg_pass = hashlib.md5(str(reg_pass).encode('utf-8')).hexdigest()
    sql_reg = "insert into  users(username,passwd,money) values('"+reg_name+"','"+reg_pass+"',1000)"
    f = cursor.execute(sql_reg)
    db.commit()
    if f:
        return 1
    else:
        return 0

def check(chname,chpass):
    #chpass = chpass.encode('utf-8')
    chpass = hashlib.md5(str(chpass).encode('utf-8')).hexdigest()
    sql_sea = "select * from users where username='"+chname+"' and passwd='"+chpass+"'"
    #print(res)
    if cursor.execute(sql_sea):
        db.commit()
        return 1
    else:
        return 0

def getmoney(name):
    sql_m = "select * from users where username='"+name+"'"
    cursor.execute(sql_m)
    u_money = cursor.fetchall()
    return u_money[0][2]



@app.route('/')
def index():
    #initdb()
    user=session.get('user')
    sql_g = "select * from goods"
    cursor.execute(sql_g)
    goods = cursor.fetchall()
    if (user):
        return render_template('index.html',Login=user,goods=goods)
    else:
        return render_template('index.html',Login='Login',goods=goods)


@app.route('/register/',methods=['GET','POST'])
def register():
    alert = ''
    if  request.method == 'POST':
        name = request.values.get('user')
        passwd = request.values.get('passwd')
        if name != '' and passwd != '':
            sql_exname = "select * from users where username='"+name+"'"
            if cursor.execute(sql_exname):
                alert = 'username exists!'
                return render_template('register.html',alert=alert)
            else:
                if regdb(name,passwd):
                    return redirect("/login/")
                else:
                    alert = 'Wrong!!'
        else:
            alert = 'Wrong!!'
    return render_template('register.html',alert=alert)

@app.route('/login/',methods=['GET','POST'])
def login():
    alert = ''
    name = ''
    sql_sea = ''
    user=session.get('user')
    if (user):
        if (request.method == 'POST'):
            session['user'] = ''
            return redirect("/login/")    
        #sql_m = "select * from users where username='"+session['user']+"'"
        #cursor.execute(sql_m)
        #u_money = cursor.fetchall()
        return render_template('logined.html',name=user,money=getmoney(session['user']))
    if  request.method == 'POST':
        name = request.values.get('user')
        passwd = request.values.get('passwd')
        if name!= '' and passwd != '' and check(name,passwd):
            session['user'] = name
            name ='admin'
            return redirect("/")
        else:
            alert = 'Wrong!!'
        #return render_template('login.html',alert=alert)
    return render_template('login.html',alert=alert,name='please login')

@app.route('/logout/')
def logout():
        session['user'] = ''
        return redirect("/login/")    

def agood(gname):
    sql_chg = "select * from goods where gname='"+gname+"'"
    cursor.execute(sql_chg)
    agood = cursor.fetchall()
    return agood


@app.route('/view/<gname>',methods=['GET','POST'])
def view(gname):
    user=session.get('user')
    if (user):
        if request.method == 'POST':
            gname = request.values.get('gname')
            gmoney = int(request.values.get('gmoney'))
            my_money = getmoney(session['user']) 
            if my_money > gmoney or my_money == gmoney:
                my_money -= gmoney
                sql_up = "update  users set money="+str(my_money)+" where username='"+session['user']+"'"
                cursor.execute(sql_up)
            return render_template('view.html',Login=user,agood=agood(gname),msg="bought！,your money is: "+str(my_money))
        return render_template('view.html',Login=user,agood=agood(gname))
    else:
        return render_template('view.html',Login='Login',agood=agood(gname))
'''
@app.route('/view/',methods=['GET','POST'])
def view()
'''

@app.route('/err/')
def err():
    return render_template('err.html')

@app.route('/add/',methods=['GET','POST'])
def add_goods():
    alert = ''
    sql_addg = ''
    user=session.get('user')
    if not (user):
        return redirect("/err/")
    if  request.method == 'POST':
        gname = request.values.get('gname')
        glink = request.values.get('glink')
        gmoney = request.values.get('gmoney')
        if gname!= '' and glink != '' and gmoney != '':
            sql_addg = "insert into goods(gname,glink,gmoney) values('"+gname+"','"+glink+"',"+gmoney+")"
            cursor.execute(sql_addg)
            db.commit()
            return redirect("/")
        else:
            alert = 'Wrong!!'
        #return render_template('login.html',alert=alert)
    return render_template('add.html',alert=alert)

if __name__ == '__main__':
    app.run(port = 1111,debug = True)
