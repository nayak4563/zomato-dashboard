# Zomato Streamlit Analytics Dashboard

## 1. Install Python packages
```bash
pip install -r requirements.txt
```

## 2. Run the dashboard
Open a terminal in this folder and run:
```bash
streamlit run app.py
```

## 3. Load your data
When the dashboard opens in your browser, upload `zomato_dataset.csv` using the file uploader in the left sidebar.

## Dashboard features
- KPI cards for restaurants, cities, average dining rating, average delivery rating and average price
- Interactive filters for city, cuisine, restaurant and price range
- Restaurant rating and vote analysis
- Cuisine and city analysis
- Popular food items and average cuisine prices
- Cuisine-by-city heatmap
- Filtered data preview and CSV download

The dashboard uses the column names from the supplied `Zomato__Project.ipynb` notebook. It tolerates optional analysis columns being absent, but requires `Restaurant Name`, `City` and `Cuisine`.
