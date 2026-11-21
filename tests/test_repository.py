from models import CartLine


# Bug 1: Ensures SQL injection cannot happen in get_product()
def test_get_product_rejects_sql_injection(repo):
    assert repo.get_product("' OR '1'='1") is None

# Bug 1: Ensures SQL injection cannot happen in get_saved_cart()
def test_get_saved_cart_rejects_sql_injection(repo):
    repo.save_cart("bob", [CartLine("LAP-01", "Laptop", 999.99, 1)])
    assert repo.get_saved_cart("x' OR '1'='1") == []
    
# Bug 2: Ensures listing orders only shows the user's orders
def test_list_orders_only_returns_own_orders(repo):
    repo.save_order("alice", 10.0, "paid", "r1")
    repo.save_order("bob", 20.0, "paid", "r2")
    rows = repo.list_orders("alice")
    assert [row[1] for row in rows] == ["alice"]