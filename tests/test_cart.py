import pytest

# Ensure adding items works after already applying a discount
def test_total_reflects_items_added_after_discount(cart):
    cart.add_item("MOU-01", 1)            # 29.95
    cart.apply_discount("WELCOME10")
    cart.add_item("USB-01", 1)            # +9.99
    assert cart.total() == pytest.approx(35.95, abs=0.01)   # 39.94 * 0.9
    
# Ensure discounts don't stack
def test_discount_cannot_be_applied_twice(cart):
    cart.add_item("LAP-01", 1)            # 999.99
    cart.apply_discount("WELCOME10")
    cart.apply_discount("WELCOME10")
    assert cart.total() == pytest.approx(899.99, abs=0.01)
    
# Ensure the discounted amount cannot be negative
def test_fixed_discount_never_makes_total_negative(cart):
    cart.add_item("USB-01", 1)
    cart.apply_discount("SAVE15")
    assert cart.total() >= 0
    
    
    
@pytest.mark.parametrize("qty", [0, -1, -5])
def test_add_item_rejects_non_positive_quantity(cart, qty):
    assert cart.add_item("MOU-01", qty) is False
    assert cart.lines == []

def test_add_item_counts_quantity_already_in_cart(cart):
    assert cart.add_item("LAP-01", 3)
    assert cart.add_item("LAP-01", 3) is False       # only 5 in stock
    assert cart.lines[0].quantity == 3

def test_remove_item_rejects_negative_quantity(cart):
    cart.add_item("MOU-01", 2)
    assert cart.remove_item("MOU-01", -3) is False
    assert cart.lines[0].quantity == 2