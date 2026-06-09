# Data Dictionary

This document serves as the schema reference for variables in the project. Update this once datasets are selected and preliminary ingestion is completed.

## Raw Dataset Schema

| Column Name | Data Type (Raw) | Description | Example Value | Notes / Handling Strategy |
| :--- | :--- | :--- | :--- | :--- |
| `id` | Integer / String | Unique identifier of the crime incident | `1234567` | Keep as primary key (do not scale/encode) |
| `date_occurred` | Object / String | Date and time of incident occurrence | `2025-06-09 17:30:00` | Parse to `datetime64[ns]` in cleaning step |
| `category` | Categorical / Object | Broad classification of crime | `THEFT` | Map to standard categories / drop low frequency |
| `description` | Object / String | Detailed narrative / sub-category | `GRAND THEFT FROM MOTOR VEHICLE` | Text processing or categorical encoding |
| `location_lat` | Float | Latitude coordinate of occurrence | `41.8781` | Geospatial features; check for coordinate bounds |
| `location_lon` | Float | Longitude coordinate of occurrence | `-87.6298` | Geospatial features; check for coordinate bounds |
| `district` | Categorical / Int | District identifier or code | `1` or `Central` | Use for regional analysis |
| `arrested` | Boolean | Indicating whether an arrest was made | `True` | Target variable for predictive analysis |

---

## Processed Dataset Schema (Engineered Features)

These columns are generated during the processing / feature engineering phases in `notebooks/01_data_cleaning.ipynb` or `src/cleaning.py`.

| Column Name | Data Type | Source / Calculation | Description |
| :--- | :--- | :--- | :--- |
| `year` | Integer | Extracted from `date_occurred` | The year of the incident |
| `month` | Integer | Extracted from `date_occurred` | The month of the incident (1-12) |
| `hour` | Integer | Extracted from `date_occurred` | Hour of the incident (0-23) |
| `day_of_week` | Categorical | Extracted from `date_occurred` | Day of the week (Monday-Sunday) |
| `is_night` | Boolean | `hour >= 20` or `hour < 6` | Flag for night-time incident |
| `spatial_cluster`| Integer | K-Means clustering on Lat/Lon | Identified high-density crime hot spot zone |
