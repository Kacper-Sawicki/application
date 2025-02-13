from app import db
from app.models import Client

class ClientRepository:
    @staticmethod
    def add_client(name):
        client = Client(name=name)
        db.session.add(client)
        db.session.commit()
        return client.to_json()

    @staticmethod
    def get_client_by_id(client_id):
        client_db = Client.query.get(client_id)
        if client_db is None:
            return None
        return client_db.to_json()

    @staticmethod
    def get_all_clients():
        clients_db = Client.query.all()
        return [client.to_json() for client in clients_db]

    @staticmethod
    def update_client(client_id, new_name):
        client_db = Client.query.get(client_id)
        if client_db:
            client_db.name = new_name
            db.session.commit()
            return client_db.to_json()
        return None

    @staticmethod
    def delete_client(client_id):
        client_db = Client.query.get(client_id)
        if client_db:
            db.session.delete(client_db)
            db.session.commit()
            return True
        return False
