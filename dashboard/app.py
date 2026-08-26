import streamlit as st, pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/processed/borough_year_metrics_demo.csv')
st.set_page_config(page_title='NYC Economic Intelligence',layout='wide')
st.title('NYC Economic Intelligence Platform')
st.caption('Portfolio demo. Replace demo snapshot by running src/fetch_live_data.py and the live ETL.')
year=st.selectbox('Year',sorted(df.year.unique(),reverse=True)); x=df[df.year==year]
c1,c2,c3=st.columns(3); c1.metric('Median borough income',f"${x.median_household_income.median():,.0f}"); c2.metric('Median gross rent',f"${x.median_gross_rent.median():,.0f}"); c3.metric('Median unemployment',f"{x.unemployment_rate.median():.1f}%")
st.subheader('Affordability pressure'); st.bar_chart(x.set_index('borough')['rent_to_monthly_income_pct'])
st.subheader('Unemployment by borough'); st.bar_chart(x.set_index('borough')['unemployment_rate'])
st.subheader('Economic metrics'); st.dataframe(x,use_container_width=True)
