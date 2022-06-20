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



try:
    driver.get("http://gaceta.ces.gob.ec/inicio.html")
        # 2 | setWindowSize | 1346x708 | 
    driver.set_window_size(1346, 708)
        # 3 | click | id=j_idt43 | 
    
    #driver.find_element(By.ID, "j_idt43").click()
        # 4 | click | id=mensajeCes | 
    
    
    dft1 = pd.DataFrame(columns=["numero","fecha","resolucion"])
        
    
    soup_level2=BeautifulSoup(driver.page_source, "html.parser")

    
    
    
    try:
      WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'j_idt43')))
      button = driver.find_element_by_id('j_idt43')
      driver.execute_script("arguments[0].click();", button)
    except TimeoutException:
      print('la pagina tardo demasiado en cargar')
      pass
    
    
    
    
        # 5 | click | id=linkBusquedaSimple | 
    
       # 4 | click | id=inTipDoc_label | 
    try:
      WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'mensajeCes')))
      button = driver.find_element_by_id('mensajeCes')
      driver.execute_script("arguments[0].click();", button)
    except TimeoutException:
      print('la pagina tardo demasiado en cargar')
      pass
    
    
    try:
        element = WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.ID, "inTipDoc_label")))
        # 4 | click | id=inTipDoc_label | 
        driver.find_element(By.ID, "inTipDoc_label").click()
        # 5 | click | css=#inTipDoc_11 > td | 
        driver.find_element(By.CSS_SELECTOR, "#inTipDoc_11 > td").click()
        # 6 | click | css=.marcoPanel | 
        driver.find_element(By.CSS_SELECTOR, ".marcoPanel").click()

    except TimeoutException:
      print('la pagina tardo demasiado en cargar')
        # 5 | click | css=#inTipDoc_11 > td | 
    
    #Abrir modal
    
    try:
      element = WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.ID, "linkBusquedaAVA")))
      boton_buscar = driver.find_element_by_id("linkBusquedaAVA")
      boton_buscar.click()
    except TimeoutException:
      print('la pagina tardo demasiado en cargar')
    
    
        # 6 | click | id=tablaResultados:0:j_idt129 | 
    
    try:
      element = WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.CLASS_NAME, "ui-datatable-tablewrapper")))
    except TimeoutException:
      print('la pagina tardo demasiado en cargar')
    
    e2 = driver.find_elements(By.TAG_NAME, "table")
    soup_level2=BeautifulSoup(driver.page_source, 'lxml')
    table = soup_level2.find_all('table')[3]
    
    
    for child in table.children:
        td1=td2=td3 = ""
        for td in child:
            try:
                td1=td.contents[0].get_text()
                td2=td.contents[1].get_text()
                td3 = (td.find("td",{"class":"ui-column-p-3"})).get_text()
                dft1=dft1.append({'numero' : td1 , 'fecha' : td2, 'resolucion' : td3} , ignore_index=True)
            except:
              
              pass
                
    #print(table)
    
    #time.sleep(10)
    
        # 7 | click | id=j_idt177 | 
            
    for x in range(250):
        print(x)
        try:
          WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tablaResultados_paginator_bottom"]/a[3]')))
          boton_siguiente = driver.find_element_by_xpath('//*[@id="tablaResultados_paginator_bottom"]/a[3]')
          driver.execute_script("arguments[0].click();", boton_siguiente)
        #webdriver.ActionChains(driver).move_to_element(boton_siguiente).click(boton_siguiente).perform()
        except TimeoutException:
          print('la pagina tardo demasiado en cargar')
        
        e2 = driver.find_elements(By.TAG_NAME, "table")
        soup_level2=BeautifulSoup(driver.page_source, 'lxml')
        table = soup_level2.find_all('table')[3]
        

        
        for child in table.children:
            td1=td2=td3 = ""
            for td in child:
                try:
                    td1=td.contents[0].get_text()
                    td2=td.contents[1].get_text()
                    td3 = (td.find("td",{"class":"ui-column-p-3"})).get_text()
                    dft1=dft1.append({'numero' : td1 , 'fecha' : td2, 'resolucion' : td3} , ignore_index=True)
                except:
                  
                  pass
                
            
    dft1.to_excel(r'C:\Users\Santiago\Documents\GitHub\gacetaces\export_dataframe_all.xls', index = False, header=True)
            
    
except:

    print("ERROR x = ")
    driver.save_screenshot(path_base + "imagenes/error" + str(random.randint(10, 200000)) + ".png")
    pass
 

logging.info("")
logging.info("Fin: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


driver.quit()




