import pytest
from app.models import Client,Product,Cart,Order

@pytest.fixture
def test_order():
    product = Product(name="product1",price=15000)
    client = Client(name="client1")

    cart = Cart(client_id=client.id,products=[product.to_json()])
    order = Order(client_id=cart.client_id,total_price=cart.total(),products=cart.products)
    assert order.total_price < 30000

@pytest.fixture
def test_order_fail():
    product = Product(name="product1",price=30000)
    client = Client(name="client1")

    cart = Cart(client_id=client.id,products=[product.to_json()])
    order = Order(client_id=cart.client_id,total_price=cart.total(),products=cart.products)
    assert order.total_price >= 30000

