from .api_customer import api_customer
from .api_product import api_product
from .api_order import api_order
from .endpoint import endpoint

def init_app(app):
    app.register_blueprint(api_customer)
    app.register_blueprint(api_product)
    app.register_blueprint(api_order)
    app.register_blueprint(endpoint)
