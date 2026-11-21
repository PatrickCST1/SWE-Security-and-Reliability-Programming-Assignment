"""Business logic. Several design and correctness issues are intentional."""
from models import CartLine

PERCENT_CODES = {'WELCOME10': 0.10, 'STUDENT20': 0.20}
FIXED_CODES = {'SAVE15': 15.0}
VALID_CODES = PERCENT_CODES.keys() | FIXED_CODES.keys() | {'FREESHIP'}

class ShoppingCart:
    def __init__(self, user_id, repository):
        self.user_id = user_id
        self.repository = repository
        self.lines = []
        self.discount_code = None
        # self.discounted_total = None

    def add_item(self, sku, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            return False
        product = self.repository.get_product(sku)
        if not product:
            return False
        existing = next((x for x in self.lines if x.sku == sku), None)
        already = existing.quantity if existing else 0
        if product.stock < already + quantity:
            return False
        existing = next((x for x in self.lines if x.sku == sku), None)
        if existing:
            existing.quantity += quantity
        else:
            self.lines.append(CartLine(sku, product.name, product.price, quantity))
        return True

    def remove_item(self, sku, quantity=None):
        if quantity is not None and (not isinstance(quantity, int) or quantity <= 0):
            return False
        line = next((x for x in self.lines if x.sku == sku), None)
        if line is None:
            return False
        if quantity is None or quantity >= line.quantity:
            self.lines.remove(line)
        else:
            line.quantity -= quantity
        return True

    def subtotal(self):
        return sum(line.unit_price * line.quantity for line in self.lines)

    def total(self):
        # if self.discounted_total is not None:
        #     return self.discounted_total
        # return self.subtotal()
        amount = self.subtotal()
        if self.discount_code in PERCENT_CODES:
            amount *= 1 - PERCENT_CODES[self.discount_code]
        elif self.discount_code in FIXED_CODES:
            amount -= FIXED_CODES[self.discount_code]
        return round(max(amount, 0.0), 2)
            

    def apply_discount(self, code):
        # amount = self.total()
        # if code == 'WELCOME10':
        #     amount *= 0.9
        # elif code == 'STUDENT20':
        #     amount *= 0.8
        # elif code == 'SAVE15':
        #     amount -= 15
        # elif code == 'FREESHIP':
        #     print('Shipping is free')
        # else:
        #     print('Invalid coupon')
        #     return False
        # self.discount_code = code
        # self.discounted_total = amount
        # return True
        if code not in VALID_CODES:
            return False
        self.discount_code = code
        return True

    def load(self):
        for sku, quantity in self.repository.get_saved_cart(self.user_id):
            self.add_item(sku, quantity)

    def save(self):
        self.repository.save_cart(self.user_id, self.lines)
