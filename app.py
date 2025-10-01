from flask import Flask, request, jsonify, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "mysecret"  # 세션 암호화용 키

# ✅ MySQL 연결 설정
db = mysql.connector.connect(
    host="localhost",      # Render에 올릴 때는 DB 호스트 주소 입력
    user="root",           # MySQL 사용자 이름
    password="0000",       # MySQL 비밀번호
    database="bookshop"    # 사용할 데이터베이스 이름
)
cursor = db.cursor(dictionary=True)

# ✅ 회원가입
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]

    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()
    return jsonify({"message": "회원가입 완료!"})

# ✅ 로그인
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        session["user_id"] = user["id"]
        return jsonify({"message": "로그인 성공!"})
    else:
        return jsonify({"message": "로그인 실패"}), 401

# ✅ 주문하기
@app.route("/order", methods=["POST"])
def order():
    if "user_id" not in session:
        return jsonify({"message": "로그인 먼저 하세요"}), 403

    data = request.json
    book_title = data["book_title"]
    amount = data["amount"]

    cursor.execute("INSERT INTO orders (user_id, book_title, amount) VALUES (%s, %s, %s)",
                   (session["user_id"], book_title, amount))
    db.commit()
    return jsonify({"message": "주문 완료!"})

# ✅ 주문 목록 보기
@app.route("/orders", methods=["GET"])
def get_orders():
    if "user_id" not in session:
        return jsonify({"message": "로그인 먼저 하세요"}), 403

    cursor.execute("SELECT * FROM orders WHERE user_id=%s", (session["user_id"],))
    orders = cursor.fetchall()
    return jsonify(orders)

if __name__ == "__main__":
    app.run(debug=True)
