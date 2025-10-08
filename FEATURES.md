# Weather Data Analysis Application - Features

## Available Visualizations

### 1. Correlation Matrix (Summary Table)
- **Route:** `/summary`
- **Description:** Displays a tabular view of Pearson correlation coefficients between all numeric weather variables
- **Technology:** Pandas DataFrame rendered as HTML table with Bootstrap styling

### 2. Correlation Heatmap
- **Route:** `/heatmap`
- **Description:** Visual heatmap representation of the correlation matrix
- **Technology:** Seaborn heatmap with color-coded correlations (red = positive, blue = negative)

### 3. Monthly Weather Trends (NEW)
- **Route:** `/monthly-trends`
- **Description:** Multi-panel visualization showing month-over-month averages for 2012
- **Metrics Displayed:**
  - Average Temperature (°C)
  - Average Relative Humidity (%)
  - Average Wind Speed (km/h)
  - Average Atmospheric Pressure (kPa)
  - Average Visibility (km)
  - Average Dew Point Temperature (°C)
- **Technology:** Matplotlib subplots with 2x3 grid layout, filled line charts

## Public Functions in `weather_data.py`

### 1. `summarize_weather_data() -> pd.DataFrame`
Returns correlation matrix of numeric weather variables.

### 2. `plot_summary_heatmap(corr_df=None, *, save_path=None, show=False) -> Path`
Generates and saves a correlation heatmap visualization.

### 3. `plot_monthly_weather_trends(year=2012, *, save_path=None, show=False) -> Path` (NEW)
Generates a 6-panel chart showing monthly averages for key weather metrics.

## Application Architecture

```
User Request
    ↓
Routes (weather_routes.py)
    ↓
Services (weather_service.py)
    ↓
Repositories (weather_data.py)
    ↓
Data (WeatherData.csv)
```

## How to Access

1. Start the application: `python main.py`
2. Navigate to: http://127.0.0.1:5000
3. Click on any of the three tiles:
   - **Correlation Matrix** - View data relationships in table format
   - **Correlation Heatmap** - View data relationships as a heatmap
   - **Monthly Trends** - View seasonal patterns throughout 2012

## Navigation

The application includes a responsive navbar with links to:
- Home
- Summary Table
- Heatmap
- Monthly Trends (NEW)

All pages maintain consistent styling and navigation.
