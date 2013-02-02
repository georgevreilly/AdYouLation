from __future__ import absolute_import

from flask import Flask
from gae_flask_app.videos import load_video_json
import logging
 
def create_app(config):    
    app = Flask(__name__)
    app.config.from_object(config)

    json_filename = app.config['VIDEO_JSON']
    app.videos = load_video_json(json_filename)
    logging.info("Loaded video data from '%s'", json_filename)
 
    # Register blueprints here.
    from gae_flask_app.hello_gae import hello_gae
    app.register_blueprint(hello_gae, url_prefix="/")

    from gae_flask_app.AdYouLation import AdYouLation
    app.register_blueprint(AdYouLation)

    return app
