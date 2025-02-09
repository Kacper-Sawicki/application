from app import db
from app.models import Cart

class CartRepository:
    @staticmethod
    def create_cart(client_id):
        existing_cart = Cart.query.filter_by(client_id=client_id).first()
        if existing_cart:
            return None
        cart = Cart(client_id=client_id, products=[])
        db.session.add(cart)
        db.session.commit()
        return cart

    @staticmethod
    def get_cart_by_client_id(client_id):
        cart_db = Cart.query.filter_by(client_id=client_id).first()
        if not cart_db:
            return None
        cart = Cart.from_snapshot(cart_db.snapshot())
        return cart

    @staticmethod
    def add_product_to_cart(client_id, product):
        cart_db = Cart.query.filter_by(client_id=client_id).first()
        if not cart_db:
            return None, "no cart"
        cart = Cart.from_snapshot(cart_db.snapshot())

        cart.products = cart.products + [product.to_json()]

        cart_db.products = cart.products
        db.session.commit()
        return cart, None

    @staticmethod
    def delete_cart(cart_id):
        cart = Cart.query.get(cart_id)
        if cart:
            db.session.delete(cart)
            db.session.commit()
            return True
        return False
