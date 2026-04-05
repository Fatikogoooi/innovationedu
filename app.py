"""
InnovationEdu - Басты серверлік файл
Flask + SQLite + bcrypt
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = "innovationedu-secret-key-2025"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///innovationedu.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ─── МОДЕЛЬДЕР (Кестелер) ─────────────────────────────────────────────────────

class User(db.Model):
    """Пайдаланушылар кестесі"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="admin")  # admin / superadmin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Question(db.Model):
    """Тест сұрақтары кестесі"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct = db.Column(db.String(1), nullable=False)  # a, b, c, немесе d
    topic = db.Column(db.String(100), default="Жалпы")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TestResult(db.Model):
    """Оқушылардың тест нәтижелері"""
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)


class Content(db.Model):
    """Сайт мазмұны (редакциялауға болатын)"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


# ─── ДЕКОРАТОРЛАР ─────────────────────────────────────────────────────────────

def login_required(f):
    """Кіруді талап ететін беттерге декоратор"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ─── БАСТАПҚЫ ДЕРЕКТЕР ────────────────────────────────────────────────────────

def seed_database():
    """Дерекқорды алғашқы деректермен толтыру"""
    # Әдепкі сұрақтар
    if Question.query.count() == 0:
        questions = [
            Question(
                text="Алгоритм дегеніміз не?",
                option_a="Программа тілі",
                option_b="Есепті шешудің нақты қадамдар тізбегі",
                option_c="Компьютер құрылғысы",
                option_d="Деректер базасы",
                correct="b",
                topic="Алгоритмдеу"
            ),
            Question(
                text="HTML тегінің дұрыс жазылуы қайсысы?",
                option_a="<html>",
                option_b="(html)",
                option_c="[html]",
                option_d="{html}",
                correct="a",
                topic="Веб-технологиялар"
            ),
            Question(
                text="Python тілінде пікір (comment) қалай жазылады?",
                option_a="// пікір",
                option_b="/* пікір */",
                option_c="# пікір",
                option_d="<!-- пікір -->",
                correct="c",
                topic="Программалау"
            ),
            Question(
                text="Wi-Fi дегеніміз не?",
                option_a="Сымды желі",
                option_b="Сымсыз желі технологиясы",
                option_c="Процессор түрі",
                option_d="Операциялық жүйе",
                correct="b",
                topic="Желілер"
            ),
            Question(
                text="1 байт неше биттен тұрады?",
                option_a="4",
                option_b="16",
                option_c="8",
                option_d="32",
                correct="c",
                topic="Ақпарат өлшемі"
            ),
        ]
        db.session.add_all(questions)

    # Әдепкі контент
    if Content.query.count() == 0:
        contents = [
            Content(key="hero_title", value="Инновациялық Информатика"),
            Content(key="hero_subtitle", value="Танымдық белсенділікті арттыру — заманауи әдістер арқылы"),
            Content(key="about_text", value="Бұл платформа оқушылардың информатика пәніне деген қызығушылығын геймификация, жобалық оқыту және STEM әдістері арқылы арттыруға арналған."),
        ]
        db.session.add_all(contents)

    db.session.commit()


# ─── МАРШРУТТАР (Routes) ──────────────────────────────────────────────────────

@app.route("/")
def index():
    contents = {c.key: c.value for c in Content.query.all()}
    return render_template("index.html", contents=contents)

@app.route("/learning")
def learning():
    return render_template("learning.html")

@app.route("/test")
def test_page():
    return render_template("test.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

# ─── АВТОРИЗАЦИЯ ──────────────────────────────────────────────────────────────

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")

        if User.query.filter_by(username=username).first():
            return jsonify({"success": False, "message": "Бұл логин бұрыннан бар"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "Бұл email бұрыннан тіркелген"}), 400
        if len(password) < 6:
            return jsonify({"success": False, "message": "Пароль кемінде 6 таңба болуы керек"}), 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"success": True, "message": "Сәтті тіркелдіңіз!"})

    return render_template("auth.html", mode="register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            return jsonify({"success": True, "redirect": "/admin"})
        return jsonify({"success": False, "message": "Логин немесе пароль қате"}), 401

    return render_template("auth.html", mode="login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ─── АДМИН ПАНЕЛІ ─────────────────────────────────────────────────────────────

@app.route("/admin")
@login_required
def admin():
    questions = Question.query.order_by(Question.created_at.desc()).all()
    results = TestResult.query.order_by(TestResult.taken_at.desc()).limit(50).all()
    contents = {c.key: c.value for c in Content.query.all()}
    stats = {
        "total_results": TestResult.query.count(),
        "avg_score": db.session.query(db.func.avg(TestResult.percentage)).scalar() or 0,
        "total_questions": Question.query.count(),
    }
    return render_template("admin.html",
                           questions=questions,
                           results=results,
                           contents=contents,
                           stats=stats,
                           username=session.get("username"))


# ─── API ENDPOINTS ────────────────────────────────────────────────────────────

@app.route("/api/questions")
def get_questions():
    """Тест сұрақтарын беру (дұрыс жауапсыз)"""
    questions = Question.query.all()
    return jsonify([{
        "id": q.id,
        "text": q.text,
        "options": {"a": q.option_a, "b": q.option_b, "c": q.option_c, "d": q.option_d},
        "topic": q.topic
    } for q in questions])


@app.route("/api/questions/add", methods=["POST"])
@login_required
def add_question():
    data = request.get_json()
    q = Question(
        text=data["text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct=data["correct"],
        topic=data.get("topic", "Жалпы")
    )
    db.session.add(q)
    db.session.commit()
    return jsonify({"success": True, "id": q.id})


@app.route("/api/questions/<int:qid>", methods=["DELETE"])
@login_required
def delete_question(qid):
    q = Question.query.get_or_404(qid)
    db.session.delete(q)
    db.session.commit()
    return jsonify({"success": True})


@app.route("/api/submit-test", methods=["POST"])
def submit_test():
    """Тест нәтижесін сақтау"""
    data = request.get_json()
    answers = data.get("answers", {})
    student_name = data.get("student_name", "Белгісіз")

    questions = Question.query.all()
    correct_count = 0
    for q in questions:
        if answers.get(str(q.id)) == q.correct:
            correct_count += 1

    total = len(questions)
    percentage = round((correct_count / total * 100) if total > 0 else 0, 1)

    result = TestResult(
        student_name=student_name,
        score=correct_count,
        total=total,
        percentage=percentage
    )
    db.session.add(result)
    db.session.commit()

    return jsonify({
        "success": True,
        "score": correct_count,
        "total": total,
        "percentage": percentage
    })


@app.route("/api/content/update", methods=["POST"])
@login_required
def update_content():
    data = request.get_json()
    for key, value in data.items():
        c = Content.query.filter_by(key=key).first()
        if c:
            c.value = value
            c.updated_at = datetime.utcnow()
        else:
            db.session.add(Content(key=key, value=value))
    db.session.commit()
    return jsonify({"success": True})


@app.route("/api/chat", methods=["POST"])
def chat():
    """AI чат — қарапайым жауаптар базасы"""
    msg = request.get_json().get("message", "").lower()

    responses = {
        "алгоритм": "Алгоритм — берілген есепті шешу үшін орындалатын нақты қадамдардың реттелген тізбегі. Мысалы: нан пісіру рецепті де алгоритм!",
        "python": "Python — оңай оқылатын синтаксисі бар жоғары деңгейлі программалау тілі. Деректер ғылымы, ИИ, веб-әзірлеу үшін өте қолайлы.",
        "html": "HTML (HyperText Markup Language) — веб-беттерді жасауға арналған белгілеу тілі. Барлық сайттың негізі.",
        "желі": "Компьютерлік желі — деректер алмасу үшін бір-бірімен байланысқан компьютерлер жиынтығы. LAN, WAN, MAN түрлері бар.",
        "деректер базасы": "Деректер базасы — ақпаратты ұйымдасқан түрде сақтауға арналған жүйе. MySQL, PostgreSQL, SQLite, MongoDB мысалдары.",
        "программалау": "Программалау — компьютерге нені орындау керектігін түсіндіретін нұсқаулар жазу өнері. Python, JavaScript, Java, C++ тілдерін үйренуден бастаңыз.",
        "геймификация": "Геймификация — оқу процесіне ойын элементтерін енгізу. Ұпай жүйесі, медальдар, рейтинг — оқушылардың мотивациясын арттырады.",
        "stem": "STEM — Science (Ғылым), Technology (Технология), Engineering (Инженерия), Mathematics (Математика). Бұл бағыт оқушыларды болашақ мамандықтарға дайындайды.",
        "pbl": "PBL (Project-Based Learning) — жобалық оқыту. Оқушылар нақты мәселені шешу арқылы білім алады. Командалық жұмыс дағдыларын дамытады.",
    }

    for keyword, response in responses.items():
        if keyword in msg:
            return jsonify({"reply": response})

    return jsonify({"reply": "Сұрағыңыз үшін рахмет! Информатика тақырыптары бойынша: алгоритм, Python, HTML, желі, деректер базасы, программалау, геймификация, STEM, PBL — осы сөздерді жазып сұрақ қойыңыз."})


# ─── ІСКЕ ҚОСУ ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_database()
        # Әдепкі админ жасау
        if not User.query.filter_by(username="admin").first():
            admin_user = User(username="admin", email="admin@innovationedu.kz")
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Әдепкі админ жасалды: admin / admin123")
    print("🚀 Сервер іске қосылды: http://localhost:5000")
    app.run(debug=True, port=5000)
