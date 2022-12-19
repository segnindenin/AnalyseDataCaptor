# dependence
import itertools
import numpy as np
import pandas as pd
import random
import datetime
import pickle

# definition des variables
a = [[1,2,3,4],[1,2,3,4,5],[1,2,3,4]]
famille = list(itertools.product(*a))

my_data = []
for i in famille:
    my_data.append(list(i))

my_data = np.array(my_data)

column_names = ["depart", "type_mesure", "phase"]
data_df = pd.DataFrame(my_data, columns=column_names)
data = data_df.drop(data_df.loc[(data_df['type_mesure'].isin([1,2,4])) & (data_df['phase'] == 4)].index)


hr = int(datetime.datetime.now().strftime("%H"))
mn = int(datetime.datetime.now().strftime("%M"))
sd = int(datetime.datetime.now().strftime("%S"))
da_hr_ms = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
data['heure_mesure'] = hr
data['minute_mesure'] = mn
data['seconde_mesure'] = sd


# ouverture du model pre-entraîner
with open('r16_tab1_5s.pkl', "rb") as f:
    reg = pickle.load(f)

data['mesure'] = reg.predict(data) + random.uniform(-0.09, 0.1)


# decriptages des données
data['type_mesure'] = data['type_mesure'].map({
                             1:'tension_ph',
                             2:'tension_n',
                             3:'courant',
                             4:'desequilibre_tension',
                             5:'desequilibre_courant'
                             },
                             na_action=None)

data['phase']= data['phase'].replace([4],['N'])


# definitions des colonnes du dataframes
data['date_heure_mesure'] = da_hr_ms
data = data.drop(columns=['heure_mesure', 'minute_mesure', 'seconde_mesure'])

data['id_poste'] = 'P0016.210.043'
data['zone_poste'] = 'tab1'
data['classification'] = 'CLA_BT'
data['date_heure_transfert'] = da_hr_ms
data['unite_mesure'] = data['type_mesure']
data['unite_mesure'].loc[data['unite_mesure'] == 'courant'] = 'A'
data['unite_mesure'].loc[data['unite_mesure'].isin(['tension_n', 'tension_ph'])] = 'V'
data['unite_mesure'].loc[data['unite_mesure'].isin(['desequilibre_courant', 'desequilibre_tension'])] = '%'
data['phase'] = data['phase'].astype(str)
data['description_mesure'] = 'mesure - ' + data['type_mesure'] + ' phase ' +  data['phase']

# recadrement du dataframe
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
    files_name = 'R16_Tab1_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))

    file = open(files_name, "a+")
    file.write(data_log)
    file.close()

# data_log = data.to_json(orient = 'records', lines=True)

# files_name = 'R16_Tab1_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))

# file = open(files_name, "a+")
# file.write(data_log)
# file.close()
