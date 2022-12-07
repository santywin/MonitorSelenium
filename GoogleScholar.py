# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 09:30:03 2022

@author: Santiago
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 09:00:36 2022

@author: Santiago
"""
import os
import numpy as np
import pandas as pd
from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from file_read_backwards import FileReadBackwards
from webdriver_manager.chrome import ChromeDriverManager
import alerta_correo
import teams_notificaciones
from datetime import date
from datetime import datetime
from IPython.display import display_html
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.common.exceptions import TimeoutException






#from dotenv import load_dotenv

#load_dotenv()

paso = 0
alerta = False
path_base = 'C:\\Users\\Santiago\\Documents\\GitHub\\gacetaces\\'
log_actual = path_base + 'logs\\monitor_%s.log' % date.today().strftime('%Y%m%d')

#path_base = '/home/edisson/PycharmProjects/monitor_servicios/'
#log_actual = path_base + 'logs/monitor_%s.log' % datetime.now().strftime('%Y%m%d')


options = Options()
options.headless = True
options.add_argument("--lang=en")
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver = webdriver.Chrome(path_base + 'chromedriver.exe', options=options)
driver.set_page_load_timeout(30)  # Tiempo en segundos

logging.info("--")
logging.info("Test de Servicios en Línea")
tiempo_inicio = datetime.now()
logging.info("Inicio: %s" % tiempo_inicio.strftime('%Y-%m-%d %H:%M:%S'))
logging.info("")


def alertar():
    global alerta
    alerta = True

   
dfcompleto = pd.DataFrame()
dfscholarcompleto = pd.DataFrame()


lists = [
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&btnG=", 
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=njkzADn8__8J&astart=10", 
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=17xdALf9__8J&astart=20", 
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=28wgAGj-__8J&astart=30",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=qBErAM3-__8J&astart=40",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=Jq8pAA7___8J&astart=50",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=z8cOADj___8J&astart=60",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=tb8qAE____8J&astart=70",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=5yOcAFz___8J&astart=80",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=kMQpAHL___8J&astart=90",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=_OtdAHz___8J&astart=100",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=cY2IAIj___8J&astart=110",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=uJQyAJT___8J&astart=120",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=2vUoAJ3___8J&astart=130",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=2M6KAKT___8J&astart=140",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=w28rAK7___8J&astart=150",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=prCaALL___8J&astart=160",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=ghdGALf___8J&astart=170",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=SuuAALr___8J&astart=180",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=Zk9mAL____8J&astart=190",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=6AwKAcP___8J&astart=200",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=3P8cAcf___8J&astart=210",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=IfGJAM3___8J&astart=220",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=mV4cAND___8J&astart=230",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=_1eRANP___8J&astart=240",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=5g9vANj___8J&astart=250",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=mBvPANv___8J&astart=260",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=LwEMAdz___8J&astart=270",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=RuoOAd____8J&astart=280",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=lp8jAOP___8J&astart=290",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=mEDPAOT___8J&astart=300",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=2hRvAOb___8J&astart=310",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=p2jmAOf___8J&astart=320",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=VTotAOn___8J&astart=330",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=AdTBAOr___8J&astart=340",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=wGIpAOz___8J&astart=350",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=VakVAez___8J&astart=360",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=BQUmAO7___8J&astart=370",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=jNAyAe7___8J&astart=380",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=pqrSAPD___8J&astart=390",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=heWIAPH___8J&astart=400",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=g6ObAPL___8J&astart=410",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=wC-HAPP___8J&astart=420",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=th-4APT___8J&astart=430",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=Ri6XAPX___8J&astart=440",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=GAhGAPb___8J&astart=450",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=eXkSAfb___8J&astart=460",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=xxu-APf___8J&astart=470",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=O5I8Aff___8J&astart=480",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=2t6SAPj___8J&astart=490",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=m_ljAfj___8J&astart=500",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=m7BGAPn___8J&astart=510",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=Oz1vAPn___8J&astart=520",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=YYOuAPn___8J&astart=530",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=33LxAPn___8J&astart=540",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=FONIAfn___8J&astart=550",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=QuiAAPr___8J&astart=560",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=UgTaAPr___8J&astart=570",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=TrorAPv___8J&astart=580",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=B2ygAPv___8J&astart=590",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=2ornAPv___8J&astart=600",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=LVkTAfv___8J&astart=610",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=YE8rAPz___8J&astart=620",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=VLBfAPz___8J&astart=630",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=9KmHAPz___8J&astart=640",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=9CaZAPz___8J&astart=650",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=YSXMAPz___8J&astart=660",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=AscPAfz___8J&astart=670",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=BUlBAfz___8J&astart=680",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=Ry5kAfz___8J&astart=690",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=eZIoAP3___8J&astart=700",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=w_cqAP3___8J&astart=710",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=QjotAP3___8J&astart=720",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=E1xcAP3___8J&astart=730",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=h-FkAP3___8J&astart=740",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=Ri5vAP3___8J&astart=750",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=OzCHAP3___8J&astart=760",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=K-GJAP3___8J&astart=770",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=gPGJAP3___8J&astart=780",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=avCTAP3___8J&astart=790",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=E0e2AP3___8J&astart=800",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=IKHBAP3___8J&astart=810",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=c0XLAP3___8J&astart=820",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=9TrYAP3___8J&astart=830",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=9v7gAP3___8J&astart=840",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=zIrnAP3___8J&astart=850",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=oMzuAP3___8J&astart=860",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=azX3AP3___8J&astart=870",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=I-oCAf3___8J&astart=880",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=VyYOAf3___8J&astart=890",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=ao8RAf3___8J&astart=900",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=UfkmAf3___8J&astart=910",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=OLIvAf3___8J&astart=920",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=vJU8Af3___8J&astart=930",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=G0lBAf3___8J&astart=940",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=gTlIAf3___8J&astart=950",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=GWJdAf3___8J&astart=960",
         "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=ups.edu.ec&after_author=FQpkAf3___8J&astart=970"
         
         ]

for link in lists: 

    df = pd.DataFrame()
    allNames = []
    allCitas = []
    allinstitutions = []
    alllinks = []
    dfscholar = pd.DataFrame()
    
    
    try:
        
        time.sleep(2)
        driver.get(link)
    
        driver.set_window_size(1346, 708)
        
        sections = driver.find_elements_by_css_selector('div.gsc_1usr')
    
        print(df)
        # iterate over each one
        for section in sections:
            names = section.find_elements_by_css_selector('h3.gs_ai_name')
            citas = section.find_elements_by_css_selector('div.gs_ai_cby')
            institutions = section.find_elements_by_css_selector('div.gs_ai_aff')
            links = section.find_elements_by_css_selector("a.gs_ai_pho")
           
            for name in names:
                allNames.append(name.text)
            
            for cita in citas:
                allCitas.append(cita.text)
                
            for institution in institutions:
                allinstitutions.append(institution.text)
            
            for link in links:
                alllinks.append(link.get_attribute("href") )        
    
        df['name'] = allNames
        df['cita'] = allCitas
        df['institution'] = allinstitutions
        df['link'] = alllinks
                 
        print(df)
        
        for index, row in df.iterrows():
            try:
                time.sleep(2)
                driver.get(row['link'])
                
                driver.set_window_size(1346, 708)
                html = driver.page_source
    
                soup = BeautifulSoup(html, 'lxml')
    
                name = soup.select_one('#gsc_prf_in').text
    
                cititations_all = soup.select_one('tr:nth-child(1) .gsc_rsb_sc1+ .gsc_rsb_std').text
                cititations_since_2016 = soup.select_one('tr:nth-child(1) .gsc_rsb_std+ .gsc_rsb_std').text
    
                h_index_all = soup.select_one('tr:nth-child(2) .gsc_rsb_sc1+ .gsc_rsb_std').text
                h_index_since_2016 = soup.select_one('tr:nth-child(2) .gsc_rsb_std+ .gsc_rsb_std').text
    
                i_10_index_all = soup.select_one('tr~ tr+ tr .gsc_rsb_sc1+ .gsc_rsb_std').text
                i_10_index_since_2016 = soup.select_one('tr~ tr+ tr .gsc_rsb_std+ .gsc_rsb_std').text
    
                data = {
                    "Name": [name],
                    "Citations": cititations_all,
                    "Citations Since 2016": cititations_since_2016,
                    "h-index": h_index_all,
                    "h-index Since 2016": h_index_since_2016,
                    "i10-index": i_10_index_all,
                    "i10-index Since 2016": i_10_index_since_2016,
                    "link": row['link']
                }
    
                dfscholar = pd.DataFrame(data)
    
                print(dfscholar)
                
                dfscholarcompleto = dfscholarcompleto.append(dfscholar, ignore_index = True)

            except Exception:
                pass
                
    except:
    
        print("ERROR x = ")
        driver.save_screenshot(path_base + "imagenes/error" + str(random.randint(10, 200000)) + ".png")
        pass
    
    dfcompleto = dfcompleto.append(df, ignore_index = True)
    

dfcompleto.to_excel(r'C:\Users\Santiago\Documents\GitHub\MonitorSelenium\export_schollar.xls', index = False, header=True)
dfscholarcompleto.to_excel(r'C:\Users\Santiago\Documents\GitHub\MonitorSelenium\export_schollar_citas.xls', index = False, header=True)

 

logging.info("")
logging.info("Fin: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


driver.quit()




