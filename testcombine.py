## combine stats with rankings

import pandas as pd
import datetime
import time


rank_df = pd.read_csv('expected.csv')
print(rank_df)
for i, row in rank_df.iterrows():
    print(row)
##print(rank_df['Expected'])
total_points = pd.read_csv('total_points_per_game.csv')
print(total_points)

merged = pd.merge(rank_df,total_points,how="inner",on=["team","year","month","day"])

print(merged)