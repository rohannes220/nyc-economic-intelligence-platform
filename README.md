# NYC Economic Intelligence Platform

An end-to-end analytics portfolio project that asks: **How are economic conditions changing across New York City, which boroughs are under the most economic/affordability pressure, and what indicators are associated with those changes?**

## What it demonstrates
Python ETL, multi-source public data integration, SQL dimensional modeling, advanced SQL (CTEs/window functions/LAG/ranking), data-quality checks, BI-style dashboarding, and a deliberately simple linear-regression forecast.

## Architecture
`Public APIs -> Python ETL -> cleaned borough/year metrics -> SQL warehouse -> analytical SQL -> dashboard -> simple forecast`

## Public data sources
- U.S. Census ACS 5-year API: household income, gross rent, employment/unemployment inputs.
- NYC Open Data / DCWP: licensed businesses by borough/community-board geography.
- NYC Open Data / DOB: building permit issuance as a development/activity indicator.

`src/fetch_live_data.py` downloads the live source files. The repository also contains an **explicitly labeled synthetic demo snapshot** so the SQL schema, dashboard, and modeling pipeline can be run offline. Do not present demo values as real NYC statistics.

## Warehouse
- `dim_borough`
- `dim_year`
- `fact_economic_metrics`

Metrics include median household income, median gross rent, unemployment rate, licensed-business count, building permits, rent-to-income ratio, and YoY affordability gap.

## Key analytical questions
1. Where is rent consuming the largest share of monthly household income?
2. Where is rent growth outpacing income growth?
3. Which boroughs show the highest unemployment pressure?
4. How does business/development activity differ across boroughs and over time?
5. What does a simple historical trend suggest for the next period's unemployment rate?

## ML scope
The model is intentionally simple: linear regression forecasts a selected economic indicator from historical trend. The goal is not sophisticated ML; the portfolio value is the end-to-end data pipeline and defensible analytics.

## Run offline demo
```bash
python build_project.py
streamlit run dashboard/app.py
```

## Fetch live public data
```bash
python src/fetch_live_data.py
```
Then transform the downloaded source files into the warehouse using the same borough/year grain. The acquisition layer is isolated so source refreshes do not require rewriting the analytical layer.

## Interview summary
“I built an economic intelligence platform that integrates public demographic, housing, business, and development data for New York City. I used Python for ETL, modeled borough-year metrics in a SQL warehouse, wrote window-function and year-over-year analytical queries, built an interactive dashboard, and added a simple regression forecast. The main analysis focuses on affordability pressure and differences in economic conditions across boroughs.”
