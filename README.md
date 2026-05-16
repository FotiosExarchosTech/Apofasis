# Apofasis — AI E-Shop Assistant

An AI-powered shopping assistant system built for e-commerce, designed to chat with customers in real time and help them find the product that best fits their needs. Originally developed for the **Athens AI Hackathon** (we never took place as due to a high participation rate we were rejected since all the seats were full).

The system is intentionally designed so that **non-programmers can fully customize the AI's behavior as they would with an employee** by editing a plain text file — no code changes required.

---

## About

Traditional e-shop search bars require the customer to know exactly what they want. **Apofasis** takes a different approach: it holds a conversation, understands the customer's level of expertise and needs, queries the product database intelligently, and then recommends the best matching product with a human-friendly explanation.

The pipeline works in three steps on every message:

1. **Filter extraction** — A silent LLM call parses the customer's message into structured search filters (`keyword`, `max_price`, `product_type`)
2. **Database search** — The filters are used to query a SQLite product database
3. **Response generation** — A second LLM call receives the customer's message, the matching products, the full conversation history, and the plain-text instructions file, then generates the final reply

---

## Features

### AI Chat
- Conversational product recommendations powered by an LLM (via Ollama)
- Maintains full **conversation history** across the session for context-aware replies
- Responds in **the same language the customer writes in** (Greek, English, etc.)
- Adapts tone and detail level based on detected customer expertise — avoids technical jargon with beginners, goes deep with enthusiasts
- **Streaming support** — responses are printed token-by-token in terminal mode

### Intelligent Two-Stage Product Search
The LLM first silently extracts structured filters from the customer's free-text message, then queries the database using:
- **Keyword** — matched against title, description, and brand (`LIKE` search)
- **Max price** — upper price bound filter
- **Product type** — category filter (LAPTOP, PHONE, GPU, CPU, etc.)

### Plain-Text Instruction System
The AI's entire behavior is controlled by `back_end/Instructions.txt` — a plain English text file that any non-technical person can read and edit. It defines:
- What the shop sells
- How to handle beginners vs. experts
- What to do when no products are found
- Tone and response length guidelines
- Language mirroring rules

No code changes are needed to repurpose the assistant for a different shop or product category — just rewrite the instructions file.

### Embeddable Chat Widget
A self-contained chat UI (`fake_site/`) designed to embed into any existing website:
- Dark themed (Catppuccin Mocha color palette)
- Animated typing indicator (three bouncing dots) while waiting for the AI
- Auto-resizing textarea (expands up to 120px, then scrolls)
- Send on `Enter`, new line on `Shift+Enter`
- One-click chat clear button (resets to welcome message)
- Fully responsive — works on mobile screens

### Product Import Utility
`Json_to_add_function_converter.py` converts JavaScript-style product objects (copy-pasted from any e-shop) into `add_product()` calls ready for the database. It handles:
- JS unquoted keys → valid JSON
- Single quotes → double quotes
- Trailing commas removal
- Price string → integer (strips `€`, `$`, `.`)
- Greek unit translation (`Ώρες` → `Hours`)
- Random stock quantity generation for testing

---

## Project Structure

```
Apofasis/
├── back_end/
│   ├── chatbot_llama_cloud_server.py   # Main Flask server: /api/chat endpoint, LLM calls, DB search
│   ├── database_handler.py             # SQLite schema init + full demo product catalogue inserts
│   ├── Instructions.txt                # Plain-text AI behavior rules (editable by non-programmers)
│   └── test.py                         # Minimal test server used during development
│
├── fake_site/
│   ├── ui.html                         # Standalone chat widget (embeddable)
│   ├── ui.css                          # Chat widget styles (dark theme, responsive)
│   ├── ui.js                           # Chat widget logic (fetch, message rendering, auto-resize)
│   ├── index.html                      # Demo e-shop homepage with embedded chat widget
│   └── product.html                    # Demo product detail page
│
├── Json_to_add_function_converter.py   # Utility: converts JS product objects → DB insert calls
├── products.txt                        # Raw product data (JS object format) for the converter
└── Dimitris.db                         # SQLite database
```

---

## Database Schema

