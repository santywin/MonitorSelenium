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
from fake_useragent import UserAgent





#from dotenv import load_dotenv

#load_dotenv()

paso = 0
alerta = False
path_base = 'C:\\Users\\Santiago\\Documents\\GitHub\\gacetaces\\'
log_actual = path_base + 'logs\\monitor_%s.log' % date.today().strftime('%Y%m%d')

#path_base = '/home/edisson/PycharmProjects/monitor_servicios/'
#log_actual = path_base + 'logs/monitor_%s.log' % datetime.now().strftime('%Y%m%d')


options = Options()
#ua = UserAgent()
#userAgent = ua.random
#print(userAgent)
options.headless = True
options.add_argument("--lang=en")
#options.add_argument(f'user-agent={userAgent}')
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
    
    
    # 1 | open | /sri-en-linea/SriDeclaracionesWeb/ConsultaImpuestoRenta/Consultas/consultaImpuestoRenta | 
    driver.get("https://srienlinea.sri.gob.ec/sri-en-linea/SriDeclaracionesWeb/ConsultaImpuestoRenta/Consultas/consultaImpuestoRenta")
    # 2 | setWindowSize | 1346x708 | 
    driver.set_window_size(1346, 708)
    # 3 | click | id=busquedaRucId | 
    driver.find_element(By.ID, "busquedaRucId").click()
    # 4 | type | id=busquedaRucId | 0104775473
    driver.find_element(By.ID, "busquedaRucId").send_keys("0104775473")
    # 5 | click | css=.cyan-btn > .ui-button-text | 
    driver.find_element(By.CSS_SELECTOR, ".cyan-btn > .ui-button-text").click()
    # 6 | click | linkText=2 | 
    
    soup_level2=BeautifulSoup(driver.page_source, "html.parser")
    
    
    driver.find_element(By.LINK_TEXT, "2").click()
    # 7 | click | css=.col-sm-12 .ui-button-text | 
    driver.find_element(By.CSS_SELECTOR, ".col-sm-12 .ui-button-text").click()
    

    
    #driver.find_element(By.ID, "j_idt43").click()
        # 4 | click | id=mensajeCes | 
    
 
        
    
    soup_level2=BeautifulSoup(driver.page_source, "html.parser")


    driver.save_screenshot(path_base + "imagenes/error" + str(random.randint(10, 200000)) + ".png")


except:

    print("ERROR x = ")
    driver.save_screenshot(path_base + "imagenes/error" + str(random.randint(10, 200000)) + ".png")
    pass
 

logging.info("")
logging.info("Fin: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


driver.quit()




