import pandas as pd
import matplotlib.pyplot as plt

import numpy as np

import xgboost as xgb
import pickle
import datetime
import itertools
import numpy as np
import pandas as pd
import random

a = [[1,2,3,4,5,6,7,8,9,10,11],[1,2,3,4,5]]
famille = list(itertools.product(*a))

my_data = []
for i in famille:
    my_data.append(list(i))

my_data = np.array(my_data)

column_names = ["type_mesure", "phase"]  #4,10 -- 5,11,6
data_df = pd.DataFrame(my_data, columns=column_names)
data = data_df.drop((data_df.loc[(data_df['type_mesure'].isin([6,11])) & (data_df['phase'].isin([1,2,3,4]))].index) |
                    (data_df.loc[(data_df['type_mesure'].isin([4,10])) & (data_df['phase'].isin([4]))].index) |
                    (data_df.loc[(data_df['type_mesure'].isin([1,7])) & (data_df['phase'].isin([5]))].index) |
                    (data_df.loc[(data_df['type_mesure'].isin([2,3,5,8,9])) & (data_df['phase'].isin([4,5]))].index)
)

hr = int(datetime.datetime.now().strftime("%H"))
mn = int(datetime.datetime.now().strftime("%M"))
sd = int(datetime.datetime.now().strftime("%S"))
da_hr_ms = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
data['heure_mesure'] = hr

import pickle

with open('r16_tfo1_max_courant.pkl', "rb") as a:
    Mcrt = pickle.load(a)
with open('r16_tfo1_max_tension_n.pkl', "rb") as b:
    Mten_n = pickle.load(b)
with open('r16_tfo1_max_tension_ph.pkl', "rb") as c:
    Mten_ph = pickle.load(c)
with open('r16_tfo1_max_puissance_reactive.pkl', "rb") as d:
    Mpui_rec = pickle.load(d)
with open('r16_tfo1_max_puissance_active.pkl', "rb") as e:
    Mpui_act = pickle.load(e)
with open('r16_tfo1_max_puissance_apparente.pkl', "rb") as f:
    Mpui_app = pickle.load(f)
with open('r16_tfo1_min_courant.pkl', "rb") as g:
    mcrt = pickle.load(g)
with open('r16_tfo1_min_tension_n.pkl', "rb") as h:
    mten_n = pickle.load(h)
with open('r16_tfo1_min_tension_ph.pkl', "rb") as i:
    mten_ph = pickle.load(i)
with open('r16_tfo1_min_puissance_reactive.pkl', "rb") as j:
    mpui_rec = pickle.load(j)
with open('r16_tfo1_min_puissance_apparente.pkl', "rb") as k:
    mpui_app = pickle.load(k)

data_omo = data.copy()

data['type_mesure'].loc[data['type_mesure']==1] = Mcrt.predict(data_omo.loc[data['type_mesure']==1])
data['type_mesure'].loc[data['type_mesure']==2] = Mten_n.predict(data_omo.loc[data_omo['type_mesure']== 2])
data['type_mesure'].loc[data['type_mesure']==3] = Mten_ph.predict(data_omo.loc[data_omo['type_mesure']== 3])
data['type_mesure'].loc[data['type_mesure']==4] = Mpui_rec.predict(data_omo.loc[data_omo['type_mesure']== 4])
data['type_mesure'].loc[data['type_mesure']==5] = Mpui_act.predict(data_omo.loc[data_omo['type_mesure']== 5])
data['type_mesure'].loc[data['type_mesure']==6] = Mpui_app.predict(data_omo.loc[data_omo['type_mesure']== 6])
data['type_mesure'].loc[data['type_mesure']==7] = mcrt.predict(data_omo.loc[data_omo['type_mesure']== 7])
data['type_mesure'].loc[data['type_mesure']==8] = mten_n.predict(data_omo.loc[data_omo['type_mesure']== 8])
data['type_mesure'].loc[data['type_mesure']==9] = mten_ph.predict(data_omo.loc[data_omo['type_mesure']== 9])
data['type_mesure'].loc[data['type_mesure']==10] = mpui_rec.predict(data_omo.loc[data_omo['type_mesure']== 10])
data['type_mesure'].loc[data['type_mesure']==11] = mpui_app.predict(data_omo.loc[data_omo['type_mesure']== 11])

data['mesure'] = data['type_mesure']
data['type_mesure'] = data_omo['type_mesure']

data['type_mesure'] = data['type_mesure'].map({
                            1:'max_courant', 2:'max_tension_n', 3:'max_tension_ph', 
                            4:'max_puissance_reactive', 5:'max_puissance_active', 6:'max_puissance_apparente',
                            7:'min_courant', 8:'min_tension_n', 9:'min_tension_ph', 10:'min_puissance_reactive',
                            11:'min_puissance_apparente'                   
                             },
                             na_action=None)

data['phase']= data['phase'].replace([4, 5],['N', ''])

data['date_heure_mesure'] = da_hr_ms
data = data.drop(columns=['heure_mesure'])

data['id_poste'] = 'P0016.210.043'
data['zone_poste'] = 'transfo1'
data['classification'] = 'CLA_BT'
# data['classification'].loc[data['type_mesure'].isin(['tension_ph_hta', 'courant_hta'])] = 'CLA_HTA'
data['date_heure_transfert'] = da_hr_ms
data['unite_mesure'] = data['type_mesure']
data['unite_mesure'].loc[data['unite_mesure'].isin(['max_courant', 'min_courant', '', ''])] = 'V'
data['unite_mesure'].loc[data['unite_mesure'].isin(['max_tension_n', 'min_tension_n', 'max_tension_ph', 'min_tension_ph'])] = 'A'
data['unite_mesure'].loc[data['unite_mesure'].isin(['min_puissance_active', 'max_puissance_active', '', '',''])] = 'W'
data['unite_mesure'].loc[data['unite_mesure'].isin(['max_puissance_apparente'])] = 'VA'
data['unite_mesure'].loc[data['unite_mesure'].isin(['max_puissance_reactive', 'min_puissance_reactive'])] = 'VAR'
# data['unite_mesure'].loc[data['unite_mesure'].isin(['facteur_puissance', 'taux_de_charge', 'tdh_courant', 'tdh_tension'])] = '%'
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

# files_name = 'R16_Tab1_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))

# file = open(files_name, "a+")
# file.write(data_log)
# file.close()
