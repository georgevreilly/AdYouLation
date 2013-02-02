from gae_flask_app import settings
from gaesessions import SessionMiddleware

def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key=settings.COOKIE_KEY)
    return app
