from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# ------------------------------------
# Create Flask App
# ------------------------------------

app = Flask(__name__)
CORS(app)

# ------------------------------------
# Connect to MySQL
# ------------------------------------

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # Put your MySQL password here if you have one
        database="financewise"
    )

    cursor = db.cursor(dictionary=True)
    print("Connected to MySQL Successfully!")

except mysql.connector.Error as err:
    print("Database Connection Error:", err)

# =====================================================
# SIGNUP
# =====================================================

@app.route("/signup", methods=["POST"])
def signup():

    try:

        data = request.get_json()

        fullname = data["fullname"]
        email = data["email"]
        password = data["password"]
        dob = data["dob"]
        age = data["age"]
        gender = data["gender"]
        occupation = data["occupation"]
        goal = data["goal"]

        # Check if email already exists

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            return jsonify({
                "success": False,
                "message": "Email already registered."
            })

        # Encrypt password

        hashed_password = generate_password_hash(password)

        sql = """
        INSERT INTO users
        (
        fullname,
        email,
        password,
        dob,
        age,
        gender,
        occupation,
        goal
        )

        VALUES
        (
        %s,%s,%s,%s,%s,%s,%s,%s
        )
        """

        values = (
            fullname,
            email,
            hashed_password,
            dob,
            age,
            gender,
            occupation,
            goal
        )

        cursor.execute(sql, values)
        db.commit()

        return jsonify({
            "success": True,
            "message": "Account Created Successfully!"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })
    # =====================================================
# LOGIN
# =====================================================

@app.route("/login", methods=["POST"])
def login():

    try:

        data = request.get_json()

        email = data["email"]
        password = data["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if user:

            if check_password_hash(user["password"], password):

                return jsonify({
                    "success": True,
                    "message": "Login Successful!"
                })

            else:

                return jsonify({
                    "success": False,
                    "message": "Incorrect Password!"
                })

        else:

            return jsonify({
                "success": False,
                "message": "Email not found!"
            })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })
    # =====================================================
# FORGOT PASSWORD
# =====================================================

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    try:
        data = request.get_json()
        email = data["email"]
        # 1. Check if the email exists in the database
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            # 2. Logic to send a reset link or reset the password goes here
            return jsonify({
                "success": True,
                "message": "Password reset link sent to your email!"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Email not found!"
            })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


# =====================================================
# HOME ROUTE
# =====================================================

@app.route("/")
def home():
    return "FinanceWise Backend is Running!"


# =====================================================
# RUN APP
# =====================================================

    # =====================================================
# GET SAVINGS DATA
# =====================================================

@app.route("/get-savings", methods=["GET"])
def get_savings():
    try:
        # Assuming you identify the user via email or session. 
        # For simplicity, we can fetch a specific user's data or structure it accordingly.
        # Replace 'user@example.com' with dynamic session data in a full implementation.
        email = request.args.get("email") 
        
        cursor.execute("SELECT income, current_savings, savings_goal, monthly_budget, monthly_spent FROM users WHERE email=%s", (email,))
        user_data = cursor.fetchone()

        if user_data:
            return jsonify({
                "success": True,
                "income": user_data["income"] or 0,
                "current_savings": user_data["current_savings"] or 0,
                "savings_goal": user_data["savings_goal"] or 200000,
                "monthly_budget": user_data["monthly_budget"] or 0,
                "monthly_spent": user_data["monthly_spent"] or 0
            })
        else:
            return jsonify({"success": False, "message": "User not found"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
if __name__ == "__main__":
    app.run(debug=True)
