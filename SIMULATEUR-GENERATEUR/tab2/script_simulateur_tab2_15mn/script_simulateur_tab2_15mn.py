import pickle
import itertools
import numpy as np
import pandas as pd
import datetime
import random

a = [[1,2,3,4],[1,2,3,4,5,6,7,8,9],[1,2,3,4]]
famille = list(itertools.product(*a))

my_data = []
for i in famille:
    my_data.append(list(i))

my_data = np.array(my_data)

column_names = ["depart", "type_mesure", "phase"]
data_df = pd.DataFrame(my_data, columns=column_names)
data = data_df.drop((data_df.loc[(data_df['type_mesure'].isin([1,2,3,7])) & (data_df['phase'].isin([1,2,3]))].index) | (data_df.loc[(data_df['type_mesure'].isin([8,9])) & 
                    (data_df['phase'].isin([4]))].index))

hr = int(datetime.datetime.now().strftime("%H"))
mn = int(datetime.datetime.now().strftime("%M"))
da_hr_ms = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
data['heure_mesure'] = hr
data['minute_mesure'] = mn



with open('r16_tab1_energie.pkl', "rb") as f:
    eng = pickle.load(f)
with open('r16_tab1_facteur_puissance.pkl', "rb") as f:
    fct_p = pickle.load(f)
with open('r16_tab1_frequence.pkl', "rb") as f:
    freq = pickle.load(f)
with open('r16_tab1_puissance_active.pkl', "rb") as f:
    pui_act = pickle.load(f)
with open('r16_tab1_puissance_apparente.pkl', "rb") as f:
    pui_app = pickle.load(f)
with open('r16_tab1_puissance_reactive.pkl', "rb") as f:
    pui_rea = pickle.load(f)
with open('r16_tab1_taux_de_charge.pkl', "rb") as f:
    tx_ch = pickle.load(f)
with open('r16_tab1_tdh_courant.pkl', "rb") as f:
    tdh_c = pickle.load(f)
with open('r16_tab1_tdh_tension.pkl', "rb") as f:
    tdh_t = pickle.load(f)


# data['mesure'] = data['type_mesure']
# df1 = data.loc[data['type_mesure']==1]
data_omo = data.copy()

data['type_mesure'].loc[data['type_mesure']==1] = eng.predict(data_omo.loc[data['type_mesure']==1]) + random.uniform(-0.009, 0.01)
data['type_mesure'].loc[data['type_mesure']==2] = fct_p.predict(data_omo.loc[data_omo['type_mesure']== 2]) + random.uniform(-0.009, 0.01)
data['type_mesure'].loc[data['type_mesure']==3] = freq.predict(data_omo.loc[data_omo['type_mesure']== 3]) + random.uniform(-0.009, 0.01)
data['type_mesure'].loc[data['type_mesure']==4] = pui_act.predict(data_omo.loc[data_omo['type_mesure']== 4]) + random.uniform(-0.009, 0.01)
data['type_mesure'].loc[data['type_mesure']==5] = pui_app.predict(data_omo.loc[data_omo['type_mesure']== 5 ]) + random.uniform(-0.009, 0.01)
data['type_mesure'].loc[data['type_mesure']==6] = pui_rea.predict(data_omo.loc[data_omo['type_mesure']== 6 ]) + random.uniform(-0.009, 0.01)
data['type_mesure'].loc[data['type_mesure']==7] = tx_ch.predict(data_omo.loc[data_omo['type_mesure']== 7 ]) + random.uniform(-0.009, 0.01)
data['type_mesure'].loc[data['type_mesure']==8] = tdh_c.predict(data_omo.loc[data_omo['type_mesure']== 8 ]) + random.uniform(-0.009, 0.01)
data['type_mesure'].loc[data['type_mesure']==9] = tdh_t.predict(data_omo.loc[data_omo['type_mesure']== 9 ]) + random.uniform(-0.009, 0.01)

data['mesure'] = data['type_mesure']
data['type_mesure'] = data_omo['type_mesure']

data['type_mesure'] = data['type_mesure'].map({
                             1:'energie',
                             2:'facteur_puissance',
                             3:'frequence',
                             4:'puissance_active',
                             5:'puissance_apparente',
                             6:'puissance_reactive',
                             7:'taux_de_charge',
                             8:'tdh_courant',
                             9:'tdh_tension'
                             },
                             na_action=None)

data['phase']= data['phase'].replace([4],[ np.nan])


data['date_heure_mesure'] = da_hr_ms
data = data.drop(columns=['heure_mesure', 'minute_mesure'])

data['id_poste'] = 'P0016.210.043'
data['zone_poste'] = 'tab2'
data['classification'] = 'CLA_BT'
data['date_heure_transfert'] = da_hr_ms
data['unite_mesure'] = data['type_mesure']
data['unite_mesure'].loc[data['unite_mesure'].isin(['energie'])] = 'MWh'
data['unite_mesure'].loc[data['unite_mesure'].isin(['frequence'])] = 'Hz'
data['unite_mesure'].loc[data['unite_mesure'].isin(['puissance_active'])] = 'W'
data['unite_mesure'].loc[data['unite_mesure'].isin(['puissance_apparente'])] = 'VA'
data['unite_mesure'].loc[data['unite_mesure'].isin(['puissance_reactive'])] = 'VAR'
data['unite_mesure'].loc[data['unite_mesure'].isin(['facteur_puissance', 'taux_de_charge', 'tdh_courant', 'tdh_tension'])] = '%'
data['phase'] = data['phase'].astype(str)
data['description_mesure'] = 'mesure - ' + data['type_mesure'] + ' phase ' +  data['phase']


data = data[[
    'id_poste', 'zone_poste', 'classification', 'depart', 
    'type_mesure', 'description_mesure', 'phase', 'mesure',
    'unite_mesure', 'date_heure_mesure','date_heure_transfert'
    ]]
    
# Enregistrement du dataframe commes fichier json
dataDB = data.copy()

for b in dataDB.index:
    dataDB = data.copy()
    dataDB = dataDB[dataDB.index == b]
    data_log = dataDB.to_json(orient = 'records', lines=True)
    files_name = 'R16_Tab2_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))

    file = open(files_name, "a+")
    file.write(data_log)
    file.close()

# data_log = data.to_json(orient = 'records', lines=True)

# files_name = 'R16_Tab1_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))

# file = open(files_name, "a+")
# file.write(data_log)
# file.close()