```sql
CREATE TABLE Products (
    productId   INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT,
    type        TEXT,       -- e.g. LAPTOP, PHONE, GPU, CPU, AUDIO, MONITOR
    description TEXT,       -- flat spec string, e.g. "cpu: i7 ram: 16GB screen: 15.6"
    price       REAL,
    brand       TEXT,
    image       TEXT,       -- product image URL
    quantity    INTEGER DEFAULT 0
);

CREATE TABLE Reviews (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id  INTEGER NOT NULL,
    comment     TEXT NOT NULL,
    FOREIGN KEY(product_id) REFERENCES Products(id)
);
```

### Demo Product Catalogue

| Category | Example Products |
|----------|-----------------|
| `LAPTOP` | MacBook Air M3, HP Omen 16, Legion Pro 5, ROG Zephyrus G14, XPS 13 Plus |
| `PHONE` | Galaxy S24 Ultra, iPhone 15 Pro Max, Pixel 8 Pro, Xiaomi 14 Ultra, OnePlus 12 |
| `AUDIO` | Sony WH-1000XM5, Bose QC Ultra, AirPods Pro 2, JBL Flip 6, Nothing Ear (2) |
| `GPU` | RTX 4060 8GB, RTX 4070 12GB, Radeon RX 7800 XT |
| `CPU` | Ryzen 5 5600X, Ryzen 7 5800X, Core i5-12600K, Core i7-12700K |
| `RAM` | Corsair Vengeance 16GB DDR4, G.Skill Trident Z Neo 32GB |
| `STORAGE` | Samsung 970 EVO Plus 1TB NVMe, WD Blue 2TB SATA |
| `MONITOR` | LG UltraGear 27GL850, Samsung Odyssey G5 32 |
| `KEYBOARD` | Corsair K70 RGB MK.2, Logitech G513 Carbon |
| `MICE` | Logitech G502 HERO, Razer DeathAdder V2 |
| `PC` | Pre-built gaming desktops and a workstation |

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, Flask, Flask-CORS |
| LLM | Ollama (`gpt-oss:20b-cloud`) via cloud API |
| Database | SQLite3 |
| Frontend | Vanilla HTML, CSS, JavaScript (no frameworks) |

---

## Getting Started

### Prerequisites
- Python 3.10+
- An Ollama API key, or a locally running Ollama instance (though unless your hardware is powerfull i would not recomend it)

### Install Dependencies

```bash
pip install flask flask-cors ollama
```

### Configure the LLM

Open `back_end/chatbot_llama_cloud_server.py` and update the client:

```python
# Cloud (current setup)
client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

# OR local Ollama instance
client = Client(host="http://localhost:11434")
```

Change the model name to match what you have available:

```python
model="llama3"    # or mistral, gemma, phi3, etc.
```

### Set Up the Database

```bash
cd Apofasis
python back_end/database_handler.py
```

This creates `Dimitris.db` and populates it with the full demo product catalogue.

### Run the Server

```bash
python back_end/chatbot_llama_cloud_server.py
```

The API will be available at `http://127.0.0.1:5000`.

### Open the Chat Widget

Open `fake_site/index.html` in a browser. The widget connects to the running Flask server automatically.

---

## Customizing the AI (No Code Required)

The AI's entire personality, product knowledge, and conversation rules live in **`back_end/Instructions.txt`**. To change how it behaves:

1. Open `Instructions.txt` in any text editor
2. Edit the sections you want to change:
   - `WHAT WE SELL` — list your actual product categories
   - `YOUR BEHAVIOR GUIDELINES` — add, remove, or rewrite rules in plain language
3. Save the file and restart the server

**Example:** to repurpose the assistant for a clothing store, update `WHAT WE SELL` to list your clothing categories and adjust the behavior rules to ask about size, style, and occasion instead of specs. No Python knowledge required.

---

## API Reference

### `POST /api/chat`

**Request:**
```json
{
  "question": "I need a laptop for gaming under 1500€",
  "context": "optional page description passed from the e-shop",
  "model": "gpt-oss:20b-cloud"
}
```

**Response:**
```json
{
  "reply": "For gaming under 1500€, I'd recommend the HP Omen 16..."
}
```

---

## Adding Products from Another E-Shop

Paste JavaScript product objects into `products.txt`, then run:

```bash
python Json_to_add_function_converter.py
```

The script outputs ready-to-use `add_product(...)` calls you can paste into `database_handler.py` and run.

---

## Authors

**Fotios Exarchos (back end and simple improovements on front end)** & **Stelios Kotsalis (front end)** *(collaborator)*  
Built as a submission attempt for the Athens AI Hackathon.

---
