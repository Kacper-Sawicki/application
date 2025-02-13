from app.models import Client,Product,Cart,Order
from flask import request, make_response, jsonify
from app.repositories.client_repository import ClientRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository





def init_routes(app):

    # client

    @app.route("/clients/add", methods=["POST"])
    def clientadd():
        name = request.json.get('name')
        client = ClientRepository.add_client(name)
        return make_response(jsonify({
            "success": True,
            "client": client.to_json()
        }))

    @app.route("/clients", methods=["GET"])
    def clients():
        clients = ClientRepository.get_all_clients()
        return make_response(jsonify({
            "success": True,
            "data": [client.to_json() for client in clients]
        }))

    @app.route("/clients/change/<int:client_id>", methods=["PUT"])
    def clientchange(client_id):
        new_name = request.json.get('name')
        client = ClientRepository.update_client(client_id, new_name)
        if client:
            return make_response(jsonify({
                "success": True,
                "data": client.to_json()
            }))
        else:
            return make_response(jsonify({
                "success": False,
                "message": "Client not found"
            })), 404

    #product

    @app.route("/products/add", methods=["POST"])
    def productadd():
        name = request.json.get('name')
        price = request.json.get('price')
        product = ProductRepository.add_product(name, price)
        return make_response(jsonify({
            "success": True,
            "product": product.to_json()
        }))

    @app.route("/products", methods=["GET"])
    def products():
        products = ProductRepository.get_all_products()
        return make_response(jsonify({
            "success": True,
            "data": [product.to_json() for product in products]
        }))

    @app.route("/products/change/<int:product_id>", methods=["PUT"])
    def productchange(product_id):
        name = request.json.get('name')
        price = request.json.get('price')
        product = ProductRepository.update_product(product_id, new_name=name, new_price=price)
        if product:
            return make_response(jsonify({
                "success": True,
                "product": product.to_json()
            }))
        else:
            return make_response(jsonify({
                "success": False,
                "message": "Product not found"
            })), 404

    #cart

    @app.route("/cart/<int:client_id>",methods=["GET"])
    def cartproducts(client_id):
        cart = Cart.query.filter_by(client_id=client_id).first()
        if not cart:
            return make_response(jsonify({
                "success": False,
            }))
        return make_response(jsonify({
            "success": True,
            "data": cart.to_json()
        }))

    @app.route("/cart/<int:client_id>/create", methods=["POST"])
    def cartcreate(client_id):
        cart = CartRepository.create_cart(client_id)
        if cart is None:
            return make_response(jsonify({
                "success": False,
                "message": "Cart already exists"
            })), 400
        return make_response(jsonify({
            "success": True,
        }))

    @app.route("/cart/<int:client_id>/add/<int:product_id>", methods=["PUT", "POST"])
    def cartadd(client_id, product_id):
        product = Product.query.get(product_id)
        if not product:
            return make_response(jsonify({
                "success": False,
                "problem": "no product"
            })), 404

        cart, error = CartRepository.add_product_to_cart(client_id, product)
        if error:
            return make_response(jsonify({
                "success": False,
                "problem": error
            })), 400

        return make_response(jsonify({
            "success": True,
            "cart": cart.to_json()
        }))

    #order

    @app.route("/order/<int:client_id>", methods=["POST"])
    def order(client_id):
        order_obj, error = OrderRepository.create_order(client_id)
        if error:
            return make_response(jsonify({
                "success": False,
                "problem": error
            })), 400

        return make_response(jsonify({
            "success": True,
            "order": order_obj.to_json()
        }))

    @app.route("/order/<int:order_id>/get", methods=["GET"])
    def orderget(order_id):
        order_obj = OrderRepository.get_order_by_id(order_id)
        if not order_obj:
            return make_response(jsonify({
                "success": False,
                "message": "Order not found"
            })), 404

        return make_response(jsonify({
            "success": True,
            "order": order_obj.to_json()
        }))
        
