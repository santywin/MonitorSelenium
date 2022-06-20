# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 08:33:29 2022

@author: Santiago
"""
import pandas as pd

import os
from datetime import datetime
import logging

from selenium.webdriver.support.wait import WebDriverWait

import tesCap

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image

from bs4 import BeautifulSoup

import psycopg2, psycopg2.extras
from sqlalchemy import create_engine

from time import sleep



estudiantes = pd.read_csv('C:/Users/Santiago/Documents/GitHub/gacetaces/automotriz1.csv', delimiter=';', dtype=str)


   
    

path_base = 'C:\\Users\\Santiago\\Documents\\GitHub\\gacetaces\\'
log_actual = path_base + 'logs/monitor_%s.log' % datetime.now().strftime('%Y%m%d')
url_base = 'https://www.senescyt.gob.ec/consulta-titulos-web/faces/vista/consulta/consulta.xhtml'




def tableDataText(table):       
    rows = []
    trs = table.find_all('tr')
    headerow = [td.get_text(strip=True) for td in trs[0].find_all('th')] # header row
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append([td.get_text(strip=True) for td in tr.find_all('td')]) # data row
    return rows


def extraerTabla(table):
    list_table = tableDataText(table)
    dftable = pd.DataFrame(list_table[1:], columns=list_table[0])
    dftable.head(4)
    return dftable
        


for index, row in estudiantes.iterrows():
    
    sleep(5)
    
    options = Options()
    options.headless = True
    options.add_argument("--lang=en")
    driver = webdriver.Chrome(path_base + 'chromedriver.exe', options=options)
    driver.set_page_load_timeout(30)  # Tiempo en segundos



    logging.info("--")
    logging.info("Test de Servicios en Línea")
    tiempo_inicio = datetime.now()
    logging.info("Inicio: %s" % tiempo_inicio.strftime('%Y-%m-%d %H:%M:%S'))
    logging.info("")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_actual, 'a+', 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(handler)

    options.add_experimental_option('prefs', {"download.default_directory": path_base,"download.prompt_for_download": False,"download.directory_upgrade": True,"plugins.plugins_disabled": ["Chrome PDF Viewer"]})

    engine = create_engine('postgresql://postgres:admin123@localhost:5432/senescyt');


    
    
    identificacion = str(row.IDENTIFICACION)

    cedula = 0
    mensaje = 0
    
    while cedula == 0:
        
        try:
            sleep(2)
            datos_estudiante = {}
            driver.get(url_base)
            driver.set_window_size(974, 1040)
            driver.find_element(By.ID, "formPrincipal:identificacion").click()
            driver.find_element(By.ID, "formPrincipal:identificacion").send_keys(identificacion)
            driver.save_screenshot(path_base + "captchas/captcha.png")
            img = Image.open(path_base + "captchas/captcha.png")
            area = (154, 467, 272, 496)
            cropped_img = img.crop(area)
            #cropped_img.show()
            cropped_img.save(path_base + "captchas/img_captcha.png")
            path_image = path_base + "captchas/img_captcha.png"
            texto = tesCap.resolver_captcha(path_image)
            print(texto)
            driver.find_element(By.ID, "formPrincipal:captchaSellerInput").click()
            driver.find_element(By.ID, "formPrincipal:captchaSellerInput").send_keys(texto)
            
            
            
            sleep(3)
            
            driver.find_element(By.ID, "formPrincipal:boton-buscar").click()
            
            
            
            sleep(5)
            
            df = pd.DataFrame()
            
            
            
            cedula = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/form/div/span/div[1]/div[2]/div/div/div/div/div[1]/table/tbody/tr[1]/td[2]/label').text
            
        except:
            try:
                mensaje = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/form/div/div[3]')
                if mensaje != 0:
                    cedula = 1
            except:
              print("An exception occurred")
              pass
            print("OS error: {0}")
            pass
            
    
    if cedula != 1:
    
        nombres = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/form/div/span/div[1]/div[2]/div/div/div/div/div[1]/table/tbody/tr[2]/td[2]/label').text
        genero = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/form/div/span/div[1]/div[2]/div/div/div/div/div[1]/table/tbody/tr[3]/td[2]/label').text
        nacionalidad = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/form/div/span/div[1]/div[2]/div/div/div/div/div[1]/table/tbody/tr[4]/td[2]/label').text
        
        df = df.append({'cedula': cedula, 'nombres':nombres, 'genero':genero, 'nacionalidad':nacionalidad}, ignore_index=True)
        
        soup = BeautifulSoup(driver.page_source,'html.parser')

        try:
            
          title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/form/div/span/div[2]/div[1]/h4').text
         
          if title == 'Título(s) de tercer nivel de grado':
            contentGrado = soup.find_all('table')[4]   
            
            dftable_grado = extraerTabla(contentGrado)
            
            dftable_grado['identificacion'] = pd.Series([cedula for x in range(len(dftable_grado.index))]) 
        
            dftable_grado.to_sql('grado', engine,if_exists = 'append', index=False);
            
            df.to_sql('principal', engine,if_exists = 'append', index=False);
            sleep(2)
        
          else:
            contentPosgrado = soup.find_all('table')[4]   
            tableposgrado = extraerTabla(contentPosgrado)
            tableposgrado['identificacion'] = pd.Series([cedula for x in range(len(tableposgrado.index))]) 
        
            tableposgrado.to_sql('posgrado', engine,if_exists = 'append', index=False);
            
            contentGrado = soup.find_all('table')[5]   
            dftable_grado = extraerTabla(contentGrado)
            dftable_grado['identificacion'] = pd.Series([cedula for x in range(len(dftable_grado.index))]) 
        
            dftable_grado.to_sql('grado', engine,if_exists = 'append', index=False);
            
            df.to_sql('principal', engine,if_exists = 'append', index=False);
            sleep(2)
        
        except:
          print("An exception occurred")
          sleep(2)
          pass
      
    driver.quit()

logging.info("")
logging.info("Fin: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
