from collections import Counter
from app.models import Purchase, Product
from app.services.analytics import get_popular_products


def get_recommendations(user_id, top_n=5):
    """
    Frequency-based recommendation engine.

    Logic:
    1. Count how many times the user bought each product name.
    2. For each product name (most frequent first), find the matching
       Product row in the catalog.
    3. If the user has fewer than top_n distinct products, backfill
       with globally popular products not yet in the list.
    4. Return top_n results with a reason string showing purchase count.

    Can recommend items already bought — that is intentional, as high
    purchase frequency is the strongest signal of preference.
    """
    # ── Step 1: purchase frequency per product name ────────────────────────
    purchases = Purchase.query.filter_by(user_id=user_id).all()
    freq = Counter(p.product_name for p in purchases)

    result = []
    seen_ids = set()

    # ── Step 2: match product names to catalog rows, ordered by frequency ──
    for product_name, count in freq.most_common():
        product = Product.query.filter_by(name=product_name).first()
        if product and product.id not in seen_ids:
            seen_ids.add(product.id)
            if count == 1:
                reason = "You've purchased this before"
            else:
                reason = f"You've purchased this {count} times"
            result.append({
                "product": product,
                "reason": reason,
                "score": round(count * 10 + product.popularity_score * 0.1, 2),
            })
        if len(result) >= top_n:
            break

    # ── Step 3: backfill with global popularity if not enough results ───────
    if len(result) < top_n:
        for product in get_popular_products(limit=20):
            if product.id not in seen_ids:
                seen_ids.add(product.id)
                result.append({
                    "product": product,
                    "reason": "Trending — popular with other shoppers",
                    "score": round(product.popularity_score * 0.1, 2),
                })
            if len(result) >= top_n:
                break

    return result[:top_n]
