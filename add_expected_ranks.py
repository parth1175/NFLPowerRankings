
import pandas as pd
import datetime
import time


rank_df = pd.read_csv('ranking.csv')
##print(rank_df)

##print(rank_df["ranking"])

##for i,row in rank_df.iterrows():
##    print(row)

##print(rank_df[rank_df["team"]=='Buffalo Bills'])
##print(rank_df.dtypes)
rank_df['DateTime'] = pd.to_datetime(rank_df[['year','month','day']])

##print(rank_df)
expected_r = []
for i, row in rank_df.iterrows():
    temp1 = rank_df[rank_df['DateTime'] - datetime.timedelta(7) ==row['DateTime']]

    temp2 = temp1[temp1['team']==row['team']]
    
    if temp2.empty:
        expected_r.append(None)
    else:
        expected_r.append(int(temp2['ranking'].item()))

##print(expected_r)
exp = pd.DataFrame(expected_r)
rank_df['Expected'] = expected_r
print(rank_df)
rank_df.to_csv('expected.csv')
    ##rank_df[rank_df['team']==row['team'] & 