-- 1) Borough affordability: rent burden relative to monthly household income
SELECT b.borough, f.year_id AS year,
       f.median_household_income, f.median_gross_rent,
       f.rent_to_monthly_income_pct
FROM fact_economic_metrics f JOIN dim_borough b USING (borough_id)
ORDER BY year DESC, rent_to_monthly_income_pct DESC;

-- 2) Rank boroughs by unemployment each year (window function)
WITH ranked AS (
 SELECT b.borough, f.year_id AS year, f.unemployment_rate,
        RANK() OVER (PARTITION BY f.year_id ORDER BY f.unemployment_rate DESC) AS stress_rank
 FROM fact_economic_metrics f JOIN dim_borough b USING (borough_id)
)
SELECT * FROM ranked ORDER BY year DESC, stress_rank;

-- 3) Year-over-year business activity with LAG
SELECT b.borough, f.year_id AS year, f.licensed_businesses,
       LAG(f.licensed_businesses) OVER(PARTITION BY f.borough_id ORDER BY f.year_id) AS prior_year,
       ROUND(100.0*(f.licensed_businesses-LAG(f.licensed_businesses) OVER(PARTITION BY f.borough_id ORDER BY f.year_id)) /
             NULLIF(LAG(f.licensed_businesses) OVER(PARTITION BY f.borough_id ORDER BY f.year_id),0),2) AS yoy_pct
FROM fact_economic_metrics f JOIN dim_borough b USING (borough_id)
ORDER BY borough, year;

-- 4) Where rent growth is outpacing income growth
SELECT b.borough, f.year_id AS year, f.rent_yoy_pct, f.income_yoy_pct, f.affordability_gap_pp
FROM fact_economic_metrics f JOIN dim_borough b USING (borough_id)
WHERE f.affordability_gap_pp > 0
ORDER BY affordability_gap_pp DESC;
