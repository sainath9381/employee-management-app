from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )


@app.route("/")
def home():
    return jsonify({"message": "Employee Management Backend Running"})


@app.route("/health")
def health():
    return jsonify({"status": "UP"})


# =========================
# GET ALL EMPLOYEES
# =========================
@app.route("/employees", methods=["GET"])
def get_employees():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(employees)


# =========================
# GET SINGLE EMPLOYEE
# =========================
@app.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM employees WHERE id=%s",
        (id,)
    )

    employee = cursor.fetchone()

    cursor.close()
    conn.close()

    if employee:
        return jsonify(employee)

    return jsonify({"message": "Employee not found"}), 404


# =========================
# ADD EMPLOYEE
# =========================
@app.route("/employees", methods=["POST"])
def add_employee():

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO employees(name,email,department,salary)
        VALUES(%s,%s,%s,%s)
        """,
        (
            data["name"],
            data["email"],
            data["department"],
            data["salary"]
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Employee Added Successfully"}), 201


# =========================
# UPDATE EMPLOYEE
# =========================
@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE employees
        SET
        name=%s,
        email=%s,
        department=%s,
        salary=%s
        WHERE id=%s
        """,
        (
            data["name"],
            data["email"],
            data["department"],
            data["salary"],
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Employee Updated Successfully"})


# =========================
# DELETE EMPLOYEE
# =========================
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Employee Deleted Successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)