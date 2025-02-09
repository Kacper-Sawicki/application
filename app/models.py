from app import db
from sqlalchemy.orm import Mapped
from sqlalchemy import JSON

class Client(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)

    def snapshot(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    @staticmethod
    def from_snapshot(snapshot_data):
        client = Client(name=snapshot_data.get("name"))
        client.id = snapshot_data.get("id")
        return client

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Product(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    price: Mapped[int] = db.Column(db.Integer, nullable=False)

    def snapshot(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }
    
    @staticmethod
    def from_snapshot(snapshot_data):
        product = Product(
            name=snapshot_data.get("name"),
            price=snapshot_data.get("price")
        )
        product.id = snapshot_data.get("id")
        return product

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

    def snapshot(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "products": self.products
        }

    @staticmethod
    def from_snapshot(snapshot_data):
        return Cart(
            id=snapshot_data.get("id"),
            client_id=snapshot_data.get("client_id"),
            products=snapshot_data.get("products", [])
        )


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

    def snapshot(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "products": self.products,
            "total_price": self.total_price
        }

    @staticmethod
    def from_snapshot(snapshot_data):
        return Order(
            id=snapshot_data.get("id"),
            client_id=snapshot_data.get("client_id"),
            products=snapshot_data.get("products", []),
            total_price=snapshot_data.get("total_price", 0.0)
        )

    def to_json(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "total_price":self.total_price,
            "products": self.products
        }