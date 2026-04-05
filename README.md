# InnovationEdu — Іске Қосу Нұсқаулығы

## 📁 Файл құрылымы

```
innovationedu/
├── app.py                  ← Негізгі сервер (Flask)
├── requirements.txt        ← Кітапханалар тізімі
├── README.md               ← Осы файл
├── instance/
│   └── innovationedu.db    ← SQLite дерекқоры (автоматты жасалады)
├── static/
│   ├── css/
│   │   └── main.css        ← Стиль файлы
│   └── js/
│       └── main.js         ← JavaScript
└── templates/
    ├── base.html           ← Негізгі шаблон (навбар, футер)
    ├── index.html          ← Басты бет
    ├── learning.html       ← Оқу бөлімі
    ├── test.html           ← Тест беті
    ├── chat.html           ← AI Чат
    ├── auth.html           ← Кіру / Тіркелу
    └── admin.html          ← Админ панель
```

---

## 🚀 Іске қосу қадамдары

### 1. Python орнату
Python 3.8+ орнатылған болуы керек.
Тексеру: `python --version`

### 2. Жобаны жүктеу
```bash
# Жоба папкасына кіру
cd innovationedu
```

### 3. Виртуалды орта жасау (ұсынылады)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Кітапханаларды орнату
```bash
pip install -r requirements.txt
```

### 5. Серверді іске қосу
```bash
python app.py
```

### 6. Браузерді ашу
```
http://localhost:5000
```

---

## 🔐 Кіру деректері

| Рөл  | Логин | Пароль   |
|------|-------|----------|
| Админ | admin | admin123 |

> Жаңа админ тіркелу үшін: http://localhost:5000/register

---

## 📋 Сайт беттері

| Бет            | URL              | Сипаттама                        |
|----------------|------------------|----------------------------------|
| Басты бет      | /                | Жоба туралы ақпарат              |
| Оқу бөлімі     | /learning        | Геймификация, PBL, STEM          |
| Тест           | /test            | Интерактивті тест жүйесі         |
| AI Чат         | /chat            | Сұрақ-жауап чат боты             |
| Кіру           | /login           | Админ жүйесіне кіру              |
| Тіркелу        | /register        | Жаңа админ жасау                 |
| Админ панель   | /admin           | Барлық басқару мүмкіндіктері     |

---

## ⚙️ Админ панель мүмкіндіктері

- **Басқару тақтасы** — Жалпы статистика (тест саны, орташа %)
- **Сұрақтар** — Тест сұрақтарын қосу және өшіру
- **Нәтижелер** — Барлық оқушылардың тест нәтижелері
- **Контент** — Басты бет мәтінін редакциялау

---

## 🛠 Техникалық мәліметтер

- **Backend:** Python Flask 3.0
- **Дерекқор:** SQLite (Flask-SQLAlchemy арқылы)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Қауіпсіздік:** Werkzeug PBKDF2 хеш (пароль шифрлау)
- **Сессия:** Flask session (server-side)

---

## ❓ Жиі кездесетін қателер

**ModuleNotFoundError: No module named 'flask'**
→ `pip install -r requirements.txt` командасын орындаңыз

**Address already in use**
→ 5000 порт бос болуы керек. `python app.py` орнына `flask run --port 5001` қолданыңыз

**База жасалмады**
→ `instance/` папкасын қолмен жасаңыз немесе `python app.py` іске қосыңыз — база автоматты жасалады
