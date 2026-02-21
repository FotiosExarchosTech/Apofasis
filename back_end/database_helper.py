#Stelio don't run this unless the database is empty.

# database_helper.py
import sqlite3 as sql

DB_NAME = "Dimitris.db"

def init():
    database = sql.connect(DB_NAME)

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
    )'''
    )
    database.commit()

def add_product(quantity, type_, kind, title, description, price):
    """Add a product to the existing Dimitris.db database"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Products (quantity, type, kind, title, description, price)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (quantity, type_, kind, title, description, price))

    connection.commit()
    connection.close()
    print(f"✅ Added product: {title}")


# =========================
# GPUS
# =========================
add_product(10, "Electronics", "GPU", "NVIDIA RTX 4060 8GB", "Mid-range gaming GPU, great for 1080p and 1440p gaming.", 329.99)
add_product(7, "Electronics", "GPU", "NVIDIA RTX 4070 12GB", "High-performance GPU, excellent for 1440p and entry-level 4K gaming.", 599.99)
add_product(5, "Electronics", "GPU", "AMD Radeon RX 7800 XT", "Powerful GPU for gaming at 1440p and 4K, supports ray tracing.", 549.99)

# =========================
# CPUS
# =========================
add_product(8, "Electronics", "CPU", "AMD Ryzen 5 5600X", "6-core processor, great for gaming and multitasking.", 199.99)
add_product(6, "Electronics", "CPU", "AMD Ryzen 7 5800X", "8-core high-performance CPU, excellent for gaming and productivity.", 299.99)
add_product(5, "Electronics", "CPU", "Intel Core i5-12600K", "10-core Intel CPU, strong single-threaded and multi-threaded performance.", 269.99)
add_product(4, "Electronics", "CPU", "Intel Core i7-12700K", "12-core CPU for gaming and content creation, excellent all-rounder.", 399.99)

# =========================
# RAM
# =========================
add_product(15, "Electronics", "RAM", "Corsair Vengeance 16GB DDR4 3200MHz", "Reliable DDR4 RAM kit, ideal for gaming and productivity.", 79.99)
add_product(10, "Electronics", "RAM", "G.Skill Trident Z 32GB DDR4 3600MHz", "High-speed RAM kit for gaming and heavy multitasking.", 149.99)

# =========================
# STORAGE
# =========================
add_product(12, "Electronics", "SSD", "Samsung 970 EVO Plus 1TB NVMe", "Fast NVMe SSD for quick boot times and application loading.", 89.99)
add_product(8, "Electronics", "SSD", "Western Digital Blue 2TB SATA", "Reliable SATA SSD for mass storage and daily usage.", 119.99)

# =========================
# MONITORS
# =========================
add_product(10, "Electronics", "Monitor", "LG UltraGear 27GL850 27-inch", "27-inch 1440p 144Hz gaming monitor with IPS panel.", 399.99)
add_product(7, "Electronics", "Monitor", "Samsung Odyssey G5 32-inch", "32-inch curved 1440p 165Hz gaming monitor for immersive gameplay.", 349.99)

# =========================
# KEYBOARDS
# =========================
add_product(20, "Electronics", "Keyboard", "Corsair K70 RGB", "Mechanical gaming keyboard with customizable RGB lighting.", 129.99)
add_product(15, "Electronics", "Keyboard", "Logitech G513", "High-quality mechanical keyboard, excellent for gaming and typing.", 119.99)

# =========================
# MICE
# =========================
add_product(25, "Electronics", "Mouse", "Logitech G502 HERO", "Precision gaming mouse with programmable buttons and adjustable DPI.", 59.99)
add_product(20, "Electronics", "Mouse", "Razer DeathAdder V2", "Ergonomic gaming mouse, perfect for FPS and MOBA games.", 69.99)

# =========================
# HEADPHONES
# =========================
add_product(15, "Electronics", "Headphones", "HyperX Cloud II", "Comfortable gaming headset with 7.1 virtual surround sound.", 99.99)
add_product(10, "Electronics", "Headphones", "Sony WH-1000XM5", "High-end wireless noise-cancelling headphones, great for music and calls.", 399.99)
add_product(10, "Electronics", "Headphones", "Apple AirPods Pro 2", "Wireless earbuds with active noise cancellation and transparency mode.", 249.99)

# =========================
# PHONES
# =========================
add_product(8, "Electronics", "Phone", "iPhone 14", "Latest Apple iPhone with excellent camera and performance.", 799.99)
add_product(10, "Electronics", "Phone", "Samsung Galaxy S23", "High-end Android smartphone with great display and camera.", 749.99)
add_product(12, "Electronics", "Phone", "Google Pixel 7", "Android smartphone with stock OS and excellent camera AI.", 599.99)