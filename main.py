"""
Entry point for the Weather Data Analysis Flask application.
"""
from src.main.app import create_app


def main():
    """Run the Flask development server."""
    app = create_app()
    print("🌤️  Starting Weather Data Analysis Application...")
    print("📊 Navigate to: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)


if __name__ == "__main__":
    main()
