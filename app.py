"""
FinanceWise - Interactive Financial Literacy Platform for Youth Earners
Flask + SQLite implementation based on the project SRS.

Run:
    python database.py   # one-time: creates & seeds financewise.db
    python app.py         # starts the dev server on http://127.0.0.1:5000
"""

from functools import wraps
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db, DB_PATH
import os

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-this-in-production"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_conn():
    if "db" not in g:
        g.db = get_db()
    return g.db


@app.teardown_appcontext
def close_conn(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return wrapper


def award_badge(conn, user_id, criteria):
    badge = conn.execute("SELECT * FROM badges WHERE criteria = ?", (criteria,)).fetchone()
    if not badge:
        return
    already = conn.execute(
        "SELECT 1 FROM user_badges WHERE user_id = ? AND badge_id = ?",
        (user_id, badge["id"]),
    ).fetchone()
    if not already:
        conn.execute(
            "INSERT INTO user_badges (user_id, badge_id) VALUES (?, ?)",
            (user_id, badge["id"]),
        )
        conn.commit()
        flash(f"Achievement unlocked: {badge['icon']} {badge['name']}!", "success")


@app.context_processor
def inject_user():
    return {"current_user": {
        "id": session.get("user_id"),
        "name": session.get("full_name"),
        "role": session.get("role"),
    }}


# ---------------------------------------------------------------------------
# Auth (SRS 3.1 / 3.2)
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not full_name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("register"))

        conn = get_conn()
        existing = conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone()
        if existing:
            flash("An account with that email already exists.", "danger")
            return redirect(url_for("register"))

        conn.execute(
            "INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, 'user')",
            (full_name, email, generate_password_hash(password)),
        )
        conn.commit()
        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_conn()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            session["role"] = user["role"]
            flash(f"Welcome back, {user['full_name']}!", "success")
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# Dashboard (SRS 3.3)
# ---------------------------------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_conn()
    uid = session["user_id"]
    now = datetime.now()

    income_row = conn.execute(
        "SELECT SUM(amount) AS total FROM income WHERE user_id = ? AND month = ? AND year = ?",
        (uid, now.month, now.year),
    ).fetchone()
    total_income = income_row["total"] or 0

    expense_row = conn.execute(
        "SELECT SUM(amount) AS total FROM expenses WHERE user_id = ? "
        "AND strftime('%m', date) = ? AND strftime('%Y', date) = ?",
        (uid, f"{now.month:02d}", str(now.year)),
    ).fetchone()
    total_expenses = expense_row["total"] or 0

    goals = conn.execute("SELECT * FROM goals WHERE user_id = ?", (uid,)).fetchall()
    total_saved = sum(gl["saved_amount"] for gl in goals)

    total_lessons = conn.execute("SELECT COUNT(*) AS c FROM lessons").fetchone()["c"]
    completed_lessons = conn.execute(
        "SELECT COUNT(*) AS c FROM progress WHERE user_id = ? AND completed = 1", (uid,)
    ).fetchone()["c"]

    recent_quizzes = conn.execute(
        "SELECT qa.*, l.title FROM quiz_attempts qa JOIN lessons l ON qa.lesson_id = l.id "
        "WHERE qa.user_id = ? ORDER BY qa.taken_at DESC LIMIT 5", (uid,)
    ).fetchall()

    my_badges = conn.execute(
        "SELECT b.* FROM user_badges ub JOIN badges b ON ub.badge_id = b.id "
        "WHERE ub.user_id = ? ORDER BY ub.earned_at DESC", (uid,)
    ).fetchall()

    return render_template(
        "dashboard.html",
        total_income=total_income,
        total_expenses=total_expenses,
        balance=total_income - total_expenses,
        total_saved=total_saved,
        goals=goals,
        total_lessons=total_lessons,
        completed_lessons=completed_lessons,
        recent_quizzes=recent_quizzes,
        my_badges=my_badges,
    )


# ---------------------------------------------------------------------------
# Learning Modules (SRS 3.4)
# ---------------------------------------------------------------------------

@app.route("/lessons")
@login_required
def lessons():
    conn = get_conn()
    uid = session["user_id"]
    rows = conn.execute(
        """SELECT l.*, p.completed
           FROM lessons l
           LEFT JOIN progress p ON p.lesson_id = l.id AND p.user_id = ?
           ORDER BY l.order_index""",
        (uid,),
    ).fetchall()
    return render_template("lessons.html", lessons=rows)


@app.route("/lessons/<int:lesson_id>")
@login_required
def lesson_detail(lesson_id):
    conn = get_conn()
    lesson = conn.execute("SELECT * FROM lessons WHERE id = ?", (lesson_id,)).fetchone()
    if not lesson:
        flash("Lesson not found.", "danger")
        return redirect(url_for("lessons"))
    return render_template("lesson_detail.html", lesson=lesson)


