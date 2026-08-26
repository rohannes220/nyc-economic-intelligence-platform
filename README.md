# NYC Economic Intelligence Platform

An end-to-end data analytics platform for analyzing economic conditions across New York City's five boroughs.

The project integrates demographic, housing, employment, business, and development data from multiple public sources into a centralized analytics pipeline. Python is used for data acquisition and transformation, SQL for structured data storage and analysis, and Streamlit for interactive visualization.

The project explores:

> **How are economic conditions changing across New York City, and how do those conditions differ across the five boroughs?**

---

## Project Overview

Understanding economic conditions requires combining information from multiple sources rather than relying on a single indicator.

This project brings together public datasets covering income, housing, employment, business activity, and development and standardizes them into a common **borough-year dataset**.

The platform analyzes indicators including:

- Median household income
- Median gross rent
- Unemployment rates
- Licensed business activity
- Building permit activity
- Rent-to-income ratios
- Year-over-year economic changes

The resulting dataset supports comparisons between boroughs as well as analysis of how economic conditions change over time.

---

## Architecture

```text
Public Data Sources
        |
        v
Python Data Acquisition
        |
        v
Data Cleaning & Transformation
        |
        v
Borough-Year Dataset
        |
        v
SQL Database
        |
        v
Data Analysis
        |
        v
Streamlit Dashboard
```

The project separates data acquisition, transformation, storage, analysis, and visualization into distinct stages.

This structure allows source datasets to be refreshed without requiring the entire analytics application to be redesigned.

---

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas |
| Database | SQLite / SQL |
| Data Modeling | Dimensional Modeling |
| Data Analysis | SQL |
| Visualization | Streamlit |
| Data Sources | U.S. Census API, NYC Open Data |
| Data Formats | CSV, JSON, SQL |

---

## Public Data Sources

### U.S. Census Bureau — ACS 5-Year Estimates

The American Community Survey provides demographic and economic indicators used throughout the platform, including:

- Median household income
- Median gross rent
- Employment data
- Unemployment-related measures

These indicators provide a foundation for comparing economic conditions across New York City's boroughs.

### NYC Open Data — DCWP

NYC Department of Consumer and Worker Protection licensing data is incorporated as an indicator of business activity.

Business-license records provide an additional perspective on commercial activity across different parts of the city.

### NYC Open Data — Department of Buildings

Building permit data is incorporated as an indicator of construction and development activity.

Combining development data with demographic and economic indicators provides a broader view of changes occurring across the five boroughs.

---

## ETL Pipeline

The project implements a Python-based **Extract, Transform, Load (ETL)** workflow.

### 1. Extract

`src/fetch_live_data.py` retrieves data from external public sources.

The acquisition layer is separated from the analytical components so source data can be refreshed independently.

### 2. Transform

Raw data from different sources must be standardized before the datasets can be combined.

The transformation process includes:

- Standardizing borough names
- Converting fields to consistent data types
- Handling missing or invalid values
- Aligning datasets to a common borough-year level
- Creating derived analytical fields
- Validating records before loading

### 3. Load

Processed records are loaded into a structured SQL database.

The database provides a centralized analytical layer that can be queried independently from the original CSV and API responses.

---

## Data Model

The project organizes economic information using a simplified dimensional structure.

### `dim_borough`

Stores standardized information for NYC's five boroughs:

- Manhattan
- Brooklyn
- Queens
- Bronx
- Staten Island

### `dim_year`

Stores the time dimension used for historical analysis.

### `fact_economic_metrics`

Contains economic measurements associated with each borough and year.

Metrics include:

- Median household income
- Median gross rent
- Unemployment rate
- Licensed business count
- Building permit count
- Rent-to-income ratio
- Year-over-year economic indicators

The structure can be represented as:

```text
              dim_borough
                   |
                   v
          fact_economic_metrics
                   ^
                   |
               dim_year
```

This design separates descriptive dimensions from quantitative measurements and provides a consistent structure for analysis.

---

## Data Analysis

Once the datasets are standardized and loaded into SQL, the analytical layer compares economic indicators across boroughs and years.

The analysis focuses on questions such as:

1. How do income and housing costs differ across NYC boroughs?
2. Which boroughs experience the highest unemployment rates?
3. How have major economic indicators changed over time?
4. How does licensed business activity differ across the city?
5. Which boroughs show the greatest levels of construction and development activity?
6. How do economic conditions differ between boroughs within the same year?

The goal is to transform data from several independent public sources into a single dataset that can support broader economic analysis.

---

## Dashboard

The Streamlit dashboard provides an interactive interface for exploring the processed economic data.

Users can examine indicators across boroughs and years rather than working directly with raw source files or database tables.

The dashboard provides views covering areas such as:

- Household income
- Housing costs
- Employment conditions
- Business activity
- Development activity
- Historical trends
- Borough comparisons

The dashboard serves as the presentation layer for the underlying Python and SQL analytics pipeline.

---

## Data Quality

Because the project combines datasets from multiple sources, data validation is an important part of the pipeline.

The workflow checks areas such as:

- Borough naming consistency
- Year values
- Numeric data types
- Missing observations
- Invalid values
- Expected borough-year combinations
- Derived analytical fields

These checks help maintain consistency before information reaches the SQL database and dashboard.

---

## Repository Structure

```text
nyc-economic-intelligence-platform/
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── processed/
│
├── reports/
│
├── sql/
│   └── analytics.sql
│
├── src/
│   └── fetch_live_data.py
│
├── build_project.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Key Files

**`src/fetch_live_data.py`**

Retrieves data from public APIs and NYC Open Data sources.

**`build_project.py`**

Processes and prepares the project data and creates the analytical database.

**`sql/analytics.sql`**

Contains the SQL used to analyze economic indicators across boroughs and years.

**`dashboard/app.py`**

Provides the Streamlit interface for interactive data exploration.

---

## Running the Project

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Build the Project

```bash
python build_project.py
```

### Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Fetching Live Public Data

Live public data can be retrieved using:

```bash
python src/fetch_live_data.py
```

The acquisition layer downloads the source datasets separately from the rest of the analytics workflow.

The data can then be standardized to the same borough-year structure used throughout the project.

---

## Demo Data Disclaimer

The repository includes an **explicitly labeled synthetic demo dataset** so the analytics pipeline can be run locally without depending on external APIs.

The synthetic dataset exists to demonstrate:

- Data processing
- ETL
- SQL storage and analysis
- Data modeling
- Dashboard functionality

Synthetic values should **not** be interpreted or presented as actual NYC economic statistics.

The live-data acquisition component demonstrates how real datasets can be retrieved from the U.S. Census Bureau and NYC Open Data.

