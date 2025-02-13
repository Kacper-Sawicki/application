from app import db
from app.models import Order,Cart

class OrderRepository:
    @staticmethod
    def create_order(client_id):
        cart_db = Cart.query.filter_by(client_id=client_id).first()
        if not cart_db:
            return None, "no cart"


        total_price = cart_db.total()

        if total_price >= 30000:
            return None, "too expensive"
        order = Order(client_id=client_id, products=cart_db.products, total_price=total_price)
        db.session.add(order)
        db.session.delete(cart_db)
        db.session.commit()
        return order.to_json(), None

    @staticmethod
    def get_order_by_id(order_id):
        order_db = Order.query.get(order_id)
        if not order_db:
            return None
        return order_db.to_json()
    @staticmethod
    def get_all_orders():
        return Order.query.all()
