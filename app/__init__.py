from flask import Flask, request, session
from flask_babel import Babel

babel = Babel()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-change-this'
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ru']
    
    babel.init_app(app, locale_selector=get_locale)
    
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app

def get_locale():
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(['en', 'ru'])