@app.route("/lessons/<int:lesson_id>/complete", methods=["POST"])
@login_required
def complete_lesson(lesson_id):
    conn = get_conn()
    uid = session["user_id"]
    conn.execute(
        """INSERT INTO progress (user_id, lesson_id, completed, completed_at)
           VALUES (?, ?, 1, CURRENT_TIMESTAMP)
           ON CONFLICT(user_id, lesson_id) DO UPDATE SET completed = 1, completed_at = CURRENT_TIMESTAMP""",
        (uid, lesson_id),
    )
    conn.commit()

    total_lessons = conn.execute("SELECT COUNT(*) AS c FROM lessons").fetchone()["c"]
    completed = conn.execute(
        "SELECT COUNT(*) AS c FROM progress WHERE user_id = ? AND completed = 1", (uid,)
    ).fetchone()["c"]

    award_badge(conn, uid, "lesson_complete_1")
    if total_lessons and completed >= total_lessons:
        award_badge(conn, uid, "lesson_complete_all")

    flash("Lesson marked as complete!", "success")
    return redirect(url_for("lesson_detail", lesson_id=lesson_id))


# ---------------------------------------------------------------------------
# Quiz Module (SRS 3.5)
# ---------------------------------------------------------------------------

@app.route("/quiz/<int:lesson_id>", methods=["GET", "POST"])
@login_required
def quiz(lesson_id):
    conn = get_conn()
    lesson = conn.execute("SELECT * FROM lessons WHERE id = ?", (lesson_id,)).fetchone()
    questions = conn.execute(
        "SELECT * FROM quiz_questions WHERE lesson_id = ?", (lesson_id,)
    ).fetchall()

    if request.method == "POST":
        score = 0
        for q in questions:
            selected = request.form.get(f"q{q['id']}")
            if selected == q["correct_option"]:
                score += 1

        uid = session["user_id"]
        conn.execute(
            "INSERT INTO quiz_attempts (user_id, lesson_id, score, total) VALUES (?, ?, ?, ?)",
            (uid, lesson_id, score, len(questions)),
        )
        conn.commit()

        if questions and score == len(questions):
            award_badge(conn, uid, "quiz_perfect")

        return render_template(
            "quiz_result.html", lesson=lesson, score=score, total=len(questions)
        )

    return render_template("quiz.html", lesson=lesson, questions=questions)


# ---------------------------------------------------------------------------
# Budget Planner (SRS 3.6)
# ---------------------------------------------------------------------------

@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    conn = get_conn()
    uid = session["user_id"]
    now = datetime.now()

    if request.method == "POST":
        category = request.form.get("category", "").strip()
        amount = request.form.get("amount", "0")
        try:
            amount = float(amount)
        except ValueError:
            amount = 0
        if category and amount > 0:
            conn.execute(
                "INSERT INTO budget (user_id, month, year, category, allocated_amount) VALUES (?, ?, ?, ?, ?)",
                (uid, now.month, now.year, category, amount),
            )
            conn.commit()
            award_badge(conn, uid, "budget_created")
            flash("Budget category added.", "success")
        return redirect(url_for("budget"))

    items = conn.execute(
        "SELECT * FROM budget WHERE user_id = ? AND month = ? AND year = ? ORDER BY id DESC",
        (uid, now.month, now.year),
    ).fetchall()
    total_allocated = sum(item["allocated_amount"] for item in items)

    income_row = conn.execute(
        "SELECT SUM(amount) AS total FROM income WHERE user_id = ? AND month = ? AND year = ?",
        (uid, now.month, now.year),
    ).fetchone()
    total_income = income_row["total"] or 0

    return render_template(
        "budget.html", items=items, total_allocated=total_allocated, total_income=total_income
    )


