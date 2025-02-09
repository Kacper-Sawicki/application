from app import db
from app.models import Order,Cart

class OrderRepository:
    @staticmethod
    def create_order(client_id):
        cart_db = Cart.query.filter_by(client_id=client_id).first()
        if not cart_db:
            return None, "no cart"

        cart = Cart.from_snapshot(cart_db.snapshot())
        total_price = cart.total()

        if total_price >= 30000:
            return None, "too expensive"
        order = Order(client_id=client_id, products=cart.products, total_price=total_price)
        db.session.add(order)
        db.session.delete(cart_db)
        db.session.commit()
        return order, None

    @staticmethod
    def get_order_by_id(order_id):
        order_db = Order.query.get(order_id)
        if not order_db:
            return None
        return Order.from_snapshot(order_db.snapshot())

    @staticmethod
    def get_all_orders():
        return Order.query.all()
