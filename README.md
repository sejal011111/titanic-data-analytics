# Titanic Data Analytics Project

End-to-end analytics workflow: data cleaning, analysis, visualization,
Flask REST API, and Postman testing.

## Tech Stack
Python 3, Pandas, Seaborn, Matplotlib, Flask, Postman

## Setup
```bash
pip install -r requirements.txt
```

## How to Run (from the project root folder, in this order)
1. Clean data and save CSV: `python preprocessing.py`
2. Generate charts: `python visualization.py`
3. Start the API: `python app.py` (runs at http://127.0.0.1:5000)

Note: preprocessing downloads the dataset from the Seaborn GitHub repo,
so an internet connection is required.

## Project Structure
```
├── app.py               Flask API
├── preprocessing.py     Cleaning + validation
├── analysis.py          Grouped insights
├── visualization.py     Chart generation
├── requirements.txt
├── data/                cleaned_titanic.csv
├── outputs/             PNG charts
├── notebook/            titanic_analysis.ipynb
├── postman/             Postman collection (JSON)
└── screenshots/         Charts and API response screenshots
```

## API Endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/health | Check app and dataset status |
| GET | /api/summary | Rows, columns, missing values, survival rate |
| GET | /api/insights | Grouped analytical results |
| GET | /api/passengers | Filtered passenger records |

### Examples
- `GET /api/health` returns `{"status": "ok", "rows": <count>}`
- `GET /api/passengers?sex=female&pclass=1&survived=1&limit=10`
- `GET /api/passengers?pclass=9` returns 400 with an error message
- `GET /api/unknown` returns 404

## Cleaning Assumptions
- Exact duplicate rows removed (also re-checked after imputation)
- Missing age filled with median by passenger class and sex
- Missing embarked / embark_town filled with the mode
- Missing deck labelled "Unknown"
- Non-positive fares replaced with the class median
- `alive` and `class` dropped (leakage / redundant)
- Features added: family_size, is_alone, age_band, fare_band

## Limitations
- Dataset is historical and observational: results show association, not causation
- Age imputation introduces estimated values
- Deck is highly incomplete, so deck conclusions are exploratory
- The API is a learning implementation, not production-ready