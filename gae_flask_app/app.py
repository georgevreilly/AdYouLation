from flask import Flask
 
def create_app(config):    
    app = Flask(__name__)
    app.config.from_object(config)
 
    # Later register blueprints here.
    # ...
    from gae_flask_app.hello_gae import hello_gae
    app.register_blueprint(hello_gae, url_prefix="/")
    return app
