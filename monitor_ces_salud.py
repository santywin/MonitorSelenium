# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 23:08:24 2020

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







#from dotenv import load_dotenv

#load_dotenv()

paso = 0
alerta = False
path_base = 'C:\\Users\\Santiago\\Downloads\\monitor_servicios\\'
log_actual = path_base + 'logs\\monitor_%s.log' % date.today().strftime('%Y%m%d')

#path_base = '/home/edisson/PycharmProjects/monitor_servicios/'
#log_actual = path_base + 'logs/monitor_%s.log' % datetime.now().strftime('%Y%m%d')


def incrementar_paso():
    global paso
    paso = paso + 1


def alertar():
    global alerta
    alerta = True


class Monitor:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_actual, 'a+', 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(handler)
    
    

    def __init__(self, identificador=""):
        self.id = identificador
        options = Options()
        options.headless = True
        options.add_argument("--lang=en")
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver = webdriver.Chrome(path_base + 'chromedriver.exe', options=options)
        self.driver.set_page_load_timeout(30)  # Tiempo en segundos

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
            alertar()
            self.driver.save_screenshot(path_base + "imagenes/error_%s_%02d.png" % (self.id, paso))
            logging.error('Paso %02d: %s..MAL\n\t%s' % (paso, str.ljust(test_metodo.__name__, 30, '.'), repr(e)))


    def test_recuperar_contrasena(self):
        self.driver.get("http://appcmi.ces.gob.ec/oferta_vigente/salud/area_salud.php")
        self.driver.set_window_size(1270, 4800)
        self.driver.switch_to.frame(1)
        self.driver.find_element(By.ID, "Consultar").click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(2)
        self.driver.find_element(By.NAME, "submit").click()
        
        self.driver.find_element(By.CSS_SELECTOR, "td > .btn").click()
        
        dft1 = pd.DataFrame(columns=["Codigo","IES:", "Siglas:", "Código sniese:", "Tipo de financiamiento:", "Sitio web:",  "Tipo de IES:", "Estado del programa:", "Tipo de programa:",  "Campo amplio:",  "Campo específico:",  "Campo detallado:", "Programa:", "Título que otorga:", "Matrícula", "Arancel", "Codificación  del programa:",  "Lugar de ejecución:", "Provincia:",  "Cantón:",  "Ciudad:", "Duración:", "Tipo de periodo académico:",  "Modalidad:", "№ de resolución del CES:",  "Estado actual de aprobación:",  "Fecha de aprobación del CES:",  "Año de aprobación:", "Tiempo de vigencia:", "Finaliza el:", "№ de paralelos:",  "№ de estudiantes por paralelo:",  "№ de horas:", "Requisitos de ingreso:",  "Convenio con otras entidades:", "Objetivo general:",  "Perfil de ingreso:", "Perfil de egreso:", "Modalidad de titulación:"])
        
      #  self.driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
       
        
        for x in range(1, 183):
            
            try:
       
                time.sleep(1)
                print(x)
                
                ubi = x // 100
               # print("ubi es "+str(ubi))
                #☺self.driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
                #self.driver.execute_script("window.scrollTo(0, window.scrollY + "+str(ubi*200)+")")


                self.driver.execute_script("window.scrollTo(0, "+str(ubi*4105)+")")
                #print("ubi por 200 "+str(ubi*200))
                #self.driver.save_screenshot(path_base + "imagenes/error_%s_%02d.png" % (self.id, x))
                
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr:nth-child("+str(x)+") .btn")))

                self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child("+str(x)+") .btn").click()
                #print('titulo es '+ self.driver.title)
                e2 = self.driver.find_elements(By.TAG_NAME, "table")
                soup_level2=BeautifulSoup(self.driver.page_source, 'lxml')
                

                
                table = soup_level2.find_all('table')[0]
                df = pd.read_html(str(table),header=0)
                datalist = []#empty list
                ies = siglas = sniese = financiamiento = web = tipoies =   estado =campoaplio=campoespecifico=campodetallado=programa=titulo=matricula=arancel=codificacion=lugar=provincia=canton=ciudad= duracion=tipoperiodo=modalidad=nroresolucion=estadoactual=fechaprobacion=anioaprobacion=tiempovigencia=finaliza=nroparalelos=nroestudiantesxparalelo=nrohoras=reqingresos=convenios=objetivos=perfilingreso=perfilegreso=modalidadtitulacion = "vacio"
                for tr in table.find_all("tr"):
                    data = [item.get_text(strip=True) for item in tr.find_all(["th","td"])]
                    dato = str(data[0])
                    if dato == "IES:":
                        ies = data[1]
                    elif dato == "Siglas:":
                    	siglas = data[1]
                    elif  dato == "Código sniese:":
                    	sniese = data[1]
                    elif dato == "Tipo de financiamiento:":
                    	financiamiento = data[1]
                    elif dato == "Sitio web:":
                    	web = data[1]
                    elif dato == "Tipo de IES:":
                    	tipoies = data[1]
                    
                #    datalist.append(data[1])
                #dft1.loc[x]=[datalist[0], datalist[1], datalist[2], datalist[3], datalist[4]]
                
                table2 = soup_level2.find_all('table')[1]
                df2 = pd.read_html(str(table),header=0)
                datalist2 = []#empty list
                for tr in table2.find_all("tr"):
                    data = [item.get_text(strip=True) for item in tr.find_all(["th","td"])]
                   # print(data)
                    dato = str(data[1])
                    if dato == "Estado del programa:":
                        estado = data[2]
                    elif dato == "Tipo de programa:":
                    	tipoprograma = data[2]
                    elif  dato == "Campo amplio:":
                    	campoaplio = data[2]
                    elif dato == "Campo específico:":
                    	campoespecifico = data[2]
                    elif dato == "Campo detallado:":
                    	campodetallado = data[2]
                    elif dato == "Programa:":
                    	programa = data[2]
                    elif dato == "Título que otorga:":
                    	titulo = data[2]
                    elif dato == "Matrícula":
                    	matricula = data[2]
                    elif dato == "Arancel":
                    	arancel = data[2]
                    elif dato == "Codificación  del programa:":
                    	codificacion = data[2]
                    elif dato == "Lugar de ejecución:":
                    	lugar = data[2]
                    elif dato == "Provincia:":
                    	provincia = data[2]
                    elif dato == "Cantón:":
                    	canton = data[2]
                    elif dato == "Ciudad:":
                    	ciudad = data[2]
                    elif dato == "Duración:":
                    	duracion = data[2]
                    elif dato == "Tipo de periodo académico:":
                    	tipoperiodo = data[2]
                    elif dato == "Modalidad:":
                    	modalidad = data[2]
                    elif dato == "№ de resolución del CES:":
                    	nroresolucion = data[2]
                    elif dato == "Estado actual de aprobación:":
                    	estadoactual = data[2]
                    elif dato == "Fecha de aprobación del CES:":
                    	fechaprobacion = data[2]
                    elif dato == "Año de aprobación:":
                    	anioaprobacion = data[2]
                    elif dato == "Tiempo de vigencia:":
                    	tiempovigencia = data[2]
                    elif dato == "Finaliza el:":
                    	finaliza = data[2]
                    elif dato == "№ de paralelos:":
                    	nroparalelos = data[2]
                    elif dato == "№ de estudiantes por paralelo:" or dato == "№ de estudiantes por cohorte:":
                    	nroestudiantesxparalelo = data[2]
                    elif dato == "№ de horas:":
                    	nrohoras = data[2]
                    elif dato == "Requisitos de ingreso:":
                    	reqingresos = data[2]
                    elif dato == "Convenio con otras entidades:":
                    	convenios = data[2]
                    elif dato == "Objetivo general:":
                    	objetivos = data[2]
                    elif dato == "Perfil de ingreso:":
                    	perfilingreso = data[2]
                    elif dato == "Perfil de egreso:":
                    	perfilegreso = data[2]
                    elif dato == "Modalidad de titulación:":
                    	modalidadtitulacion = data[2]

                   
                    datalist2.append(data[2])
                
                time.sleep(1)
                self.driver.find_element(By.CSS_SELECTOR, "td > .btn").click()
                
                dft1.loc[x]=[x,ies,siglas,sniese,financiamiento,web,tipoies,estado, tipoprograma,campoaplio, campoespecifico, campodetallado,programa,titulo,  matricula, arancel, codificacion, lugar,provincia,  canton,  ciudad,duracion,tipoperiodo,modalidad, nroresolucion,estadoactual,fechaprobacion,anioaprobacion, tiempovigencia,finaliza, nroparalelos, nroestudiantesxparalelo,nrohoras,reqingresos,convenios,  objetivos,perfilingreso,perfilegreso,modalidadtitulacion]
                
                
                
                #print(dft1)
                #print(e2[0].text)
                  
                #print(df)
                #print(e2[1].text)

            
            except:
              print("Unexpected error:", sys.exc_info()[0])
              print("ERROR x = " + str(x))
              self.driver.save_screenshot(path_base + "imagenes/error_%s_%02d.png" % (self.id, x))
              pass
         
            

        
        print(dft1)
        
        dft1.to_excel(r'C:\Users\Santiago\Downloads\monitor_servicios\export_dataframe.xls', index = False, header=True)
      #  self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) .btn").click()
      #  self.driver.find_element(By.CSS_SELECTOR, "td > .btn").click()
        
      #  self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(4) .btn").click()
        
       
        
       # print(self.driver.page_source)
       # self.driver.find_element(By.CSS_SELECTOR, "td > .btn").click()


logging.info("--")
logging.info("Test de Servicios en Línea")
tiempo_inicio = datetime.now()
logging.info("Inicio: %s" % tiempo_inicio.strftime('%Y-%m-%d %H:%M:%S'))
logging.info("")

test = Monitor()

test.__init__(identificador=tiempo_inicio.strftime('%Y%m%d%H%M%S'))

#test.test_general(test.test_recuperar_contrasena)
test.test_recuperar_contrasena()


test.finalizar_monitor()
logging.info("")
logging.info("Fin: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


