# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 08:33:29 2022

@author: Santiago
"""

import os
from datetime import datetime
import logging

from selenium.webdriver.support.wait import WebDriverWait

import ocr

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image

paso = 0
alerta = False
path_base = 'C:\\Users\\Santiago\\Documents\\GitHub\\gacetaces\\'
log_actual = path_base + 'logs/monitor_%s.log' % datetime.now().strftime('%Y%m%d')
url_base = 'https://servicios.educacion.gob.ec/titulacion25-web/faces/paginas/consulta-titulos-refrendados.xhtml'


global identificacion


def incrementar_paso():
    global paso
    paso = paso + 1


class Monitor:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_actual, 'a+', 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(handler)

    def __init__(self, identificador=""):
        self.id = identificador
        # options = Options()
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--lang=en")

        options.add_experimental_option('prefs', {
            "download.default_directory": path_base,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.plugins_disabled": ["Chrome PDF Viewer"]
        }
                                               )

        # profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "plugins.always_open_pdf_externally": True,
        #            "download.default_directory": path_base, "download.extensions_to_open": "applications/pdf"}
        # options.add_experimental_option("prefs", profile)
        self.driver = webdriver.Chrome(path_base + 'chromedriver.exe', options=options)
        self.driver.set_page_load_timeout(30)

    def finalizar_monitor(self):
        self.driver.quit()

    def buscar_texto_en_pagina(self, texto):
        try:
            assert texto in self.driver.page_source
        except AssertionError as e:
            e.args += ('No se encontró el texto:', texto)
            raise

    def test_general(self, test_metodo):
        try:
            incrementar_paso()
            test_metodo()
            logging.info(' Paso %02d: %s..BIEN' % (paso, str.ljust(test_metodo.__name__, 30, '.')))
        except Exception as e:
            self.driver.save_screenshot(path_base + "imagenes/error_%s_%02d.png" % (self.id, paso))
            logging.error('Paso %02d: %s..MAL\n\t%s' % (paso, str.ljust(test_metodo.__name__, 30, '.'), repr(e)))

    def test_servicioWebAngie(self):
        datos_estudiante = {}
        self.driver.get(url_base)
        self.driver.set_window_size(974, 1040)
        self.driver.find_element(By.ID, "formBusqueda:cedula").click()
        self.driver.find_element(By.ID, "formBusqueda:cedula").send_keys(identificacion)
        self.driver.save_screenshot(path_base + "captchas/captcha.png")
        img = Image.open(path_base + "captchas/captcha.png")
        area = (428, 566, 548, 595)
        cropped_img = img.crop(area)
        cropped_img.show()
        cropped_img.save(path_base + "captchas/img_captcha.png")
        texto = ocr.resolver_captcha(path_base + "captchas/img_captcha.png")
        print(texto)
        self.driver.find_element(By.ID, "formBusqueda:captcha").send_keys(texto)
        self.driver.find_element(By.ID, "formBusqueda:clBuscar").click()
        cabecera_estudiantes = self.driver.find_elements(By.CLASS_NAME, "rf-dt-shdr-c")
        datos_estudiantes = self.driver.find_elements(By.CLASS_NAME, "rf-dt-c")
        cabecera_estudiantes.reverse()
        datos_estudiantes.reverse()

        for indice in range(0, len(datos_estudiantes)):
            datos_estudiante.__setitem__(cabecera_estudiantes.pop().text, datos_estudiantes.pop().text)
        # self.driver.find_element(By.LINK_TEXT, "Imprimir Certificado").click()
        self.driver.execute_script("mojarra.jsfcljs(document.getElementById('formBusqueda'),{'formBusqueda:j_idt49:0:j_idt75':'formBusqueda:j_idt49:0:j_idt75'},'_self')")

        self.driver.save_screenshot(path_base + "imagenes/pdf.png")

        ##### The file will be downloaded to original download path #####

        # enable_download_in_headless_chrome(self.driver, download_path)
        # Refresh to trigger download behavior again
        # self.driver.refresh()


        print(datos_estudiante)


logging.info("--")
logging.info("Test de Servicios en Línea")
tiempo_inicio = datetime.now()
logging.info("Inicio: %s" % tiempo_inicio.strftime('%Y-%m-%d %H:%M:%S'))
logging.info("")
test = Monitor()
test.__init__(identificador=tiempo_inicio.strftime('%Y%m%d%H%M%S'))

identificacion = '0104775473'

test.test_general(test.test_servicioWebAngie)

test.finalizar_monitor()
logging.info("")
logging.info("Fin: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
