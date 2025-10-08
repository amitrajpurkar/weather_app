# Running the Weather Data Analysis Application

## Quick Start

1. **Ensure dependencies are installed:**
   ```bash
   uv sync
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Open your browser:**
   Navigate to: http://127.0.0.1:5000

## Available Routes

- **`/`** - Home page with navigation cards
- **`/summary`** - View correlation matrix as an HTML table
- **`/heatmap`** - View correlation heatmap visualization

## Project Structure

```
weather_app/
├── main.py                          # Application entry point
├── src/
│   └── main/
│       ├── app.py                   # Flask app factory
│       ├── routes/
│       │   └── weather_routes.py    # Route handlers
│       ├── services/
│       │   └── weather_service.py   # Business logic layer
│       ├── repositories/
│       │   └── weather_data.py      # Data access layer
│       ├── templates/               # HTML templates
│       │   ├── base.html
│       │   ├── index.html
│       │   ├── summary.html
│       │   ├── heatmap.html
│       │   └── error.html
│       ├── static/                  # Static files (generated charts)
│       └── resources/
│           └── WeatherData.csv      # Weather dataset
```

## Technologies Used

- **Flask** - Web framework
- **Pandas** - Data manipulation and analysis
- **Seaborn** - Statistical data visualization
- **Matplotlib** - Plotting library
- **Bootstrap 5** - Frontend UI framework