@app.route("/budget/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_budget(item_id):
    conn = get_conn()
    conn.execute("DELETE FROM budget WHERE id = ? AND user_id = ?", (item_id, session["user_id"]))
    conn.commit()
    flash("Budget item removed.", "info")
    return redirect(url_for("budget"))


@app.route("/income", methods=["POST"])
@login_required
def set_income():
    conn = get_conn()
    uid = session["user_id"]
    now = datetime.now()
    amount = request.form.get("amount", "0")
    try:
        amount = float(amount)
    except ValueError:
        amount = 0

    existing = conn.execute(
        "SELECT id FROM income WHERE user_id = ? AND month = ? AND year = ?",
        (uid, now.month, now.year),
    ).fetchone()
    if existing:
        conn.execute("UPDATE income SET amount = ? WHERE id = ?", (amount, existing["id"]))
    else:
        conn.execute(
            "INSERT INTO income (user_id, month, year, amount) VALUES (?, ?, ?, ?)",
            (uid, now.month, now.year, amount),
        )
    conn.commit()
    flash("Monthly income updated.", "success")
    return redirect(url_for("budget"))


# ---------------------------------------------------------------------------
# Expense Tracker (SRS 3.7)
# ---------------------------------------------------------------------------

@app.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():
    conn = get_conn()
    uid = session["user_id"]

    if request.method == "POST":
        category = request.form.get("category", "").strip()
        amount = request.form.get("amount", "0")
        description = request.form.get("description", "").strip()
        date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")
        try:
            amount = float(amount)
        except ValueError:
            amount = 0
        if category and amount > 0:
            conn.execute(
                "INSERT INTO expenses (user_id, category, amount, description, date) VALUES (?, ?, ?, ?, ?)",
                (uid, category, amount, description, date),
            )
            conn.commit()
            flash("Expense recorded.", "success")
        return redirect(url_for("expenses"))

    items = conn.execute(
        "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC", (uid,)
    ).fetchall()
    return render_template("expenses.html", items=items)


@app.route("/expenses/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_expense(item_id):
    conn = get_conn()
    conn.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (item_id, session["user_id"]))
    conn.commit()
    flash("Expense deleted.", "info")
    return redirect(url_for("expenses"))


# ---------------------------------------------------------------------------
# Financial Goals (SRS 3.8)
# ---------------------------------------------------------------------------

@app.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    conn = get_conn()
    uid = session["user_id"]

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        target = request.form.get("target_amount", "0")
        deadline = request.form.get("deadline") or None
        try:
            target = float(target)
        except ValueError:
            target = 0
        if title and target > 0:
            conn.execute(
                "INSERT INTO goals (user_id, title, target_amount, saved_amount, deadline) VALUES (?, ?, ?, 0, ?)",
                (uid, title, target, deadline),
            )
            conn.commit()
            award_badge(conn, uid, "goal_created")
            flash("Financial goal created.", "success")
        return redirect(url_for("goals"))

    items = conn.execute("SELECT * FROM goals WHERE user_id = ? ORDER BY id DESC", (uid,)).fetchall()
    return render_template("goals.html", goals=items)


@app.route("/goals/<int:goal_id>/update", methods=["POST"])
@login_required
def update_goal(goal_id):
    conn = get_conn()
    uid = session["user_id"]
    added = request.form.get("added_amount", "0")
    try:
        added = float(added)
    except ValueError:
        added = 0

    goal = conn.execute(
        "SELECT * FROM goals WHERE id = ? AND user_id = ?", (goal_id, uid)
    ).fetchone()
    if goal:
        new_saved = goal["saved_amount"] + added
        conn.execute("UPDATE goals SET saved_amount = ? WHERE id = ?", (new_saved, goal_id))
        conn.commit()
        if new_saved >= goal["target_amount"]:
            award_badge(conn, uid, "goal_completed")
        flash("Goal progress updated.", "success")

    return redirect(url_for("goals"))


@app.route("/goals/<int:goal_id>/delete", methods=["POST"])
@login_required
def delete_goal(goal_id):
    conn = get_conn()
    conn.execute("DELETE FROM goals WHERE id = ? AND user_id = ?", (goal_id, session["user_id"]))
    conn.commit()
    flash("Goal removed.", "info")
    return redirect(url_for("goals"))


# ---------------------------------------------------------------------------
# Reports (SRS 3.9)
# ---------------------------------------------------------------------------

@app.route("/reports")
@login_required
def reports():
    conn = get_conn()
    uid = session["user_id"]

    expense_by_category = conn.execute(
        "SELECT category, SUM(amount) AS total FROM expenses WHERE user_id = ? GROUP BY category",
        (uid,),
    ).fetchall()

    income_total = conn.execute(
        "SELECT SUM(amount) AS total FROM income WHERE user_id = ?", (uid,)
    ).fetchone()["total"] or 0

    expense_total = conn.execute(
        "SELECT SUM(amount) AS total FROM expenses WHERE user_id = ?", (uid,)
    ).fetchone()["total"] or 0

    quiz_history = conn.execute(
        "SELECT qa.*, l.title FROM quiz_attempts qa JOIN lessons l ON qa.lesson_id = l.id "
        "WHERE qa.user_id = ? ORDER BY qa.taken_at DESC", (uid,)
    ).fetchall()

    goals_list = conn.execute("SELECT * FROM goals WHERE user_id = ?", (uid,)).fetchall()

    return render_template(
        "reports.html",
        expense_by_category=expense_by_category,
        income_total=income_total,
        expense_total=expense_total,
        quiz_history=quiz_history,
        goals=goals_list,
    )


# ---------------------------------------------------------------------------
# Profile Management (SRS 3.11)
# ---------------------------------------------------------------------------

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    conn = get_conn()
    uid = session["user_id"]

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        new_password = request.form.get("new_password", "").strip()

        if full_name:
            conn.execute("UPDATE users SET full_name = ? WHERE id = ?", (full_name, uid))
            session["full_name"] = full_name

        if new_password:
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (generate_password_hash(new_password), uid),
            )

        conn.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile"))

    user = conn.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
    return render_template("profile.html", user=user)


