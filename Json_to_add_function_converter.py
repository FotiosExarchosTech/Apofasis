import re
import ast
import random

def convert_product(js_object_string):
    cleaned = js_object_string.strip()

    # 1️⃣ Replace JS-style keys ONLY when they are actual object keys
    cleaned = re.sub(r'([{,]\s*)(\w+):', r'\1"\2":', cleaned)

    # 2️⃣ Replace single quotes with double quotes
    cleaned = cleaned.replace("'", '"')

    # 3️⃣ Remove trailing commas
    cleaned = re.sub(r',\s*}', '}', cleaned)
    cleaned = re.sub(r',\s*]', ']', cleaned)

    # 4️⃣ Safely convert to dict
    product = ast.literal_eval(cleaned)

    # 5️⃣ Extract fields
    title = product["title"]
    category = product["category"].upper().rstrip("S")
    brand = product["brand"].upper()
    image = product["image"]

    # 6️⃣ Convert price
    price_number = int(
        product["price"]
        .replace("€", "")
        .replace("$", "")
        .replace(".", "")
        .strip()
    )

    # 7️⃣ Flatten specs
    specs_parts = []
    for key, value in product["specs"].items():
        value = value.replace("Ώρες", "Hours")
        specs_parts.append(f"{key}: {value}")

    specs_string = " ".join(specs_parts)

    # 8️⃣ Quantity
    quantity = random.randint(0, 100)

    return f'add_product("{title}", "{category}", "{specs_string}", {price_number}, "{brand}", "{image}", {quantity})'

def convert_multiple_products(js_objects_string):
    cleaned = js_objects_string.strip()

    # 🔥 Wrap in list if not already
    if not cleaned.startswith("["):
        cleaned = "[" + cleaned.rstrip(",") + "]"

    # Replace JS-style keys
    cleaned = re.sub(r'([{,]\s*)(\w+):', r'\1"\2":', cleaned)

    # Replace single quotes
    cleaned = cleaned.replace("'", '"')

    # Remove trailing commas
    cleaned = re.sub(r',\s*}', '}', cleaned)
    cleaned = re.sub(r',\s*]', ']', cleaned)

    products = ast.literal_eval(cleaned)

    output = []

    for product in products:
        title = product["title"]
        category = product["category"].upper().rstrip("S")
        brand = product["brand"].upper()
        image = product["image"]

        price_number = int(
            product["price"]
            .replace("€", "")
            .replace(".", "")
            .strip()
        )

        specs_parts = []
        for key, value in product["specs"].items():
            value = value.replace("Ώρες", "Hours")
            specs_parts.append(f"{key}: {value}")

        specs_string = " ".join(specs_parts)

        quantity = random.randint(0, 100)

        output.append(
            f'add_product("{title}", "{category}", "{specs_string}", {price_number}, "{brand}", "{image}", {quantity})'
        )

    return "\n".join(output)


with open("products.txt", "r", encoding="utf-8") as file:
    content = file.read()

    print(convert_multiple_products(content))