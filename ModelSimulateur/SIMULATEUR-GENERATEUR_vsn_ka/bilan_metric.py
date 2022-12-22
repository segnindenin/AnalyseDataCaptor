########versus#######
import pandas as pd
import datetime

date = datetime.datetime.now().strftime("%Y-%m-%d")
df = pd.read_json(f"R16_tab1_2022-12-12.log", lines=True)
df = df.set_index('date_heure_mesure')
df.index = pd.to_datetime(df.index)
hr = int(datetime.datetime.now().strftime("%H")) - 1
df['id_poste'][(df.index.hour==hr)].count()


#########versus#######
import datetime

date = datetime.datetime.now().strftime('%Y-%m-%d')
hr = int(datetime.datetime.now().strftime('%H') - 1)
file = open(f'{date}.log','r')


words_Tfo1 = [f'date_heure_mesure":"{date} {hr}:', 'transfo1']
words_Tfo2 = [f'date_heure_mesure":"{date} {hr}:', 'transfo2']

NbreTfo1=0
NbreTfo2=0
lines=file.readlines()
for line in lines:
    if all(word in line for word in words_Tfo1):
        NbreTfo1+=1
    if all(word in line for word in words_Tfo2):
        NbreTfo2+=1 

print(NbreTfo1 , NbreTfo1)
