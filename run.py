"""
run.py — Application entry point + demo data seeder.

Run with:
    python run.py
"""

from datetime import datetime, timedelta, timezone
from app import create_app, db
from app.models import User, Purchase, Product

app = create_app()


def seed_database():
    """Populate the database with demo users, products, and purchases."""

    # ── Products catalog ─────────────────────────────────────────────────────
    products = [
        Product(name="Sony WH-1000XM5 Headphones",  category="Electronics",  price=349.99, popularity_score=95, description="Industry-leading noise cancelling headphones"),
        Product(name="MacBook Air M2",               category="Electronics",  price=1199.0, popularity_score=92, description="Apple's thinnest, lightest laptop"),
        Product(name="iPhone 15 Pro",                category="Electronics",  price=999.0,  popularity_score=90, description="Pro camera system, titanium design"),
        Product(name="Nike Air Max 270",             category="Fashion",      price=149.99, popularity_score=88, description="Iconic Air Max cushioning"),
        Product(name="Python Crash Course",          category="Books",        price=35.0,   popularity_score=85, description="Best-selling Python programming book"),
        Product(name="PlayStation 5",                category="Gaming",       price=499.99, popularity_score=97, description="Next-gen gaming console"),
        Product(name="Apple Watch Series 9",         category="Electronics",  price=399.0,  popularity_score=87, description="Advanced health monitoring smartwatch"),
        Product(name="Levi's 501 Original Jeans",   category="Fashion",      price=89.99,  popularity_score=82, description="Classic straight-leg jeans"),
        Product(name="Clean Code (R. Martin)",       category="Books",        price=42.0,   popularity_score=80, description="Timeless guide to writing readable code"),
        Product(name="Logitech MX Master 3S",        category="Electronics",  price=99.99,  popularity_score=86, description="Advanced wireless ergonomic mouse"),
        Product(name="Adidas Ultraboost 22",         category="Fashion",      price=179.99, popularity_score=83, description="Responsive running shoes"),
        Product(name="Nintendo Switch OLED",         category="Gaming",       price=349.99, popularity_score=91, description="Vibrant OLED screen, portable gaming"),
    ]

    for p in products:
        if not Product.query.filter_by(name=p.name).first():
            db.session.add(p)
    db.session.commit()

    # ── Demo users ────────────────────────────────────────────────────────────
    users_data = [
        {"name": "Iskandar Kchaou",      "email": "iskandar@demo.com",    "password": "password123"},
        {"name": "Yassmin Bahloul",       "email": "yassmine@demo.com",    "password": "password123"},
        {"name": "Abderrahmen Benayed",   "email": "abderrahmen@demo.com", "password": "password123"},
    ]
    users = []
    for ud in users_data:
        u = User.query.filter_by(email=ud["email"]).first()
        if not u:
            u = User(name=ud["name"], email=ud["email"])
            u.set_password(ud["password"])
            db.session.add(u)
            db.session.commit()
        users.append(u)

    iskandar, yassmine, abderrahmen = users[0], users[1], users[2]

    # ── Iskandar — Gaming + Books ──────────────────────────────────────────────
    iskandar_purchases = [
        Purchase(user_id=iskandar.id, product_name="PlayStation 5",         category="Gaming",  price=499.99, date=datetime.now(timezone.utc) - timedelta(days=80)),
        Purchase(user_id=iskandar.id, product_name="Python Crash Course",   category="Books",   price=35.0,   date=datetime.now(timezone.utc) - timedelta(days=70)),
        Purchase(user_id=iskandar.id, product_name="Nintendo Switch OLED",  category="Gaming",  price=349.99, date=datetime.now(timezone.utc) - timedelta(days=55)),
        Purchase(user_id=iskandar.id, product_name="Clean Code (R. Martin)",category="Books",   price=42.0,   date=datetime.now(timezone.utc) - timedelta(days=40)),
        Purchase(user_id=iskandar.id, product_name="PlayStation 5",         category="Gaming",  price=499.99, date=datetime.now(timezone.utc) - timedelta(days=20)),
        Purchase(user_id=iskandar.id, product_name="Python Crash Course",   category="Books",   price=35.0,   date=datetime.now(timezone.utc) - timedelta(days=8)),
    ]

    # ── Yassmine — Fashion ────────────────────────────────────────────────────
    yassmine_purchases = [
        Purchase(user_id=yassmine.id, product_name="Nike Air Max 270",          category="Fashion", price=149.99, date=datetime.now(timezone.utc) - timedelta(days=90)),
        Purchase(user_id=yassmine.id, product_name="Levi's 501 Original Jeans", category="Fashion", price=89.99,  date=datetime.now(timezone.utc) - timedelta(days=65)),
        Purchase(user_id=yassmine.id, product_name="Adidas Ultraboost 22",      category="Fashion", price=179.99, date=datetime.now(timezone.utc) - timedelta(days=45)),
        Purchase(user_id=yassmine.id, product_name="Nike Air Max 270",          category="Fashion", price=149.99, date=datetime.now(timezone.utc) - timedelta(days=28)),
        Purchase(user_id=yassmine.id, product_name="Levi's 501 Original Jeans", category="Fashion", price=89.99,  date=datetime.now(timezone.utc) - timedelta(days=14)),
        Purchase(user_id=yassmine.id, product_name="Adidas Ultraboost 22",      category="Fashion", price=179.99, date=datetime.now(timezone.utc) - timedelta(days=3)),
    ]

    # ── Abderrahmen — Electronics + Gaming ───────────────────────────────────
    abderrahmen_purchases = [
        Purchase(user_id=abderrahmen.id, product_name="MacBook Air M2",               category="Electronics", price=1199.0, date=datetime.now(timezone.utc) - timedelta(days=85)),
        Purchase(user_id=abderrahmen.id, product_name="PlayStation 5",                category="Gaming",      price=499.99, date=datetime.now(timezone.utc) - timedelta(days=72)),
        Purchase(user_id=abderrahmen.id, product_name="Sony WH-1000XM5 Headphones",  category="Electronics", price=349.99, date=datetime.now(timezone.utc) - timedelta(days=50)),
        Purchase(user_id=abderrahmen.id, product_name="Nintendo Switch OLED",         category="Gaming",      price=349.99, date=datetime.now(timezone.utc) - timedelta(days=35)),
        Purchase(user_id=abderrahmen.id, product_name="Logitech MX Master 3S",        category="Electronics", price=99.99,  date=datetime.now(timezone.utc) - timedelta(days=18)),
        Purchase(user_id=abderrahmen.id, product_name="MacBook Air M2",               category="Electronics", price=1199.0, date=datetime.now(timezone.utc) - timedelta(days=6)),
    ]

    all_purchases = iskandar_purchases + yassmine_purchases + abderrahmen_purchases
    for purchase in all_purchases:
        existing = Purchase.query.filter_by(
            user_id=purchase.user_id,
            product_name=purchase.product_name,
            date=purchase.date
        ).first()
        if not existing:
            db.session.add(purchase)

    db.session.commit()
    print("✅ Demo database seeded successfully.")
    print("   👤 iskandar@demo.com    /  password123  (Gaming + Books)")
    print("   👤 yassmine@demo.com    /  password123  (Fashion)")
    print("   👤 abderrahmen@demo.com /  password123  (Electronics + Gaming)")



# ── Initialisation de la base de données (locale + production) ───────────────
# Appelé par `python run.py` ET par gunicorn (`gunicorn run:app`)
with app.app_context():
    db.create_all()
    seed_database()


if __name__ == "__main__":
    print("\n🚀 ShopSense is running at http://127.0.0.1:5000\n")
    app.run(debug=True)
