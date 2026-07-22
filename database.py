"""
database.py
Handles SQLite connection, schema initialization, and demo data seeding
for the FinanceWise platform.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "financewise.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


def get_db():
    """Return a new SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """(Re)create all tables from schema.sql. Wipes existing data."""
    conn = get_db()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def seed_db():
    """Insert demo/admin data so the app is usable immediately after setup."""
    conn = get_db()
    cur = conn.cursor()

    # --- Admin account ---
    cur.execute(
        "INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, ?)",
        ("System Admin", "admin@financewise.com", generate_password_hash("admin123"), "admin"),
    )

    # --- Demo user account ---
    cur.execute(
        "INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, ?)",
        ("Demo User", "demo@financewise.com", generate_password_hash("demo123"), "user"),
    )
    demo_user_id = cur.lastrowid

    # --- Lessons (Financial Learning Modules, SRS 3.4) ---
    lessons = [
        ("Budgeting Basics", "Budgeting",
         "A budget is a plan for how you will spend your income each month. "
         "The most common approach is the 50/30/20 rule: 50% of income for needs, "
         "30% for wants, and 20% for savings or debt repayment. Tracking your spending "
         "against a budget helps you avoid overspending and build good financial habits.", 1),
        ("The Power of Saving", "Saving",
         "Saving means setting aside part of your income instead of spending it. "
         "An emergency fund covering 3-6 months of expenses protects you from unexpected "
         "costs like medical bills or job loss. Automating transfers to a savings account "
         "right after payday makes saving consistent and effortless.", 2),
        ("Introduction to Investing", "Investing",
         "Investing means putting money into assets like stocks, mutual funds, or fixed "
         "deposits with the goal of growing it over time. Compound interest means your "
         "returns start earning their own returns, so starting early -- even with small "
         "amounts -- has a big impact over the long run. Investing carries risk, so "
         "diversification (spreading money across different assets) helps manage it.", 3),
        ("Financial Planning for the Future", "Planning",
         "Financial planning means setting short-term and long-term goals (like buying a "
         "laptop, or retirement) and creating a roadmap to achieve them. This includes "
         "budgeting, saving, investing, and managing debt together. Reviewing your plan "
         "regularly helps you adjust as your income and priorities change.", 4),
    ]
    cur.executemany(
        "INSERT INTO lessons (title, category, content, order_index) VALUES (?, ?, ?, ?)",
        lessons,
    )

    # --- Quiz questions (SRS 3.5) ---
    quiz_data = [
        (1, "What does the 50/30/20 rule allocate to savings/debt repayment?",
         "50%", "30%", "20%", "10%", "C"),
        (1, "What is the main purpose of a monthly budget?",
         "To increase income", "To plan spending", "To avoid taxes", "To get a loan", "B"),
        (2, "How many months of expenses should an emergency fund ideally cover?",
         "3-6 months", "1 week", "10 years", "1 month", "A"),
        (2, "What is the easiest way to save consistently?",
         "Saving whatever is left at month end", "Automating transfers after payday",
         "Borrowing to save", "Skipping savings some months", "B"),
        (3, "What is compound interest?",
         "Interest only on the original amount", "Interest on interest already earned",
         "A one-time bonus", "A type of loan", "B"),
        (3, "Why is diversification important when investing?",
         "It guarantees profit", "It reduces risk by spreading investments",
         "It avoids all taxes", "It is required by law", "B"),
        (4, "What should a good financial plan include?",
         "Only investing", "Only budgeting", "Budgeting, saving, investing and debt management",
         "Only saving", "C"),
        (4, "Why should a financial plan be reviewed regularly?",
         "It's legally required", "Income and priorities can change over time",
         "To increase debt", "It never needs review", "B"),
    ]
    cur.executemany(
        """INSERT INTO quiz_questions
           (lesson_id, question, option_a, option_b, option_c, option_d, correct_option)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        quiz_data,
    )

    # --- Badges (Achievement System, SRS 3.10) ---
    badges = [
        ("First Steps", "Completed your first lesson", "🎓", "lesson_complete_1"),
        ("Knowledge Seeker", "Completed all learning modules", "📚", "lesson_complete_all"),
        ("Quiz Whiz", "Scored 100% on a quiz", "🏆", "quiz_perfect"),
        ("Budget Master", "Created your first monthly budget", "💰", "budget_created"),
        ("Goal Setter", "Created your first financial goal", "🎯", "goal_created"),
        ("Saver", "Reached 100% of a savings goal", "⭐", "goal_completed"),
    ]
    cur.executemany(
        "INSERT INTO badges (name, description, icon, criteria) VALUES (?, ?, ?, ?)",
        badges,
    )

    # --- Some demo financial data for the demo user ---
    cur.execute(
        "INSERT INTO income (user_id, month, year, amount) VALUES (?, ?, ?, ?)",
        (demo_user_id, 7, 2026, 20000),
    )
    cur.executemany(
        "INSERT INTO expenses (user_id, category, amount, description, date) VALUES (?, ?, ?, ?, ?)",
        [
            (demo_user_id, "Food", 3500, "Groceries and dining", "2026-07-05"),
            (demo_user_id, "Transport", 1200, "Bus pass + fuel", "2026-07-06"),
            (demo_user_id, "Entertainment", 800, "Movies", "2026-07-10"),
        ],
    )
    cur.execute(
        "INSERT INTO goals (user_id, title, target_amount, saved_amount, deadline) VALUES (?, ?, ?, ?, ?)",
        (demo_user_id, "New Laptop", 50000, 12000, "2026-12-31"),
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    seed_db()
    print(f"Database created and seeded at {DB_PATH}")
