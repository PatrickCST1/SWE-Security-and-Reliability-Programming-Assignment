import pytest
from setup_db import initialize
from repository import StoreRepository
from cart import ShoppingCart
from checkout import CheckoutService
from payments import FakePaymentGateway

@pytest.fixture
def repo(tmp_path):
    db = str(tmp_path / "test.db")
    initialize(db)
    return StoreRepository(db)

@pytest.fixture
def cart(repo):
    return ShoppingCart("alice", repo)