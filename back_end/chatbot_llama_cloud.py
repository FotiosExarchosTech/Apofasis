from ollama import Client
import json
import sqlite3 as sql

# =========================
# DATABASE SETUP
# =========================

database = sql.connect('Dimitris.db')
cursor = database.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    productId INTEGER PRIMARY KEY AUTOINCREMENT,
    quantity INTEGER,
    type TEXT,
    kind TEXT,
    title TEXT,
    description TEXT,
    price REAL
)
''')

database.commit()

# =========================
# OLLAMA FUNCTIONS
# =========================

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + "Your ollama api key."}
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
    "product_kind": string or null
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
            "product_kind": None
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

    instructions = open("Instructions.txt", "r")

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

    return answer

# =========================
# MAIN LOOP
# =========================

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
