"""Fetch live public data. Requires internet access.
Sources: Census ACS 5-year API + NYC Open Data Socrata APIs.
This script intentionally keeps source acquisition separate from transformations.
"""
from pathlib import Path
import requests, pandas as pd
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw'; RAW.mkdir(parents=True,exist_ok=True)
# ACS: median household income (B19013_001E), median gross rent (B25064_001E), unemployment inputs
for year in range(2015,2025):
    url=f'https://api.census.gov/data/{year}/acs/acs5?get=NAME,B19013_001E,B25064_001E,B23025_003E,B23025_005E&for=county:*&in=state:36'
    r=requests.get(url,timeout=60); r.raise_for_status(); data=r.json()
    pd.DataFrame(data[1:],columns=data[0]).to_csv(RAW/f'acs_ny_counties_{year}.csv',index=False)
# NYC licensed businesses (current snapshot; borough/community board geography)
url='https://data.cityofnewyork.us/resource/jff5-ygbi.json?$limit=50000'
r=requests.get(url,timeout=60); r.raise_for_status(); pd.DataFrame(r.json()).to_csv(RAW/'nyc_licensed_businesses.csv',index=False)
# DOB permit issuance; limit to a manageable portfolio snapshot. Dataset id ipu4-2q9a.
url='https://data.cityofnewyork.us/resource/ipu4-2q9a.json?$limit=50000&$order=issuance_date DESC'
r=requests.get(url,timeout=60); r.raise_for_status(); pd.DataFrame(r.json()).to_csv(RAW/'dob_permits_recent.csv',index=False)
print('Live source files downloaded to',RAW)
