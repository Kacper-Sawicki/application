from app import db
from app.models import Product

class ProductRepository:
    @staticmethod
    def add_product(name, price):
        product = Product(name=name, price=price)
        db.session.add(product)
        db.session.commit()
        return Product.from_snapshot(product.snapshot())

    @staticmethod
    def get_product_by_id(product_id):
        product_db = Product.query.get(product_id)
        if not product_db:
            return None
        return Product.from_snapshot(product_db.snapshot())

    @staticmethod
    def get_all_products():
        products_db = Product.query.all()
        return [Product.from_snapshot(product.snapshot()) for product in products_db]

    @staticmethod
    def update_product(product_id, new_name=None, new_price=None):
        product_db = Product.query.get(product_id)
        if product_db:
            if new_name:
                product_db.name = new_name
            if new_price is not None:
                product_db.price = new_price
            db.session.commit()
            return Product.from_snapshot(product_db.snapshot())
        return None

    @staticmethod
    def delete_product(product_id):
        product_db = Product.query.get(product_id)
        if product_db:
            db.session.delete(product_db)
            db.session.commit()
            return True
        return False
