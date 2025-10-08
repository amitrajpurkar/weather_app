"""
Business logic layer for weather data operations.
"""
import pandas as pd
from pathlib import Path
from src.main.repositories.weather_data import (
    summarize_weather_data, 
    plot_summary_heatmap,
    plot_monthly_weather_trends
)


class WeatherService:
    """Service class to handle weather data operations."""
    
    @staticmethod
    def get_summary_table() -> pd.DataFrame:
        """
        Get the weather data correlation matrix summary.
        
        Returns:
            pd.DataFrame: Correlation matrix.
        """
        return summarize_weather_data()
    
    @staticmethod
    def get_summary_html() -> str:
        """
        Get the weather data summary as an HTML table.
        
        Returns:
            str: HTML representation of the correlation matrix.
        """
        corr_df = summarize_weather_data()
        # Convert to HTML with styling
        html = corr_df.to_html(
            classes='table table-striped table-bordered table-hover',
            float_format=lambda x: f'{x:.3f}',
            border=0
        )
        return html
    
    @staticmethod
    def generate_heatmap(output_path: Path) -> Path:
        """
        Generate and save the correlation heatmap.
        
        Args:
            output_path: Path where the heatmap image should be saved.
            
        Returns:
            Path: The path where the heatmap was saved.
        """
        corr_df = summarize_weather_data()
        plot_summary_heatmap(corr_df, save_path=output_path, show=False)
        return output_path
    
    @staticmethod
    def generate_monthly_trends(output_path: Path, year: int = 2012) -> Path:
        """
        Generate and save the monthly weather trends chart.
        
        Args:
            output_path: Path where the chart image should be saved.
            year: The year to analyze (default: 2012).
            
        Returns:
            Path: The path where the chart was saved.
        """
        plot_monthly_weather_trends(year=year, save_path=output_path, show=False)
        return output_path
