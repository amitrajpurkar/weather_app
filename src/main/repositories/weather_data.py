import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web server compatibility
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional

# Internal helper to locate the CSV relative to this file
def _get_csv_path() -> Path:
    # This file is at: src/main/repositories/weather_data.py
    # CSV is at:       src/main/resources/WeatherData.csv
    return Path(__file__).resolve().parents[1] / "resources" / "WeatherData.csv"


def _load_weather_df() -> pd.DataFrame:
    """
    Load the weather data CSV into a pandas DataFrame.

    Returns:
        pd.DataFrame: The loaded weather data.
    """
    csv_path = _get_csv_path()
    if not csv_path.exists():
        raise FileNotFoundError(f"Weather data CSV not found at: {csv_path}")
    df = pd.read_csv(csv_path)
    return df


def summarize_weather_data() -> pd.DataFrame:
    """
    Public API: Return a tabular matrix summary of the weather data.

    Currently implemented as the numeric correlation matrix (Pearson) across
    all numeric columns in the dataset.

    Returns:
        pd.DataFrame: A correlation matrix DataFrame (rows/cols = numeric features).
    """
    df = _load_weather_df()
    numeric_df = df.select_dtypes(include=["number"]).copy()
    if numeric_df.empty:
        raise ValueError("No numeric columns found to compute a matrix summary.")
    corr = numeric_df.corr(numeric_only=True)
    return corr


def plot_summary_heatmap(corr_df: Optional[pd.DataFrame] = None,
                         *,
                         save_path: Optional[Path] = None,
                         show: bool = False) -> Path:
    """
    Public API: Plot a heatmap visualization for the matrix summary.

    Args:
        corr_df: Optional precomputed correlation matrix. If not provided, this
                 function will compute it via `summarize_weather_data()`.
        save_path: Optional path to save the chart image (e.g., Path("corr.png")).
        show: If True, display the plot window (useful for local debugging).

    Returns:
        Path: The path where the heatmap was saved (or None if only showing).
    """
    if corr_df is None:
        corr_df = summarize_weather_data()

    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_df, annot=True, cmap="coolwarm", fmt=".2f", square=True,
                cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title("Weather Data Correlation Matrix", fontsize=14, fontweight='bold')
    plt.tight_layout()

    # Save the figure if path is provided
    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    # Show if requested (mainly for debugging)
    if show:
        plt.show()
    
    # Always close the figure to free memory
    plt.close(fig)

    return save_path