# ---------------------------------------------------------------------------
# Admin Panel (SRS 3.12)
# ---------------------------------------------------------------------------

@app.route("/admin")
@admin_required
def admin_dashboard():
    conn = get_conn()
    stats = {
        "total_users": conn.execute("SELECT COUNT(*) AS c FROM users WHERE role='user'").fetchone()["c"],
        "total_lessons": conn.execute("SELECT COUNT(*) AS c FROM lessons").fetchone()["c"],
        "total_quizzes": conn.execute("SELECT COUNT(*) AS c FROM quiz_questions").fetchone()["c"],
        "quiz_attempts": conn.execute("SELECT COUNT(*) AS c FROM quiz_attempts").fetchone()["c"],
    }
    return render_template("admin/dashboard.html", stats=stats)


@app.route("/admin/users")
@admin_required
def admin_users():
    conn = get_conn()
    users = conn.execute(
        "SELECT * FROM users WHERE role = 'user' ORDER BY created_at DESC"
    ).fetchall()
    return render_template("admin/users.html", users=users)


@app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    conn = get_conn()
    conn.execute("DELETE FROM users WHERE id = ? AND role = 'user'", (user_id,))
    conn.commit()
    flash("User account removed.", "info")
    return redirect(url_for("admin_users"))


@app.route("/admin/lessons", methods=["GET", "POST"])
@admin_required
def admin_lessons():
    conn = get_conn()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        content = request.form.get("content", "").strip()
        if title and category and content:
            max_order = conn.execute("SELECT MAX(order_index) AS m FROM lessons").fetchone()["m"] or 0
            conn.execute(
                "INSERT INTO lessons (title, category, content, order_index) VALUES (?, ?, ?, ?)",
                (title, category, content, max_order + 1),
            )
            conn.commit()
            flash("Lesson added.", "success")
        return redirect(url_for("admin_lessons"))

    lessons = conn.execute("SELECT * FROM lessons ORDER BY order_index").fetchall()
    return render_template("admin/lessons.html", lessons=lessons)


@app.route("/admin/lessons/<int:lesson_id>/delete", methods=["POST"])
@admin_required
def admin_delete_lesson(lesson_id):
    conn = get_conn()
    conn.execute("DELETE FROM quiz_questions WHERE lesson_id = ?", (lesson_id,))
    conn.execute("DELETE FROM progress WHERE lesson_id = ?", (lesson_id,))
    conn.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
    conn.commit()
    flash("Lesson deleted.", "info")
    return redirect(url_for("admin_lessons"))


@app.route("/admin/quizzes", methods=["GET", "POST"])
@admin_required
def admin_quizzes():
    conn = get_conn()
    lessons = conn.execute("SELECT * FROM lessons ORDER BY order_index").fetchall()

    if request.method == "POST":
        lesson_id = request.form.get("lesson_id")
        question = request.form.get("question", "").strip()
        option_a = request.form.get("option_a", "").strip()
        option_b = request.form.get("option_b", "").strip()
        option_c = request.form.get("option_c", "").strip()
        option_d = request.form.get("option_d", "").strip()
        correct_option = request.form.get("correct_option")

        if all([lesson_id, question, option_a, option_b, option_c, option_d, correct_option]):
            conn.execute(
                """INSERT INTO quiz_questions
                   (lesson_id, question, option_a, option_b, option_c, option_d, correct_option)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (lesson_id, question, option_a, option_b, option_c, option_d, correct_option),
            )
            conn.commit()
            flash("Quiz question added.", "success")
        return redirect(url_for("admin_quizzes"))

    questions = conn.execute(
        "SELECT q.*, l.title AS lesson_title FROM quiz_questions q "
        "JOIN lessons l ON q.lesson_id = l.id ORDER BY q.lesson_id"
    ).fetchall()
    return render_template("admin/quizzes.html", lessons=lessons, questions=questions)


@app.route("/admin/quizzes/<int:question_id>/delete", methods=["POST"])
@admin_required
def admin_delete_question(question_id):
    conn = get_conn()
    conn.execute("DELETE FROM quiz_questions WHERE id = ?", (question_id,))
    conn.commit()
    flash("Quiz question deleted.", "info")
    return redirect(url_for("admin_quizzes"))


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print("No database found - creating and seeding one now...")
        from database import init_db, seed_db
        init_db()
        seed_db()
    app.run(debug=True)
