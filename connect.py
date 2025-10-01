from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 메인 페이지
@app.route("/")
def home():
    return render_template("index.html")  # templates/index.html 불러오기

# 로그인 페이지
@app.route("/login_page")
def login_page():
    return render_template("login.html")

# 주문 페이지
@app.route("/order_page")
def order_page():
    return render_template("orders.html")