def plot_monthly_weather_trends(year: int = 2012,
                                *,
                                save_path: Optional[Path] = None,
                                show: bool = False) -> Path:
    """
    Public API: Plot month-over-month average weather conditions for a given year.
    
    Creates a multi-panel visualization showing monthly trends for:
    - Temperature (Temp_C)
    - Humidity (Rel Hum_%)
    - Wind Speed (Wind Speed_km/h)
    - Pressure (Press_kPa)
    
    Args:
        year: The year to analyze (default: 2012).
        save_path: Optional path to save the chart image.
        show: If True, display the plot window (useful for local debugging).
    
    Returns:
        Path: The path where the chart was saved.
    """
    df = _load_weather_df()
    
    # Parse the Date/Time column
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%m/%d/%Y %H:%M')
    
    # Filter for the specified year
    df_year = df[df['Date/Time'].dt.year == year].copy()
    
    if df_year.empty:
        raise ValueError(f"No data found for year {year}")
    
    # Extract month
    df_year['Month'] = df_year['Date/Time'].dt.month
    
    # Calculate monthly averages for key metrics
    monthly_avg = df_year.groupby('Month').agg({
        'Temp_C': 'mean',
        'Rel Hum_%': 'mean',
        'Wind Speed_km/h': 'mean',
        'Press_kPa': 'mean',
        'Visibility_km': 'mean',
        'Dew Point Temp_C': 'mean'
    }).reset_index()
    
    # Create month names for better readability
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_avg['Month_Name'] = monthly_avg['Month'].apply(lambda x: month_names[x-1])
    
    # Create a 2x3 subplot layout
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle(f'Monthly Average Weather Conditions - {year}', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Plot 1: Temperature
    axes[0, 0].plot(monthly_avg['Month'], monthly_avg['Temp_C'], 
                    marker='o', linewidth=2, markersize=8, color='#e74c3c')
    axes[0, 0].set_title('Average Temperature', fontweight='bold')
    axes[0, 0].set_xlabel('Month')
    axes[0, 0].set_ylabel('Temperature (°C)')
    axes[0, 0].set_xticks(monthly_avg['Month'])
    axes[0, 0].set_xticklabels(monthly_avg['Month_Name'], rotation=45)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].fill_between(monthly_avg['Month'], monthly_avg['Temp_C'], 
                            alpha=0.3, color='#e74c3c')
    
    # Plot 2: Humidity
    axes[0, 1].plot(monthly_avg['Month'], monthly_avg['Rel Hum_%'], 
                    marker='s', linewidth=2, markersize=8, color='#3498db')
    axes[0, 1].set_title('Average Relative Humidity', fontweight='bold')
    axes[0, 1].set_xlabel('Month')
    axes[0, 1].set_ylabel('Humidity (%)')
    axes[0, 1].set_xticks(monthly_avg['Month'])
    axes[0, 1].set_xticklabels(monthly_avg['Month_Name'], rotation=45)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].fill_between(monthly_avg['Month'], monthly_avg['Rel Hum_%'], 
                            alpha=0.3, color='#3498db')
    
    # Plot 3: Wind Speed
    axes[0, 2].plot(monthly_avg['Month'], monthly_avg['Wind Speed_km/h'], 
                    marker='^', linewidth=2, markersize=8, color='#2ecc71')
    axes[0, 2].set_title('Average Wind Speed', fontweight='bold')
    axes[0, 2].set_xlabel('Month')
    axes[0, 2].set_ylabel('Wind Speed (km/h)')
    axes[0, 2].set_xticks(monthly_avg['Month'])
    axes[0, 2].set_xticklabels(monthly_avg['Month_Name'], rotation=45)
    axes[0, 2].grid(True, alpha=0.3)
    axes[0, 2].fill_between(monthly_avg['Month'], monthly_avg['Wind Speed_km/h'], 
                            alpha=0.3, color='#2ecc71')
    
    # Plot 4: Pressure
    axes[1, 0].plot(monthly_avg['Month'], monthly_avg['Press_kPa'], 
                    marker='D', linewidth=2, markersize=8, color='#9b59b6')
    axes[1, 0].set_title('Average Pressure', fontweight='bold')
    axes[1, 0].set_xlabel('Month')
    axes[1, 0].set_ylabel('Pressure (kPa)')
    axes[1, 0].set_xticks(monthly_avg['Month'])
    axes[1, 0].set_xticklabels(monthly_avg['Month_Name'], rotation=45)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].fill_between(monthly_avg['Month'], monthly_avg['Press_kPa'], 
                            alpha=0.3, color='#9b59b6')
    
    # Plot 5: Visibility
    axes[1, 1].plot(monthly_avg['Month'], monthly_avg['Visibility_km'], 
                    marker='p', linewidth=2, markersize=8, color='#f39c12')
    axes[1, 1].set_title('Average Visibility', fontweight='bold')
    axes[1, 1].set_xlabel('Month')
    axes[1, 1].set_ylabel('Visibility (km)')
    axes[1, 1].set_xticks(monthly_avg['Month'])
    axes[1, 1].set_xticklabels(monthly_avg['Month_Name'], rotation=45)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].fill_between(monthly_avg['Month'], monthly_avg['Visibility_km'], 
                            alpha=0.3, color='#f39c12')
    
    # Plot 6: Dew Point Temperature
    axes[1, 2].plot(monthly_avg['Month'], monthly_avg['Dew Point Temp_C'], 
                    marker='*', linewidth=2, markersize=10, color='#1abc9c')
    axes[1, 2].set_title('Average Dew Point Temperature', fontweight='bold')
    axes[1, 2].set_xlabel('Month')
    axes[1, 2].set_ylabel('Dew Point (°C)')
    axes[1, 2].set_xticks(monthly_avg['Month'])
    axes[1, 2].set_xticklabels(monthly_avg['Month_Name'], rotation=45)
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].fill_between(monthly_avg['Month'], monthly_avg['Dew Point Temp_C'], 
                            alpha=0.3, color='#1abc9c')
    
    plt.tight_layout()
    
    # Save the figure if path is provided
    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    # Show if requested (mainly for debugging)
    if show:
        plt.show()
    
    # Always close the figure to free memory
    plt.close(fig)
    
    return save_path
