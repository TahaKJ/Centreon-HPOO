# -*- coding: utf-8 -*-
import sys, requests, time
import json, os

user = 'username'
password ='password'

# le temps à partir du quel on recupère les stats
time = (time.time()-86400)*1000   # 24h avant *1000
time = round(time)
# RHEL
deployRhelflow ='id'  # id du flow deployRhelver
udateRhelflow ='id'  # id du flow  updateRhelacher
# AD
AjoutAD ='id'  # id du flow AjoutADver
suppressionAD ='id'  # id du flow  supprADacher
# Landesk
deployLanDeskflow ='id'  # id du flow deployLanver
udateLanDeskflow ='id'  # id du flow  undeployLanacher
# ADREZO
ReservIP ='id'  # id du flow reserver
RelachIP ='id'  # id du flow  relacher

# choix de la brique  AD:1 Landesk:2 Rhel:3 Adrezo:4
switcher = 4;

# url hp oo
url = 'hpOOurl.com:Port/oo/rest/executions/statistics?top=100&endedAfter='+str(time)
APIhp = requests.get(url , auth=(user, password))

if (APIhp.status_code!=200):
    print("UKNOWN: problème connexion HPOO", APIhp.status_code)
    sys.exit(3)

# recupération JSON
jsonfile = APIhp.text
# convertion de JSON en DICT python
python_obj = json.loads(jsonfile)

def Adrezo():
    reser = 10
    rel = 10
    for i in range(len(python_obj)):
        if (python_obj[i].get('flowUuid')==ReservIP):
            nbExec = python_obj[i].get('numberOfExecutions')
            result = python_obj[i].get('resultsDistribution')
            nbRes = result[0].get('amount')
            typeErr = result[0].get('type')
            if typeErr =='RESOLVED' and nbExec-nbRes==0:
                reser = 0
            if nbExec-nbRes!=0 :
                reser = 1
            if typeErr =='ERROR' and nbExec-nbRes==0:
                reser = 2
        if (python_obj[i].get('flowUuid')==RelachIP):
                nbExec = python_obj[i].get('numberOfExecutions')
                result = python_obj[i].get('resultsDistribution')
                nbRes = result[0].get('amount')
                typeErr = result[0].get('type')
                if typeErr =='RESOLVED' and nbExec-nbRes==0:
                    rel = 0
                if nbExec-nbRes!=0 :
                    rel = 1
                if typeErr =='ERROR' and nbExec-nbRes==0:
                    rel = 2
                    

    if reser==10 and rel==10:
                print ("OK: pas de demande AD")
                sys.exit(0)
    if reser==0 and rel==0:
                print ("OK: execution avec succes")
                sys.exit(0)
    if (reser==1 or reser==10)  and rel==0:
                print ("WARNING: ReservationIP execution incorrect")
                sys.exit(1)
    if reser==0 and (rel==1 or rel==10):
                print ("WARNING: RelacherIP execution incorrect")
                sys.exit(1)
    if reser==1 and rel==1:
                print ("WARNING: Adrezo execution incorrect")
                sys.exit(1)
    if reser==2 or rel==2:
                print ("CRITICAL: Adrezo ne marche plus")
                sys.exit(2)                

def AD():
    AjouAD = 10
    supprAD = 10
    for i in range(len(python_obj)):
        if (python_obj[i].get('flowUuid')==AjoutAD):
            nbExec = python_obj[i].get('numberOfExecutions')
            result = python_obj[i].get('resultsDistribution')
            nbRes = result[0].get('amount')
            typeErr = result[0].get('type')
            if typeErr =='RESOLVED' and nbExec-nbRes==0:
                AjouAD = 0
            if nbExec-nbRes!=0 :
                AjouAD = 1
            if typeErr =='ERROR' and nbExec-nbRes==0:
                AjouAD = 2
        if (python_obj[i].get('flowUuid')==suppressionAD):
                nbExec = python_obj[i].get('numberOfExecutions')
                result = python_obj[i].get('resultsDistribution')
                nbRes = result[0].get('amount')
                typeErr = result[0].get('type')
                if typeErr =='RESOLVED' and nbExec-nbRes==0:
                    supprAD = 0
                if nbExec-nbRes!=0:
                    supprAD = 1
                if typeErr =='ERROR' and nbExec-nbRes==0:
                    supprAD = 2
    print(AjouAD, supprAD)
    if AjouAD==10 and supprAD==10:
                print ("OK: pas de demande AD")
                sys.exit(0)
    if AjouAD==0 and supprAD==0:
            print ("OK: execution avec succes")
            sys.exit(0)
    if (AjouAD==1 or AjouAD==10) and supprAD==0:
            print ("WARNING: Ajout AD echec execution")
            sys.exit(1)
    if AjouAD==0 and (supprAD==1 or supprAD==10):
            print ("WARNING: Suppression AD echec execution")
            sys.exit(1)
    if AjouAD==1 and supprAD==1:
            print ("WARNING:  Ajout et Suppression AD echec execution")
            sys.exit(1)
    if AjouAD==2 or supprAD==2:
            print ("CRITICAL: AD ne marche pas proprement")
            sys.exit(2)            
