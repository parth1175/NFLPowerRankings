import pandas as pd


team_dict = {
    'Dallas Cowboys': 'Dallas',
    'Tampa Bay Buccaneers': 'Tampa Bay',
    'Buffalo Bills': 'Buffalo',
    'New England Patriots': 'New England',
    'Arizona Cardinals': 'Arizona',
    'Kansas City Chiefs': 'Kansas City',
    'New Orleans Saints': 'New Orleans',
    'Tennessee Titans': 'Tennessee',
    'Green Bay Packers': 'Green Bay',
    'Los Angeles Rams': 'LA Rams',
    'Baltimore Ravens': 'Baltimore',
    'San Francisco 49ers': 'San Francisco',
    'Minnesota Vikings': 'Minnesota',
    'Seattle Seahawks': 'Seattle',
    'Philadelphia Eagles': 'Philadelphia',
    'Los Angeles Chargers': 'LA Chargers',
    'Indianapolis Colts': 'Indianapolis',
    'Cleveland Browns': 'Cleveland',
    'Denver Broncos': 'Denver',
    'Carolina Panthers': 'Carolina',
    'Pittsburgh Steelers': 'Pittsburgh',
    'Cincinnati Bengals': 'Cincinnati',
    'Las Vegas Raiders': 'Las Vegas',
    'Washington Football Team': 'Washington',
    'New York Giants': 'NY Giants',
    'Miami Dolphins': 'Miami',
    'Chicago Bears': 'Chicago',
    'Jacksonville Jaguars': 'Jacksonville',
    'Atlanta Falcons': 'Atlanta',
    'Detroit Lions': 'Detroit',
    'New York Jets': 'NY Jets',
    'Houston Texans': 'Houston',
    'LA Chargers': 'LA Chargers',
    'San Diego Chargers': 'LA Chargers',
    'Oakland Raiders': 'Las Vegas',
    'St. Louis Rams': 'LA Rams',
    'Washington Redskins': 'Washington'
}


# reading the csv file
df = pd.read_csv("ranking_old.csv")

# updating the column value/data
i = 0
for index, row in df.iterrows():
    team = row[3]
    city_team = team_dict[team]
    df.loc[i, 'team'] = city_team
    i += 1

# writing into the file
df.to_csv("ranking.csv", index=False)
