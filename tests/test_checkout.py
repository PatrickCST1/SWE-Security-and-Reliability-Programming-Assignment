from checkout import CheckoutService
from payments import FakePaymentGateway


class FailingGateway:
    def charge(self, amount, payment_token):
        raise ConnectionError("gateway down")


def test_checkout_does_not_log_payment_token(repo, cart, capsys):
    cart.add_item("USB-01", 1)
    CheckoutService(repo, FakePaymentGateway()).checkout(cart, "tok_SECRET123", "r1")
    assert "tok_SECRET123" not in capsys.readouterr().out


def test_declined_payment_does_not_reduce_stock(repo, cart):
    cart.add_item("LAP-01", 2)
    gw = FakePaymentGateway(should_approve=False)
    result = CheckoutService(repo, gw).checkout(cart, "tok_test", "r1")
    assert result.status == "declined"
    assert repo.get_product("LAP-01").stock == 5


def test_payment_error_does_not_reduce_stock(repo, cart):
    cart.add_item("LAP-01", 2)
    result = CheckoutService(repo, FailingGateway()).checkout(cart, "tok_test", "r1")
    assert result.status == "payment_error"
    assert repo.get_product("LAP-01").stock == 5


def test_successful_payment_reduces_stock(repo, cart):
    cart.add_item("LAP-01", 2)
    result = CheckoutService(repo, FakePaymentGateway()).checkout(cart, "tok_test", "r1")
    assert result.status == "paid"
    assert repo.get_product("LAP-01").stock == 3