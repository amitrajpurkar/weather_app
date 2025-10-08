"""
Route handlers for weather data visualization endpoints.
"""
from flask import Blueprint, render_template, send_file
from pathlib import Path
from src.main.services.weather_service import WeatherService

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/')
def index():
    """
    Home page with navigation to different views.
    """
    return render_template('index.html')


@weather_bp.route('/summary')
def summary():
    """
    Display the weather data correlation matrix as an HTML table.
    """
    try:
        summary_html = WeatherService.get_summary_html()
        return render_template('summary.html', table_html=summary_html)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


@weather_bp.route('/heatmap')
def heatmap():
    """
    Display the correlation heatmap visualization.
    """
    try:
        # Generate heatmap and save to static folder
        static_dir = Path(__file__).resolve().parents[1] / 'static'
        static_dir.mkdir(exist_ok=True)
        heatmap_path = static_dir / 'correlation_heatmap.png'
        
        WeatherService.generate_heatmap(heatmap_path)
        
        return render_template('heatmap.html', image_url='/static/correlation_heatmap.png')
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


@weather_bp.route('/monthly-trends')
def monthly_trends():
    """
    Display the monthly weather trends visualization for 2012.
    """
    try:
        # Generate monthly trends chart and save to static folder
        static_dir = Path(__file__).resolve().parents[1] / 'static'
        static_dir.mkdir(exist_ok=True)
        trends_path = static_dir / 'monthly_trends_2012.png'
        
        WeatherService.generate_monthly_trends(trends_path, year=2012)
        
        return render_template('monthly_trends.html', 
                             image_url='/static/monthly_trends_2012.png',
                             year=2012)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


@weather_bp.route('/static/<path:filename>')
def serve_static(filename):
    """
    Serve static files (images, CSS, etc.).
    """
    static_dir = Path(__file__).resolve().parents[1] / 'static'
    return send_file(static_dir / filename)
