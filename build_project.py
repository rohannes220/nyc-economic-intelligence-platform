from pathlib import Path
import pandas as pd, numpy as np, sqlite3, json
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from joblib import dump
ROOT=Path(__file__).parent
for d in ['data/raw','data/processed','models','reports']: (ROOT/d).mkdir(parents=True,exist_ok=True)
# Offline demo snapshot, clearly marked. The fetch script replaces this with live public data.
years=list(range(2015,2025)); boroughs=['Bronx','Brooklyn','Manhattan','Queens','Staten Island']
base={'Bronx':(39000,1450,7.2,5200),'Brooklyn':(52000,1650,5.8,12000),'Manhattan':(78000,2100,5.2,18000),'Queens':(56000,1700,5.5,10500),'Staten Island':(68000,1500,4.9,3200)}
rows=[]
for b in boroughs:
    income,rent,unemp,biz=base[b]
    for i,y in enumerate(years):
        shock=2.5 if y==2020 else (1.1 if y==2021 else 0)
        rows.append([b,y,round(income*(1.025**i)),round(rent*(1.035**i)),round(max(3,unemp-0.12*i+shock),1),round(biz*(1.018**i)*(0.94 if y==2020 else 1)),round(900+40*i+(120 if b in ['Brooklyn','Queens'] else 0))])
df=pd.DataFrame(rows,columns=['borough','year','median_household_income','median_gross_rent','unemployment_rate','licensed_businesses','building_permits'])
df['rent_to_monthly_income_pct']=(df.median_gross_rent/(df.median_household_income/12)*100).round(1)
df['income_yoy_pct']=df.groupby('borough').median_household_income.pct_change().mul(100).round(2)
df['rent_yoy_pct']=df.groupby('borough').median_gross_rent.pct_change().mul(100).round(2)
df['affordability_gap_pp']=(df.rent_yoy_pct-df.income_yoy_pct).round(2)
df.to_csv(ROOT/'data/processed/borough_year_metrics_demo.csv',index=False)
# SQLite warehouse
con=sqlite3.connect(ROOT/'nyc_economic_intelligence.db')
pd.DataFrame({'borough_id':range(1,6),'borough':boroughs}).to_sql('dim_borough',con,index=False,if_exists='replace')
pd.DataFrame({'year_id':years,'year':years}).to_sql('dim_year',con,index=False,if_exists='replace')
f=df.merge(pd.read_sql('select * from dim_borough',con),on='borough').rename(columns={'year':'year_id'}).drop(columns='borough')
f.to_sql('fact_economic_metrics',con,index=False,if_exists='replace')
con.execute('CREATE INDEX IF NOT EXISTS idx_fact_borough_year ON fact_economic_metrics(borough_id, year_id)'); con.commit(); con.close()
# Simple forecasting demo: next-year unemployment per borough using linear trend, held-out last 2 years
metrics=[]; forecasts=[]
for b,g in df.groupby('borough'):
    g=g.sort_values('year'); train=g.iloc[:-2]; test=g.iloc[-2:]
    m=LinearRegression().fit(train[['year']],train['unemployment_rate'])
    pred=m.predict(test[['year']]); mae=mean_absolute_error(test.unemployment_rate,pred)
    metrics.append({'borough':b,'holdout_mae':round(mae,3)})
    forecasts.append({'borough':b,'forecast_year':2025,'forecast_unemployment_rate':round(float(m.predict(pd.DataFrame({'year':[2025]}))[0]),2)})
pd.DataFrame(metrics).to_csv(ROOT/'reports/model_metrics_demo.csv',index=False)
pd.DataFrame(forecasts).to_csv(ROOT/'reports/2025_unemployment_forecast_demo.csv',index=False)
dump(m,ROOT/'models/example_linear_regression.joblib')
print(json.dumps({'rows':len(df),'boroughs':5,'years':len(years)},indent=2))
