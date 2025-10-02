from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "mysecretkey"  # 세션용 키

# DB 연결
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="비밀번호입력",  # ← 본인 MySQL 비밀번호
        database="bookstore"
    )

# 메인 페이지
@app.route("/")
def index():
    logged_in = "user_id" in session
    return render_template("index.html", logged_in=logged_in)

# 회원가입
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
        except:
            return "회원가입 실패 (중복 ID)"
        cursor.close()
        conn.close()
        return redirect(url_for("index"))
    return render_template("register.html")

# 로그인
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))
        else:
            return "로그인 실패"
    return render_template("login.html")

# 로그아웃
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# 책 목록
@app.route("/books")
def books():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    book_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("booklist.html", books=book_list)

# 책 구매
@app.route("/buy/<int:book_id>")
def buy(book_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT price FROM books WHERE id=%s", (book_id,))
    price = cursor.fetchone()[0]

    cursor.execute("INSERT INTO sales (book_id, user_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
                   (book_id, session["user_id"], 1, price))
    conn.commit()

    cursor.close()
    conn.close()
    return "구매 완료!"

# 북뷰어
@app.route("/viewer")
def viewer():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("viewer.html")

if __name__ == "__main__":
    app.run(debug=True)
