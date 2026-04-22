from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user

from app import db, bcrypt
from app.models import User, Purchase, Product
from app.services.analytics import (
    get_purchase_frequency,
    get_category_breakdown,
    get_popular_products,
    get_total_spent,
)
from app.services.recommender import get_recommendations

main = Blueprint("main", __name__)


# ─── Accueil ──────────────────────────────────────────────────────────────────

@main.route("/")
def index():
    return render_template("index.html")


# ─── Authentification ─────────────────────────────────────────────────────────

@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.history"))

    if request.method == "POST":
        name     = request.form.get("name",             "").strip()
        email    = request.form.get("email",            "").strip().lower()
        password = request.form.get("password",         "")
        confirm  = request.form.get("confirm_password", "")

        if not name or not email or not password:
            flash("Tous les champs sont obligatoires.", "danger")
            return render_template("register.html")

        if password != confirm:
            flash("Les mots de passe ne correspondent pas.", "danger")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("Un compte avec cette adresse e-mail existe déjà.", "warning")
            return render_template("register.html")

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Compte créé avec succès ! Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.history"))

    if request.method == "POST":
        email    = request.form.get("email",    "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get("next")
            flash(f"Bienvenue, {user.name} !", "success")
            return redirect(next_page or url_for("main.history"))

        flash("Adresse e-mail ou mot de passe incorrect.", "danger")

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("main.login"))


# ─── Sprint 1 : Historique des achats ────────────────────────────────────────

@main.route("/history")
@login_required
def history():
    purchases = (
        Purchase.query
        .filter_by(user_id=current_user.id)
        .order_by(Purchase.date.desc())
        .all()
    )
    total_spent = get_total_spent(current_user.id)
    return render_template("history.html", purchases=purchases, total_spent=total_spent)


# ─── Sprint 2 : Tableau de bord analytique ───────────────────────────────────

@main.route("/dashboard")
@login_required
def dashboard():
    category_data = get_category_breakdown(current_user.id)
    freq_data     = get_purchase_frequency(current_user.id)
    popular       = get_popular_products(limit=6)
    total_spent   = get_total_spent(current_user.id)
    total_orders  = Purchase.query.filter_by(user_id=current_user.id).count()

    return render_template(
        "dashboard.html",
        category_data=category_data,
        freq_data=freq_data,
        popular=popular,
        total_spent=total_spent,
        total_orders=total_orders,
    )


# ─── Sprint 2 : Recommandations ──────────────────────────────────────────────

@main.route("/recommendations")
@login_required
def recommendations():
    recs = get_recommendations(current_user.id, top_n=5)
    return render_template("recommendations.html", recommendations=recs)


# ─── Boutique ─────────────────────────────────────────────────────────────────

@main.route("/shop")
@login_required
def shop():
    products   = Product.query.order_by(Product.popularity_score.desc()).all()
    cart       = session.get("cart", {})
    cart_count = sum(cart.values())
    return render_template("shop.html", products=products,
                           cart=cart, cart_count=cart_count)


@main.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def cart_add(product_id):
    product    = Product.query.get_or_404(product_id)
    cart       = session.get("cart", {})
    key        = str(product_id)
    cart[key]  = cart.get(key, 0) + 1
    session["cart"] = cart
    flash(f"« {product.name} » ajouté au panier.", "success")
    return redirect(request.referrer or url_for("main.shop"))


@main.route("/cart/remove/<int:product_id>", methods=["POST"])
@login_required
def cart_remove(product_id):
    cart = session.get("cart", {})
    key  = str(product_id)
    if key in cart:
        del cart[key]
        session["cart"] = cart
    flash("Article retiré du panier.", "info")
    return redirect(url_for("main.cart"))


@main.route("/cart")
@login_required
def cart():
    raw_cart = session.get("cart", {})
    items    = []
    total    = 0.0
    for pid, qty in raw_cart.items():
        p = Product.query.get(int(pid))
        if p:
            subtotal = p.price * qty
            total   += subtotal
            items.append({"product": p, "qty": qty, "subtotal": subtotal})
    return render_template("cart.html", items=items, total=total)


@main.route("/checkout", methods=["POST"])
@login_required
def checkout():
    raw_cart = session.get("cart", {})
    if not raw_cart:
        flash("Votre panier est vide.", "warning")
        return redirect(url_for("main.shop"))

    for pid, qty in raw_cart.items():
        p = Product.query.get(int(pid))
        if p:
            for _ in range(qty):
                purchase = Purchase(
                    user_id=current_user.id,
                    product_name=p.name,
                    category=p.category,
                    price=p.price,
                    date=datetime.now(timezone.utc),
                )
                db.session.add(purchase)

    db.session.commit()
    session.pop("cart", None)
    flash("🎉 Commande confirmée ! Vos achats ont été enregistrés dans votre historique.", "success")
    return redirect(url_for("main.history"))
