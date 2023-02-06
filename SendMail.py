# import smtplib, ssl
# from email.message import EmailMessage
# import json


# with open ('datarapport.log', 'r') as f:
#     data = json.load(f)
# print(data['total'])

# msg = EmailMessage()
# msg.set_content(f"""date_heure : {data['date_heure']}
# zone_poste : {data['zone_poste']}
# total : {data['total']}
# """)
# msg["Subject"] = "Email de Test"
# msg["From"] = "coulibalyoumar260@gmail.com"
# msg["To"] = "segnindenin.coulibaly@uvci.edu.ci"
# context=ssl.create_default_context()
# with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#     smtp.login(msg["From"], "zggeyvajuyhiewnm")
#     smtp.send_message(msg)
#     print('email envoyé')


################################################################

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import smtplib, ssl
import json

date = datetime.datetime.now().strftime('%Y-%m-%d')
hr = int(datetime.datetime.now().strftime('%H')) - 5
if hr < 0:
    hr = 23
if hr < 10:
    hr = f'0{hr}'
file_tfo = open(f'{date}.log','r')
Metric = {'"energie"':4,'"facteur_puissance"':4,'"frequence"':4,'"puissance_active"':12,'"puissance_apparente"':12,'"puissance_reactive"':12,'"taux_de_charge"':4,
'"tdh_courant"':16,'"tdh_tension"':12, '"tension_ph"':360,'"tension_n"':360,'"courant"':480,'"courant_hta"':480,'"tension_ph_hta"':360,'"desequilibre_tension"':12,
'"desequilibre_courant"':16, '"temperature_point_chaud_bt"':16, '"temperature_tranfo"':4}

words_Tfo1 = ['transfo1', f'date_heure_mesure":"{date} {hr}:' ]
words_Tfo2 = [f'date_heure_mesure":"{date} {hr}:', 'transfo2']
NbreTfo1=0
NbreTfo2=0
for line in file_tfo.readlines():
    if all(word in line for word in words_Tfo1):
        NbreTfo1+=1
    if all(word in line for word in words_Tfo2):
        NbreTfo2+=1
print(NbreTfo1)
NbreTfo1 = int((NbreTfo1*100)/2168)
NbreTfo2 = int((NbreTfo2*100)/2168)
dictionnaire = {'transfo1':NbreTfo1, 'transfo2':NbreTfo2}

for zp,tx in dictionnaire.items():
    if (tx < 85) | (tx > 115):
        fichier = open(f"datarapport.log", "w")
        fichier.write(f"""{{"date_heure":"{date} {hr}", "zone_poste":"{zp}", "total":"{tx}"}}
        """)
        fichier.close()
        with open ('datarapport.log', 'r') as f:
            data = json.load(f)
            print(data['total'])
        
        prmt = []
        for m,v in Metric.items():
            # print(m, v, zp)
            file = open(f'{date}.log','r')
            Drill = [zp,m, f'date_heure_mesure":"{date} {hr}:']
            NbreMetric = 0            
            for lines in file.readlines():
                if all(word in lines for word in Drill):
                    NbreMetric+=1       
            print(NbreMetric)
            pct = int((NbreMetric*100)/v)
            if (pct < 95) | (pct > 105):
                prmt.append(m)
                
        # on crée un e-mail
        message = MIMEMultipart("alternative")
        # on ajoute un sujet
        message["Subject"] = f"Rapport de Collecte des Données du {date} de {hr}h00mn à {hr}h59mn "
        # un émetteur
        message["From"] = "coulibalyoumar260@gmail.com"
        # un destinataire
        message["To"] = "segnindenin.coulibaly@uvci.edu.ci"

        # on crée un texte et sa version HTML
        bilan = {'faible taux':data['total'] , 'taux éléver':data['total']}
        if tx < 95:
            note = 'faible taux'
            comparaison = 'inferieur'
            tx_norm = 95
        if tx > 105:
            note = 'taux élever'
            comparaison = 'superieur'
            tx_norm = 105
                
        LackMetric = ', '.join(prmt)
        print((LackMetric))
        html = f'''
        <html>
        <body onload="brython()">
        <h1>Bonsoir à vous</h1>
        <p>zone de poste : <font color = "red">{zp}</font><br>
        Nous vous informons par ce mail que le taux de collecte de {hr}h était d'un <b>{note}</b> dans la zone de poste de distribution {zp}.<br>
        <b font-size = "7">Taux de Collecte: <font color = "red">{tx}%</font></b><br>
        <b font-size = "7">Nombre de Donnée manquante est d'environ: <font color = "red">{2168-((tx*2168)/100)} Metrics</font></b><br>
        PS: veuillez consultez le module Explorarion des Données pour plus de details.
        <br>
        En effet les metrics provenant de la <b>{LackMetric}<b> ont un taux de collecte {comparaison} à {tx_norm}%.
        <br>
        <a href="https://datascientest.com">Explorer les Données</a>
        </body>
        </html>
        '''

        # on crée deux éléments MIMEText 
        html_mime = MIMEText(html, 'html')

        # on attache ces deux éléments 
        message.attach(html_mime)

        # on crée la connexion
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # connexion au compte
            server.login(message["From"], "zggeyvajuyhiewnm")
            # envoi du mail
            server.sendmail(message["From"], message["to"], message.as_string())
            print('email envoyé')

    else:
        print("Le taux de collecte des Données est normal")


