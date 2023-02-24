from flask import (
    Flask, session, abort, url_for, render_template,g,flash,request,redirect,Response
)
import json
import cv2 as cv
import numpy as np
import machine as m
import configparser

class CacheClass:

    def __init__(self):
        self.container={}
    
    def addUser(self,username):
        if self.container.get(username) is None:
            self.container[username]={}
    def addItem(self,username,key,value):
        self.addUser(username)
        self.container[username][key]=value
    def getItem(self,username,key):
        if self.container.get(username) is None:
            self.container[username]={}
        return self.container[username].get(key)
    def removeItem(self,username,key):
        self.container[username].pop(key)
    def removeUser(self,username):
        self.container.pop(username)
        
        
cache = CacheClass()
app=Flask(__name__)
config=configparser.ConfigParser()
config.read("config.ini")
app.secret_key = config['DEFAULT']['secret_key']
valid_user=config['DEFAULT']['valid_user']
temp={}
tempcounter=0

def is_valid_user(user):
    if user is None:
        return False
    elif user not in valid_user:
        return False
    else:
        return True

def show_stack(stack):
    global tempcounter
    result=[]
    for i in range(len(stack)):
        obj=stack[i]
        if isinstance(obj,m.ImBin):
            temp[tempcounter]=obj
            result.append("#"+str(tempcounter))
            tempcounter=tempcounter+1
        elif isinstance(obj,np.ndarray):
            result.append(obj.tolist())
        else:
            result.append(obj)
    return result

@app.before_request
def load_session():
    user_id=session.get('user')
    if is_valid_user(user_id):
        g.user=user_id
    else:
        g.user=None

#html file
@app.route("/",methods=["GET"])
def index():
    if (g.user is None):
        return render_template("home.html")
    else:
        return render_template("user_home.html")

# universal app entry
@app.route("/UniApp",methods=['POST'])
def uniapp():
    if (g.user is None):
        abort(401)

    if request.is_json:
        obj=request.get_json()
        stack=m.interpreter([],obj,g.user,cache)
        #filter image out
        return show_stack(stack)
    else:
        return ("You are not sending a json",400)



#file upload entry
@app.route("/upload",methods=['POST'])
def upload():
    f = request.files['image']
    #decode binary
    np_array=np.asarray(bytearray(f.read()),dtype="uint8")
    img = cv.imdecode(np_array,cv.IMREAD_UNCHANGED)
    cache.addItem(g.user,request.form['label'],img)
    return redirect(url_for('index'))

#ongoing mode
@app.route("/ongoing",methods=['POST','GET'])
def ongoing():
    if (g.user is None):
        abort(401)
    global tempcounter
    if request.method=="POST":
        if request.is_json:
            stack=cache.getItem(g.user,"stack")
            if stack is None:
                print("POST: stack is empty, initialize stack.")
                stack=[]
                cache.addItem(g.user,"stack",stack)
            obj=request.get_json()
            m.interpreter(stack,obj,g.user,cache)
        #filter image out

            return "Operation success"
    elif request.method=="GET":
        stack=cache.getItem(g.user,"stack")
        
        if stack is None:
            print("GET: stack is empty, initialize stack.")
            stack=[]
            cache.addItem(g.user,"stack",stack)
        return show_stack(stack)
    else:
        return ("You are not sending a json",400)

#download script
@app.route("/script/<file>",methods=["GET"])
def getScript(file):
    try:
        if file.endswith(".js"):
            f=open("script/"+file)
            return Response(f.read(),mimetype="application/javascript")
        else:
            abort(404)
    except:
        abort(404)

#download css
@app.route("/css/<file>",methods=["GET"])
def getCSS(file):
    try:
        if file.endswith(".css"):
            f=open("css/"+file)
            return Response(f.read(),mimetype="text/css")
        else:
            abort(404)
    except:
        abort(404)


#login
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == 'POST':
        username = request.form['user']
        if username not in valid_user:
            error = 'Incorrect username.'
        else:
            #login in successful
            session.clear()
            session['user'] = username
            return redirect(url_for('index'))
        flash(error)
    return render_template("login.html")


#download temp
@app.route("/temp/<int:label>",methods=["GET"])
def getTemp(label):
    image=temp.pop(label)
    if image.format==".jpg":
        return Response(image.data,mimetype="image/jpg")
    elif image.format==".png":
        return Response(image.data,mimetype="image/png")

#logout
@app.route("/logout",methods=["GET"])
def logout():
    session.clear()
    cache.removeUser(g.user)
    return redirect(url_for("index"))


