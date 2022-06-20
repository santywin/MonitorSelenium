# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 08:24:32 2022

@author: Santiago
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 08:33:29 2022

@author: Santiago
"""

import os
from datetime import datetime
import logging

from selenium.webdriver.support.wait import WebDriverWait

import tesCap

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image


paso = 0
alerta = False
path_base = 'C:\\Users\\Santiago\\Documents\\GitHub\\gacetaces\\'
log_actual = path_base + 'logs/monitor_%s.log' % datetime.now().strftime('%Y%m%d')
url_base = 'https://servicios.educacion.gob.ec/titulacion25-web/faces/paginas/consulta-titulos-refrendados.xhtml'



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

identificacion = '0104775473'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_actual, 'a+', 'utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger.addHandler(handler)



options.add_experimental_option('prefs', {"download.default_directory": path_base,"download.prompt_for_download": False,"download.directory_upgrade": True,"plugins.plugins_disabled": ["Chrome PDF Viewer"]})



datos_estudiante = {}
driver.get(url_base)
driver.set_window_size(974, 1040)
driver.find_element(By.ID, "formBusqueda:cedula").click()
driver.find_element(By.ID, "formBusqueda:cedula").send_keys(identificacion)
driver.save_screenshot(path_base + "captchas/captcha.png")
img = Image.open(path_base + "captchas/captcha.png")
area = (428, 571, 548, 600)
cropped_img = img.crop(area)
cropped_img.show()
cropped_img.save(path_base + "captchas/img_captcha.png")
path_image = path_base + "captchas/img_captcha.png"
texto = tesCap.resolver_captcha(path_image)
print(texto)
driver.find_element(By.ID, "formBusqueda:captcha").send_keys(texto)
driver.find_element(By.ID, "formBusqueda:clBuscar").click()


cabecera_estudiantes = driver.find_elements(By.CLASS_NAME, "rf-dt-shdr-c")
datos_estudiantes = driver.find_elements(By.CLASS_NAME, "rf-dt-c")
cabecera_estudiantes.reverse()
datos_estudiantes.reverse()
   

for indice in range(0, len(datos_estudiantes)):
    datos_estudiante.__setitem__(cabecera_estudiantes.pop().text, datos_estudiantes.pop().text)


# self.driver.find_element(By.LINK_TEXT, "Imprimir Certificado").click()
driver.execute_script("mojarra.jsfcljs(document.getElementById('formBusqueda'),{'formBusqueda:j_idt49:0:j_idt75':'formBusqueda:j_idt49:0:j_idt75'},'_self')")
   
driver.save_screenshot(path_base + "imagenes/pdf.png")
   
##### The file will be downloaded to original download path #####
   
# enable_download_in_headless_chrome(self.driver, download_path)
# Refresh to trigger download behavior again
# self.driver.refresh()


print(datos_estudiante)


for indice in range(0, len(datos_estudiantes)):
    datos_estudiante.__setitem__(cabecera_estudiantes.pop().text, datos_estudiantes.pop().text)



# driver.find_element(By.LINK_TEXT, "Imprimir Certificado").click()
#driver.execute_script("mojarra.jsfcljs(document.getElementById('formBusqueda'),{'formBusqueda:j_idt49:0:j_idt75':'formBusqueda:j_idt49:0:j_idt75'},'_')")

driver.save_screenshot(path_base + "imagenes/pdf.png")


print(datos_estudiante)


driver.quit()






logging.info("")
logging.info("Fin: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
