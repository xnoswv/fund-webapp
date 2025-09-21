
from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "secret123"

# قاعدة بيانات وهمية
users = {"user": {"password": "1234", "balance": 100000, "trades": []}}
assets = {"Bitcoin":30000, "Ethereum":2000, "Tesla":900}

def update_prices():
    import random
    for asset in assets:
        change = random.uniform(-0.05, 0.05)
        assets[asset] = round(assets[asset]*(1+change),2)

@app.route("/", methods=["GET"])
def home():
    if "user" not in session:
        return redirect("/login")
    update_prices()
    user = users[session["user"]]
    return render_template("index.html", assets=assets, balance=user["balance"], trades=user["trades"])

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"]==password:
            session["user"]=username
            return redirect("/")
        else:
            return "خطأ في اسم المستخدم أو كلمة المرور"
    return render_template("login.html")

@app.route("/trade", methods=["POST"])
def trade():
    asset = request.form["asset"]
    trade_type = request.form["type"]
    quantity = float(request.form["quantity"])
    user = users[session["user"]]
    price = assets[asset]*quantity
    if trade_type=="buy":
        if user["balance"]>=price:
            user["balance"]-=price
            user["trades"].append(f"اشترى {quantity} من {asset} بسعر {price}")
        else:
            return "الرصيد غير كافي"
    elif trade_type=="sell":
        user["balance"]+=price
        user["trades"].append(f"باع {quantity} من {asset} بسعر {price}")
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__=="__main__":
    app.run(debug=True)
