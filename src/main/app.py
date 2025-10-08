"""
Flask application factory for the Weather Data Analysis application.
"""
from flask import Flask
from pathlib import Path


def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Configure the app
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['STATIC_FOLDER'] = Path(__file__).parent / 'static'
    
    # Register blueprints
    from src.main.routes.weather_routes import weather_bp
    app.register_blueprint(weather_bp)
    
    return app
