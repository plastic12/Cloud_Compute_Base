from flask import (
    Flask, session, abort, url_for, render_template,g,flash,request,redirect,Response
)
import machine
import json
import io
import cv2 as cv
import numpy as np
import machine as m

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
        return self.container[username][key]
    def removeItem(self,username,key):
        self.container[username].pop(key)
    def removeUser(self,username):
        self.container.pop(username)
        
        
cache = CacheClass()
app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
valid_user={"plastic12","cherry","leaf","firefly"}
temp={}
tempcounter=0

@app.before_request
def load_session():
    user_id=session.get('user')
    if user_id is None:
        g.user=None
    elif user_id not in valid_user:
        g.user=None
    else:
        g.user=user_id

#main process entry
@app.route("/",methods=["GET","POST"])
def index():
    global tempcounter
    if request.method=="POST":
        if request.is_json:
            obj=request.get_json()
            stack=machine.interpreter(obj,g.user,cache)
            #filter image out
            result=[]
            while len(stack)!=0:
                obj=stack.pop(0)
                if isinstance(obj,m.ImBin):
                    temp[tempcounter]=obj
                    result.append("#"+str(tempcounter))
                    tempcounter=tempcounter+1
                elif isinstance(obj,np.ndarray):
                    result.append(obj.tolist())
                else:
                    result.append(obj)
            return json.dumps(result)
        else:
            return "You are not sending a json"
    if (g.user is None):
        return render_template("home.html")
    else:
        return render_template("user_home.html")


#file upload entry
@app.route("/upload",methods=['POST'])
def upload():
    f = request.files['image']
    #decode binary
    np_array=np.asarray(bytearray(f.read()),dtype="uint8")
    img = cv.imdecode(np_array,cv.IMREAD_UNCHANGED)
    cache.addItem(g.user,request.form['label'],img)
    return redirect(url_for('index'))

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


