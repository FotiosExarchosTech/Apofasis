from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sqlite3 as sql
from ollama import Client
import os

app = Flask(__name__)
CORS(app)  # allow frontend to connect

# =========================
# DATABASE
# =========================

database = sql.connect('Dimitris.db', check_same_thread=False)
cursor = database.cursor()

# =========================
# OLLAMA
# =========================

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

conversation_history = ""

# =========================
# FUNCTIONS (reuse yours)
# =========================

def ask_llm(prompt):
    response = client.chat(
        model="gpt-oss:20b-cloud",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

def search_products(keyword=None, max_price=None, product_type=None, product_kind=None):
    query = """
    SELECT title, description, price, quantity
    FROM Products
    WHERE 1=1
    """
    params = []

    if keyword:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])

    if max_price:
        query += " AND price <= ?"
        params.append(max_price)

    if product_type:
        query += " AND type LIKE ?"
        params.append(f"%{product_type}%")
    
    if product_kind:
        query += " AND kind LIKE ?"
        params.append(f"%{product_kind}%")

    cursor.execute(query, params)
    return cursor.fetchall()

# =========================
# API ROUTE
# =========================

@app.route("/api/chat", methods=["POST"])
def chat():

    global conversation_history

    data = request.json
    user_input = data.get("question")

    # Example: simple search
    products = search_products(keyword=user_input)

    formatted_products = "\n".join(
        [f"- {p[0]} | ${p[2]} | Stock: {p[3]}" for p in products]
    ) if products else "NO PRODUCTS FOUND"

    prompt = f"""
    Customer question:
    {user_input}

    Available products:
    {formatted_products}

    Conversation:
    {conversation_history}
    """

    answer = ask_llm(prompt)

    conversation_history += f"\nCustomer: {user_input}"
    conversation_history += f"\nAssistant: {answer}"

    return jsonify({"reply": answer})

# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":
    app.run(debug=True, port=5000)