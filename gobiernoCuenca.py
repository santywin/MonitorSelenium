# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 08:35:06 2022

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

import downEmpleados

empleados = downEmpleados.download()


path_base = 'C:\\Users\\Santiago\\Documents\\GitHub\\gacetaces\\'
log_actual = path_base + 'logs/monitor_%s.log' % datetime.now().strftime('%Y%m%d')
url_base = 'https://enlinea.cuenca.gob.ec/#/informe-predial'




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
        


for index, row in empleados.iterrows():
    
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


    
    # identificacion = '0104775473'
    identificacion = str(row.document)

    cedula = 0
    mensaje = 0
    
       
    try:
        sleep(2)
        datos_estudiante = {}
        driver.get(url_base)
        driver.set_window_size(974, 1040)
        # driver.save_screenshot(path_base + "imagenes/pdf.png")

        driver.find_element(By.ID, "txtClaveCatastral").click()
        driver.find_element(By.ID, "txtClaveCatastral").send_keys(identificacion)
        
        # driver.save_screenshot(path_base + "imagenes/pdf.png")
        
        # driver.save_screenshot(path_base + "captchas/captcha.png")
        # img = Image.open(path_base + "captchas/captcha.png")
        # area = (154, 467, 272, 496)
        # cropped_img = img.crop(area)
        #cropped_img.show()
        # cropped_img.save(path_base + "captchas/img_captcha.png")
        # path_image = path_base + "captchas/img_captcha.png"
        # texto = tesCap.resolver_captcha(path_image)
        # print(texto)
        
        # nombres = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/form/div/span/div[1]/div[2]/div/div/div/div/div[1]/table/tbody/tr[2]/td[2]/label').text

        sleep(2)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div/div/div[3]/div[3]/button').click()
        # driver.save_screenshot(path_base + "imagenes/pdf.png")
        sleep(5)

        nombres = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[1]/div/div[1]/div[2]/p/span[2]').text
        
        print(nombres)
        
        nropredios = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[1]/div/div[1]/div[3]/p/span[2]').text
        
        print(nropredios)
        
        cedula = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[1]/div/div[1]/div[1]/p/span[2]').text
        
        print(cedula)
        
        soup = BeautifulSoup(driver.page_source,'html.parser')

        
        predios = soup.find_all('table')[0]   
        
        dftable_predios = extraerTabla(predios)
        
        dftable_predios['identificacion'] = pd.Series([cedula for x in range(len(dftable_predios.index))]) 

        dfPrincipal = pd.DataFrame()
        
        dfPrincipal = dfPrincipal.append({'cedula': cedula, 'nombres':nombres, 'nropredios':nropredios}, ignore_index=True)

        
        
        # driver.find_element(By.ID, "formPrincipal:captchaSellerInput").send_keys(texto)
        
        
        
        # sleep(3)
        
        # driver.find_element(By.ID, "formPrincipal:boton-buscar").click()
        
        
        
        sleep(2)
        
        # df = pd.DataFrame()
        
        
        
        # cedula = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/main/form/div/span/div[1]/div[2]/div/div/div/div/div[1]/table/tbody/tr[1]/td[2]/label').text
        
    except:
        print("OS error: {0}")
        driver.save_screenshot(path_base + "imagenes/pdf"+str(index)+".png")

        pass

    driver.quit()

logging.info("")
logging.info("Fin: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
