import pandas as pd

final = pd.read_csv('ECE_4420_NFL_Power_Rankings/FinalData.csv')
Finaldf = pd.DataFrame(final)

weighted_SM = []
counter = 0


for index, row in Finaldf.iterrows():
    counter = counter+1
    Orank = row[4]
    SM = row[21]
    if(SM>0):
        weighted_SM.append((33-Orank)*SM)
    elif(SM<0):
        weighted_SM.append(Orank*SM)
    else:
        weighted_SM.append(0)


print(counter)
print(len(weighted_SM))
Finaldf["weighted_SM"] = weighted_SM
Finaldf.to_csv("ECE_4420_NFL_Power_Rankings/FinalData.csv", index=False)
