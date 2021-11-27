## combine stats with rankings

import pandas as pd
import datetime
import time


rank_df = pd.read_csv('expected.csv')
print(rank_df)

master = pd.read_csv('master_schedule.csv')
print(master)

print(rank_df.dtypes)
print(master.dtypes)

merged = pd.merge(rank_df,master,how="left",on=["team","year","month","day"])

print(merged)

margin = pd.read_csv('scoring_margin.csv')
print(margin.dtypes)
##margin['year']= pd.to_numeric(margin['year'],errors='coerce').isnull()
##print(margin[pd.to_numeric(margin['year'],errors='coerce').isnull()])

print(margin.dtypes)

full = pd.merge(merged,margin,how="left",on=["team","year","month","day"])


print(full)

full.to_csv('test.csv')
