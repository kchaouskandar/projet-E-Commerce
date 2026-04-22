from collections import Counter
from app.models import Purchase, Product


def get_popular_products(limit=10):
    """Return products ranked by popularity_score descending."""
    return (
        Product.query
        .order_by(Product.popularity_score.desc())
        .limit(limit)
        .all()
    )


def get_purchase_frequency(user_id):
    """
    Return a dict of {product_name: count} showing how many times
    the user has purchased each product, sorted by frequency descending.
    """
    purchases = Purchase.query.filter_by(user_id=user_id).all()
    freq = Counter(p.product_name for p in purchases)
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))


def get_category_breakdown(user_id):
    """
    Return a list of dicts with category analytics for the given user:
    [{"category": str, "count": int, "total_spent": float}, ...]
    sorted by total_spent descending.
    """
    purchases = Purchase.query.filter_by(user_id=user_id).all()

    breakdown = {}
    for p in purchases:
        if p.category not in breakdown:
            breakdown[p.category] = {"count": 0, "total_spent": 0.0}
        breakdown[p.category]["count"] += 1
        breakdown[p.category]["total_spent"] += p.price

    result = [
        {"category": cat, **data}
        for cat, data in breakdown.items()
    ]
    return sorted(result, key=lambda x: x["total_spent"], reverse=True)


def get_total_spent(user_id):
    """Return cumulative spending for a user."""
    purchases = Purchase.query.filter_by(user_id=user_id).all()
    return round(sum(p.price for p in purchases), 2)


def get_most_bought_categories(user_id, top_n=3):
    """Return the top N category names the user buys most."""
    breakdown = get_category_breakdown(user_id)
    return [item["category"] for item in breakdown[:top_n]]