def RHEL ():
    deployRhel=10
    updateRhel=10
    
    for i in range(len(python_obj)):
        if (python_obj[i].get('flowUuid')==deployRhelflow):
            nbExec = python_obj[i].get('numberOfExecutions')
            result = python_obj[i].get('resultsDistribution')
            nbRes = result[0].get('amount')
            typeErr = result[0].get('type')
            if typeErr =='RESOLVED' and nbExec-nbRes==0:
                deployRhel = 0
            if nbExec-nbRes!=0 :
                deployRhel = 1
            if typeErr =='ERROR' and nbExec-nbRes==0:
                deployRhel = 2
        if (python_obj[i].get('flowUuid')==udateRhelflow):
                nbExec = python_obj[i].get('numberOfExecutions')
                result = python_obj[i].get('resultsDistribution')
                nbRes = result[0].get('amount')
                typeErr = result[0].get('type')
                if typeErr =='RESOLVED' and nbExec-nbRes==0:
                    updateRhel = 0
                if nbExec-nbRes!=0:
                    updateRhel = 1
                if typeErr =='ERROR' and nbExec-nbRes==0:
                    updateRhel = 2
    if deployRhel==10 and updateRhel==10:
                print ("OK: pas de demande rhel")
                sys.exit(0)
    if deployRhel==0 and updateRhel==0:
                print ("OK: execution avec succes")
                sys.exit(0)
    if (deployRhel==1 or deployRhel==10) and updateRhel==0 :
                print ("WARNING: deploy RHEL echec execution")
                sys.exit(1)
    if deployRhel==0 and (updateRhel==1 or updateRhel==10):
                print ("WARNING: Update RHEL echec execution")
                sys.exit(1)
    if deployRhel==1 and updateRhel==1:
                print ("WARNING: RHEL echec execution")
                sys.exit(1)
    if deployRhel==2 or updateRhel==2:
                print ("CRITICAL: RHEL ne marche pas proprement")
                sys.exit(2)
                
def landesk ():
    deployLan = 10
    undeployLan = 10
    for i in range(len(python_obj)):
        if (python_obj[i].get('flowUuid')==deployLanDeskflow):
            print(python_obj[i].get('flowUuid')==deployLanDeskflow)
            nbExec = python_obj[i].get('numberOfExecutions')
            result = python_obj[i].get('resultsDistribution')
            nbRes = result[0].get('amount')
            typeErr = result[0].get('type')
            if typeErr =='RESOLVED' and nbExec-nbRes==0:
                deployLan = 0
            if nbExec-nbRes!=0 :
                deployLan = 1
            if typeErr =='ERROR' and nbExec-nbRes==0:
                deployLan = 2
        if (python_obj[i].get('flowUuid')==udateLanDeskflow):
                nbExec = python_obj[i].get('numberOfExecutions')
                result = python_obj[i].get('resultsDistribution')
                nbRes = result[0].get('amount')
                typeErr = result[0].get('type')
                if typeErr =='RESOLVED' and nbExec-nbRes==0:
                    undeployLan = 0
                if nbExec-nbRes!=0:
                    undeployLan = 1
                if typeErr =='ERROR' and nbExec-nbRes==0:
                    undeployLan = 2
    
    if deployLan==10 and undeployLan==10:
            print ("OK: pas de demande landesk")
            sys.exit(0)
    if deployLan==0 and undeployLan==0:
            print ("OK: execution avec succes")
            sys.exit(0)
    if (deployLan==1 or deployLan==10)  and undeployLan==0:
            print ("WARNING: install LanDesk echec execution")
            sys.exit(1)
    if deployLan==0 and (undeployLan==1 or undeployLan==10) :
            print ("WARNING: suppr LanDesk echec execution")
            sys.exit(1)
    if deployLan==1 and undeployLan==1:
            print ("WARNING: LanDesk echec execution")
            sys.exit(1)
    if deployLan==2 or undeployLan==2:
            print ("CRITICAL: LanDesk ne marche pas proprement")
            sys.exit(2)

if (len(python_obj)!=0):
    if switcher ==1:
            AD()
    if switcher ==2:
            landesk()
    if switcher ==3:
            RHEL()
    if switcher ==4:
            Adrezo()
else:
    print ("OK: Pas de demandes")
    os.system("pause")
    sys.exit(0)
