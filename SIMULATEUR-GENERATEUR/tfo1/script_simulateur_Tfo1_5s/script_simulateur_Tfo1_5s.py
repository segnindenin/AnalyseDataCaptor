import itertools
import datetime
import numpy as np
import pandas as pd
import random

a = [[1,2,3,4,5,6,7],[1,2,3,4]]
famille = list(itertools.product(*a))

my_data = []
for i in famille:
    my_data.append(list(i))

my_data = np.array(my_data)

column_names = ["type_mesure", "phase"]
data_df = pd.DataFrame(my_data, columns=column_names)
data = data_df.drop(data_df.loc[(data_df['type_mesure'].isin([2,4,5,6,7])) & (data_df['phase'].isin([4]))].index)


hr = int(datetime.datetime.now().strftime("%H"))
mn = int(datetime.datetime.now().strftime("%M"))
sd = int(datetime.datetime.now().strftime("%S"))
da_hr_ms = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
data['heure_mesure'] = hr
data['minute_mesure'] = mn
data['seconde_mesure'] = sd

mon_dictionnaire = {'courant': int(1), 'courant_hta': int(2), 'desequilibre_courant':int(3),  
                    'tension_n':int(4), 'tension_ph':int(5), 'tension_ph_hta':int(6), 
                    'desequilibre_tension':int(7)}

import pickle

with open('r16_Tfo1_courant.pkl', "rb") as a:
    crt = pickle.load(a)
with open('r16_Tfo1_courant_hta.pkl', "rb") as b:
    crt_hta = pickle.load(b)
with open('r16_Tfo1_desequilibre_courant.pkl', "rb") as c:
    des_crt = pickle.load(c)
with open('r16_Tfo1_tension_n.pkl', "rb") as d:
    ten = pickle.load(d)
with open('r16_Tfo1_tension_ph.pkl', "rb") as e:
    ten_ph = pickle.load(e)
with open('r16_Tfo1_tension_ph_hta.pkl', "rb") as f:
    ten_ph_hta = pickle.load(f)
with open('r16_Tfo1_desequilibre_tension.pkl', "rb") as g:
    des_ten = pickle.load(g)


data_omo = data.copy()

data['type_mesure'].loc[data['type_mesure']==1] = crt.predict(data_omo.loc[data['type_mesure']==1]) + random.uniform(-0.09, 0.1)
data['type_mesure'].loc[data['type_mesure']==2] = crt_hta.predict(data_omo.loc[data_omo['type_mesure']== 2]) + random.uniform(-0.09, 0.1)
data['type_mesure'].loc[data['type_mesure']==3] = des_crt.predict(data_omo.loc[data_omo['type_mesure']== 3]) + random.uniform(-0.09, 0.1)
data['type_mesure'].loc[data['type_mesure']==4] = ten.predict(data_omo.loc[data_omo['type_mesure']== 4]) + random.uniform(-0.09, 0.1)
data['type_mesure'].loc[data['type_mesure']==5] = ten_ph.predict(data_omo.loc[data_omo['type_mesure']== 5 ]) + random.uniform(-0.09, 0.1)
data['type_mesure'].loc[data['type_mesure']==6] = ten_ph_hta.predict(data_omo.loc[data_omo['type_mesure']== 6 ]) + random.uniform(-0.09, 0.1)
data['type_mesure'].loc[data['type_mesure']==7] = des_ten.predict(data_omo.loc[data_omo['type_mesure']== 7 ]) + random.uniform(-0.09, 0.1)


data['mesure'] = data['type_mesure']
data['type_mesure'] = data_omo['type_mesure']

data['type_mesure'] = data['type_mesure'].map({
                             1:'courant',
                             2:'courant_hta',
                             3:'desequilibre_courant',
                             4:'tension_n',
                             5:'tension_ph',
                             6:'tension_ph_hta',
                             7:'desequilibre_tension'                   
                             },
                             na_action=None)

data['phase']= data['phase'].replace([4],['N'])

data['date_heure_mesure'] = da_hr_ms
data = data.drop(columns=['heure_mesure', 'minute_mesure', 'seconde_mesure'])

data['id_poste'] = 'P0016.210.043'
data['zone_poste'] = 'transfo1'
data['classification'] = 'CLA_BT'
data['classification'].loc[data['type_mesure'].isin(['tension_ph_hta', 'courant_hta'])] = 'CLA_HTA'
data['date_heure_transfert'] = da_hr_ms
data['unite_mesure'] = data['type_mesure']
data['unite_mesure'].loc[data['unite_mesure'].isin(['energie'])] = 'MWh'
data['unite_mesure'].loc[data['unite_mesure'].isin(['frequence'])] = 'Hz'
data['unite_mesure'].loc[data['unite_mesure'].isin(['puissance_active'])] = 'W'
data['unite_mesure'].loc[data['unite_mesure'].isin(['puissance_apparente'])] = 'VA'
data['unite_mesure'].loc[data['unite_mesure'].isin(['puissance_reactive'])] = 'VAR'
data['unite_mesure'].loc[data['unite_mesure'].isin(['facteur_puissance', 'taux_de_charge', 'tdh_courant', 'tdh_tension'])] = '%'
# data['phase'] = data['phase'].astype(int)
data['phase'] = data['phase'].astype(str)
data['description_mesure'] = 'mesure - ' + data['type_mesure'] + ' phase ' +  data['phase']

data = data[[
    'id_poste', 'zone_poste', 'classification', 
    'type_mesure', 'description_mesure', 'phase', 'mesure',
    'unite_mesure', 'date_heure_mesure','date_heure_transfert'
    ]]
    
# Enregistrement du dataframe commes fichier json
dataDB = data.copy()

for b in dataDB.index:
    dataDB = data.copy()
    dataDB = dataDB[dataDB.index == b]
    data_log = dataDB.to_json(orient = 'records', lines=True)
    files_name = 'R16_Tfo1_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))

    file = open(files_name, "a+")
    file.write(data_log)
    file.close()

# data_log = data.to_json(orient = 'records', lines=True)

# files_name = 'R16_Tfo1_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))

# file = open(files_name, "a+")
# file.write(data_log)
# file.close()
