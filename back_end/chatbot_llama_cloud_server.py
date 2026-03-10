import os # Στελιο καλο θα ειναι αν χρησιμοποιησεις κατι απο αυτην την βιβλιοθηκη να εισαι υπερβολικα προσεκτικος γιατι μπορει να κανεις χοντρη βλακεια.

from ollama import Client
from flask_cors import CORS
from flask import Flask, request, jsonify 
import json
import sqlite3 as sql

# =========================
# FOR THE SERVER
# =========================

app = Flask(__name__)
CORS(app)

# =========================
# DATABASE SETUP
# =========================

def get_database():
    return sql.connect('Dimitris.db')

# =========================
# OLLAMA FUNCTIONS
# =========================

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + "2e78e803123a4b3cb25aa584cd694177.QMXq3Z-g4mMbPVnl4xgHqjV6"}
)

def ask_llm(prompt):
    try:
        stream = client.chat(
            model="gpt-oss:20b-cloud", # The model we will use. It can change.
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        full_response = ""

        print("Assistant: ", end="", flush=True)

        for chunk in stream:
            content = chunk["message"]["content"]
            print(content, end="", flush=True)
            full_response += content

        print()  # newline after streaming

        return full_response

    except Exception as e:
        print("ERROR:", e)
        return "AI ERROR"
    
def ask_llm_silent(prompt):
    try:
        response = client.chat(
            model="gpt-oss:20b-cloud",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        print("ERROR:", e)
        return ""

# =========================
# PRODUCT SEARCH FUNCTION
# =========================

def search_products(keyword=None, max_price=None, product_type=None):
    database = get_database()
    cursor = database.cursor()

    query = """
    SELECT title, description, price, quantity, brand
    FROM Products
    WHERE 1=1
    """
    params = []

    if keyword:
        query += " AND (title LIKE ? OR description LIKE ? OR brand LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])

    if max_price:
        query += " AND price <= ?"
        params.append(max_price)

    if product_type:
        query += " AND type LIKE ?"
        params.append(f"%{product_type}%")

    cursor.execute(query, params)
    results = cursor.fetchall()
    database.close()

    return results

# =========================
# EXTRACT FILTERS USING OLLAMA
# =========================

def extract_filters(user_input):

    prompt = f"""
    Extract product search filters from this message.

    Message: "{user_input}"

    Return ONLY valid JSON:
    {{
    "keyword": string or null,
    "max_price": number or null,
    "product_type": string or null,
    }}

    Do not explain. Return JSON only.
    """

    response_text = ask_llm_silent(prompt)

    try:
        return json.loads(response_text)
    except:
        return {
            "keyword": None,
            "max_price": None,
            "product_type": None,
        }

# =========================
# FINAL ANSWER USING OLLAMA
# =========================

conversation_history = ""

def generate_answer(user_input, products):

    global conversation_history

    total_price = sum([p[2] for p in products])

    formatted_products = "NO PRODUCTS FOUND"

    if not products:
        formatted_products = "NO PRODUCTS FOUND"
    else:
        formatted_products = "\n".join([f"- {p[0]} | ${p[2]} | Stock: {p[3]}" for p in products])

    instructions = open("back_end\\Instructions.txt", "r")

    prompt = f"""
    Customer question:
    {user_input}

    Available products:
    {formatted_products}

    Conversation so far:
    {conversation_history}

    Total price: 
    {total_price}

    Instructions:
    {instructions.read()}
    
    """

    answer = ask_llm(prompt)

    conversation_history += f"\nAssistant: {answer}"

    return jsonify({"reply": answer})

@app.route("/api/chat", methods=["POST"])
def chat():
    global conversation_history

    data = request.get_json()

    if not data:
        return jsonify({"reply": "Invalid request"}), 400

    user_input = data.get("question", "")
    page_context = data.get("context", "")
    model_name = data.get("model", "gpt-oss:20b-cloud")

    if not user_input:
        return jsonify({"reply": "Empty message"}), 400

    # Step 1: Extract filters
    filters = extract_filters(user_input)

    # Step 2: Search database
    products = search_products(
        keyword=filters.get("keyword"),
        max_price=filters.get("max_price"),
        product_type=filters.get("product_type"),
    )

    # Format products
    if not products:
        formatted_products = "NO PRODUCTS FOUND"
    else:
        formatted_products = "\n".join(
            [f"- {p[0]} | ${p[2]} | Stock: {p[3]}" for p in products]
        )

    total_price = sum([p[2] for p in products]) if products else 0

    # Load instructions safely
    with open("back_end/Instructions.txt", "r", encoding="utf-8") as f:
        instructions = f.read()

    prompt = f"""
    Customer question:
    {user_input}

    Website context:
    {page_context}

    Available products:
    {formatted_products}

    Conversation so far:
    {conversation_history}

    Total price:
    {total_price}

    Instructions:
    {instructions}
    """

    answer = ask_llm(prompt)

    conversation_history += f"\nCustomer: {user_input}"
    conversation_history += f"\nAssistant: {answer}"

    return jsonify({"reply": answer})


# =========================
# MAIN LOOP
# =========================

if __name__ == "__main__":
    app.run(debug=True, port=5000)




#Terminal loop
'''
print("Shop Assistant Ready (type 'exit' to quit)\n")

while True:
    user_input = input("Customer: ")

    if user_input.lower() == "exit":
        break

    # Step 1: Extract filters
    filters = extract_filters(user_input)

    # Step 2: Search database
    products = search_products(
        keyword=filters.get("keyword"),
        max_price=filters.get("max_price"),
        product_type=filters.get("product_type"),
        product_kind=filters.get("product_kind")
    )

    conversation_history += f"\nCustomer: {user_input}"

    # Step 3: Generate answer
    generate_answer(user_input, products)
    print()
'''