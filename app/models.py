from app import db
from sqlalchemy.orm import Mapped
from sqlalchemy import JSON

class Client(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Product(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    price: Mapped[int] = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }

class Cart(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    client_id: Mapped[int] = db.Column(db.Integer, nullable=False)
    products: Mapped[dict] = db.Column(JSON)


    def to_json(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "products": self.products,
            "total_price": self.total()
        }

    def total(self):
        total = 0
        for i in range(0,len(self.products)):
            total += self.products[i]["price"]
        return total

class Order(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    client_id: Mapped[int] = db.Column(db.Integer, nullable=False)
    products: Mapped[dict] = db.Column(JSON, nullable=False)
    total_price: Mapped[int] = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "total_price":self.total_price,
            "products": self.products
        }