#############################################################


# import datetime
# import smtplib, ssl
# from email.message import EmailMessage
# import json

# date = datetime.datetime.now().strftime('%Y-%m-%d')
# hr = int(datetime.datetime.now().strftime('%H')) - 3
# if hr < 0:
#     hr = 23
# if hr < 10:
#     hr = f'0{hr}'
# file_tfo = open(f'hoursReporting/chanel-tfo/{date}.log','r')
# words_Tfo1 = [f'date_heure_mesure":"{date} {hr}:', 'transfo1']
# words_Tfo2 = [f'date_heure_mesure":"{date} {hr}:', 'transfo2']
# NbreTfo1=0
# NbreTfo2=0
# for line in file_tfo.readlines():
#     if all(word in line for word in words_Tfo1):
#         NbreTfo1+=1
#     if all(word in line for word in words_Tfo2):
#         NbreTfo2+=1
# nombreinfotfo = 5616

# if NbreTfo1 != 1250:
#     fichier = open(f"datarapport.log", "w")
#     fichier.write(f"""{{"date_heure":"{date} {hr}", "zone_poste":"tfo1", "total":"{NbreTfo1}"}}
#     """)
#     fichier.close()

#     with open ('datarapport.log', 'r') as f:
#         data = json.load(f)
#     print(data['total'])

#     msg = EmailMessage()
#     msg.set_content(f"""date_heure : {data['date_heure']}
#     zone_poste : {data['zone_poste']}
#     total : {data['total']}
#     """)
#     msg["Subject"] = "Email de Test"
#     msg["From"] = "coulibalyoumar260@gmail.com"
#     msg["To"] = "segnindenin.coulibaly@uvci.edu.ci"
#     context=ssl.create_default_context()
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#         smtp.login(msg["From"], "zggeyvajuyhiewnm")
#         smtp.send_message(msg)
#         print('email envoyé')


# if NbreTfo2 != 1250:
#     fichier = open(f"datarapport.log", "w")
#     fichier.write(f"""{{"date_heure":"{date} {hr}", "zone_poste":"tfo2", "total":"{NbreTfo2}"}}
#     """)
#     fichier.close()

#     with open ('datarapport.log', 'r') as f:
#         data = json.load(f)
#     print(data['total'])

#     msg = EmailMessage()
#     msg.set_content(f"""date_heure : {data['date_heure']}
#     zone_poste : {data['zone_poste']}
#     total : {data['total']}
#     """)
#     msg["Subject"] = "Email de Test"
#     msg["From"] = "coulibalyoumar260@gmail.com"
#     msg["To"] = "segnindenin.coulibaly@uvci.edu.ci"
#     context=ssl.create_default_context()
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#         smtp.login(msg["From"], "zggeyvajuyhiewnm")
#         smtp.send_message(msg)
#         print('email envoyé')