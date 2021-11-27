import pandas as pd
import datetime

# Read CSV file into DataFrame df_ranking
df_ranking = pd.read_csv('ranking.csv')
df_schedule = pd.read_csv('master_schedule.csv')

# print(df_schedule.columns)
# df_schedule = df_schedule.rename(columns={"Winner/tie": "team", "Loser/tie": "opponent"})
# df_schedule = df_schedule[df_schedule.Date != '2021-11-28']
#
# df_schedule_flipped = df_schedule[['Date', 'opponent', 'team', 'PtsW', 'PtsL']]
# df_schedule_flipped = df_schedule_flipped.rename(columns={'opponent': 'team', 'team': 'opponent'})
# appended_schedule = pd.concat([df_schedule, df_schedule_flipped])

# print((full_schedule_list))

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(df_schedule_flipped)

schedule_dict = {}
# print(df_ranking.columns)
for index, row in df_schedule.iterrows():
    date, team1, team2, ptsW, ptsL = row
    schedule_dict.setdefault(date, {})[team1] = team2

# appended_schedule.to_csv("master_schedule_appended.csv", index=False)

# data = pd.read_csv('./weeklyMatchups.csv')
# roster = pd.Dataframe(data)


# Show dataframe
ranking_dict = {}
# print(df_ranking.columns)
for index, row in df_ranking.iterrows():
    year, month, day, team, ranking = row
    str_date = datetime.date(year, month, day).strftime("%Y-%m-%d")
    # ranking_dict[str_date][team] = ranking
    ranking_dict.setdefault(str_date, {})[team] = ranking

opponent_ranks = []
for date in schedule_dict.keys():
    for team, opponent in schedule_dict[date].items():
        opponent_rank = 0
        try:
            opponent_rank = ranking_dict[date][opponent]
        except:
            print('error')

        opponent_ranks.append(opponent_rank)

df_schedule.insert(4, "opponent_rank", opponent_ranks, True)



# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(full_schedule_list)

