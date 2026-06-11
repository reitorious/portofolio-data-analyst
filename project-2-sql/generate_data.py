# generate_data.py
import sqlite3, random, os
from datetime import date, timedelta

random.seed(42)  # supaya hasil selalu sama tiap dijalankan

DB = "delivery.db"
if os.path.exists(DB):
    os.remove(DB)  # mulai bersih tiap kali generate ulang

conn = sqlite3.connect(DB)
cur = conn.cursor()

# ---------- 1. Buat skema (CREATE TABLE) ----------
cur.executescript("""
CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city          TEXT NOT NULL,
    signup_date   TEXT NOT NULL,
    channel       TEXT NOT NULL
);
CREATE TABLE restaurants (
    restaurant_id   INTEGER PRIMARY KEY,
    restaurant_name TEXT NOT NULL,
    city            TEXT NOT NULL,
    cuisine         TEXT NOT NULL,
    commission_rate REAL NOT NULL
);
CREATE TABLE drivers (
    driver_id    INTEGER PRIMARY KEY,
    driver_name  TEXT NOT NULL,
    vehicle_type TEXT NOT NULL,
    city         TEXT NOT NULL,
    join_date    TEXT NOT NULL
);
CREATE TABLE orders (
    order_id         INTEGER PRIMARY KEY,
    customer_id      INTEGER NOT NULL REFERENCES customers(customer_id),
    restaurant_id    INTEGER NOT NULL REFERENCES restaurants(restaurant_id),
    driver_id        INTEGER NOT NULL REFERENCES drivers(driver_id),
    order_date       TEXT NOT NULL,
    order_status     TEXT NOT NULL,
    delivery_minutes INTEGER
);
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    item_name     TEXT NOT NULL,
    category      TEXT NOT NULL,
    quantity      INTEGER NOT NULL,
    unit_price    REAL NOT NULL
);
CREATE TABLE ratings (
    rating_id       INTEGER PRIMARY KEY,
    order_id        INTEGER NOT NULL REFERENCES orders(order_id),
    food_rating     INTEGER NOT NULL,
    delivery_rating INTEGER NOT NULL,
    created_at      TEXT NOT NULL
);
""")

# ---------- 2. Data acuan ----------
CITIES   = ["Jakarta", "Bandung", "Surabaya", "Medan", "Makassar"]
CHANNELS = ["Organic", "Paid Ads", "Referral", "Social Media"]
CUISINES = ["Indonesian", "Japanese", "Western", "Chinese", "Beverages", "Dessert"]
VEHICLES = ["Motorcycle", "Car", "Bicycle"]
FIRST = ["Budi","Sari","Andi","Dewi","Eko","Putri","Rian","Maya","Fajar","Lina","Toni","Wati","Hadi","Nia","Galih"]
LAST  = ["Santoso","Wijaya","Pratama","Lestari","Halim","Saputra","Anggraini","Nugroho","Permata","Kusuma"]
MENU = {
    "Indonesian": ["Nasi Goreng","Ayam Geprek","Sate Ayam","Gado-Gado","Soto Ayam"],
    "Japanese":   ["Ramen","Sushi Roll","Chicken Katsu","Udon","Gyoza"],
    "Western":    ["Cheeseburger","Pizza","Spaghetti","Fish & Chips","Caesar Salad"],
    "Chinese":    ["Fried Rice","Dim Sum","Kung Pao Chicken","Wonton Soup","Spring Roll"],
    "Beverages":  ["Iced Coffee","Milk Tea","Lemon Tea","Smoothie","Espresso"],
    "Dessert":    ["Cheesecake","Brownie","Ice Cream","Donut","Pudding"],
}

def rand_name():
    return f"{random.choice(FIRST)} {random.choice(LAST)}"

def rand_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# ---------- 3. customers ----------
customers = []
for cid in range(1, 201):
    signup = rand_date(date(2024,1,1), date(2024,12,31))
    customers.append((cid, rand_name(), random.choice(CITIES), signup.isoformat(), random.choice(CHANNELS)))
cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers)

# ---------- 4. restaurants ----------
restaurants = []
for rid in range(1, 41):
    restaurants.append((rid, f"Resto {rid:02d}", random.choice(CITIES),
                        random.choice(CUISINES), round(random.uniform(0.10, 0.25), 2)))
cur.executemany("INSERT INTO restaurants VALUES (?,?,?,?,?)", restaurants)

# ---------- 5. drivers ----------
drivers = []
for did in range(1, 31):
    join = rand_date(date(2024,1,1), date(2024,6,30))
    drivers.append((did, rand_name(), random.choice(VEHICLES), random.choice(CITIES), join.isoformat()))
cur.executemany("INSERT INTO drivers VALUES (?,?,?,?,?)", drivers)

# ---------- 6. orders + order_items + ratings ----------
orders, items, ratings = [], [], []
oid, iid, rid_counter = 1000, 1, 1
STATUS = ["Completed"]*88 + ["Cancelled"]*8 + ["Refunded"]*4  # ~88% sukses

for _ in range(3000):
    oid += 1
    cust = random.choice(customers)
    signup = date.fromisoformat(cust[3])
    start = max(signup, date(2025,1,1))  # order terjadi di 2025, setelah daftar
    odate = rand_date(start, date(2025,12,31))
    resto = random.choice(restaurants)
    driver = random.choice(drivers)
    status = random.choice(STATUS)
    delivery = random.randint(15, 75) if status == "Completed" else None
    orders.append((oid, cust[0], resto[0], driver[0], odate.isoformat(), status, delivery))

    # 1-4 item per order, menu mengikuti cuisine restoran
    for _ in range(random.randint(1, 4)):
        item = random.choice(MENU[resto[3]])
        items.append((iid, oid, item, resto[3], random.randint(1, 3), round(random.uniform(3, 20), 2)))
        iid += 1

    # rating hanya untuk order Completed, ~70%
    if status == "Completed" and random.random() < 0.7:
        ratings.append((rid_counter, oid, random.randint(3, 5), random.randint(2, 5), odate.isoformat()))
        rid_counter += 1

cur.executemany("INSERT INTO orders      VALUES (?,?,?,?,?,?,?)", orders)
cur.executemany("INSERT INTO order_items VALUES (?,?,?,?,?,?)", items)
cur.executemany("INSERT INTO ratings     VALUES (?,?,?,?,?)", ratings)

conn.commit()
print(f"Selesai! {len(orders)} orders, {len(items)} items, {len(ratings)} ratings.")
conn.close()