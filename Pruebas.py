# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 14:31:43 2021

@author: Santiago
"""
import os
import pandas as pd
from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from file_read_backwards import FileReadBackwards
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import alerta_correo
import teams_notificaciones
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup

paso = 0
alerta = False
path_base = 'C:\\Users\\Santiago\\Downloads\\monitor_servicios\\'
log_actual = path_base + 'logs/monitor_%s.log' % datetime.now().strftime('%Y%m%d')






logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_actual, 'a+', 'utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger.addHandler(handler)
        
        

options = Options()
options.headless = True
options.add_argument("--lang=en")
driver = webdriver.Chrome(path_base + 'chromedriver', options=options)
# self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.set_page_load_timeout(30)  # Tiempo en segundos
        
        
dft1 = pd.DataFrame(columns=["x","codigo","regimen", "nivel", "tipo", "cine", 
                                     "amplio",  "especifico", "detallado", 
                                     "estado",  "sede",  "region",
                                     "provincia", "ciudad", "zona", 
                                     "tothora", "hordoc", "horpra", 
                                     "horaut", "hortit",  "instituto",
                                     "titulo","fecing","fecapr","fecreg","fecfin",
                                     "feciniacre","fecfinacre",
                                     "paralelo","nroest","nrocohorte"
                                     ])
        
        #6570
for x in range(1, 5):
    
    try:
        timeout = 10000;
        
        
        time.sleep(1000)
        
        driver.get("https://infoeducacionsuperior.gob.ec/#/oferta-academica/cursos/" + str(x))
 
        
 
        timeout = 2;
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'enlace-volver'))
        WebDriverWait(driver, timeout).until(element_present)
    
        driver.set_window_size(1270, 4800)
        
    

        html = driver.page_source
        
        #print(self.driver.find_element_by_xpath("/html/body/div/main/div/div/div/div[2]/div[1]/fieldset/div[6]/div/label"))
        
        res = BeautifulSoup(html, 'html.parser')
        
        codigo = 0
        codigos = (res.find("div",{"data-form-static":"curso.codigo"}).select("p"))
        for cod in codigos:
            codigo=cod.get_text()
            print(codigo)
        
        
        regimen = 0
        regimens = (res.find("div",{"data-form-static":"curso.regimenAcademico.nombre"}).select("p"))
        for cod in regimens:
            regimen=cod.get_text()
            print(regimen)
        
        
        nivel = 0
        nivels = (res.find("div",{"data-form-static":"curso.informacionGeneral.duracion.valorReferencialPrograma.nivelFormacion.nombre"}).select("p"))
        for cod in nivels:
            nivel=cod.get_text()
            print(nivel)
        
        
        tipo = 0
        tipos = (res.find("div",{"data-form-static":"curso.informacionGeneral.duracion.valorReferencialPrograma.nivelFormacion.nombre"}).select("p"))
        for cod in tipos:
            tipo=cod.get_text()
            print(tipo)
        
        
        cine = 0
        cines = (res.find("div",{"data-form-static":"regimenAcademico.cineClasificacion.nombre"}).select("p"))
        for cod in cines:
            cine=cod.get_text()
            print(cine)
            
        
        amplio = 0
        amplios = (res.find("div",{"data-form-static":"curso.informacionGeneral.cursoAcademico.campoDetallado.campoEspecifico.campoAmplio.nombre"}).select("p"))
        for cod in amplios:
            amplio=cod.get_text()
            print(amplio)
            
        
        especifico = 0
        especificos = (res.find("div",{"data-form-static":"curso.informacionGeneral.cursoAcademico.campoDetallado.campoEspecifico.nombre"}).select("p"))
        for cod in especificos:
            especifico=cod.get_text()
            print(especifico)
            
        
        detallado = 0
        detallados = (res.find("div",{"data-form-static":"curso.informacionGeneral.cursoAcademico.campoDetallado.nombre"}).select("p"))
        for cod in detallados:
            detallado=cod.get_text()
            print(detallado)
        
        
        estado = 0
        estados = (res.find("div",{"data-form-static":"curso.informacionGeneral.estadoVigencia.nombre"}).select("p"))
        for cod in estados:
            estado=cod.get_text()
            print(estado)
        
        
        sede = 0;
        region = 0;
        provincia =0;
        ciudad = 0;
        zona = 0;

        lugar = 0
        lugars = (res.find("tr",{"data-ng-repeat":"lugar in curso.lugaresInstruccion"}).select("td"))
        

        
        for cod in lugars:
            
            if sede == 0 :
                sede = cod.get_text();
                print(sede)
            elif region == 0 :
                region = cod.get_text()
                print(region)
            elif provincia == 0 :
                provincia = cod.get_text();
                print(provincia)
            elif ciudad == 0:
                ciudad = cod.get_text();
                print(ciudad)
            elif zona == 0:
                zona=cod.get_text();
                print(zona)
            

        
        tothora = 0
        tothoras = (res.find("div",{"data-form-static":"curso.informacionGeneral.duracion.valorReferencialPrograma.numeroTotalUnidades"}).select("p"))
        for cod in tothoras:
            tothora=cod.get_text()
            print(tothora)
        
        
        hordoc = 0
        hordocs = (res.find("div",{"data-form-static":"curso.informacionGeneral.duracion.detalleHoras.horasDocencia"}).select("p"))
        for cod in hordocs:
            hordoc=cod.get_text()
            print(hordoc)
        
        
        horpra = 0
        horpras = (res.find("div",{"data-form-static":"curso.informacionGeneral.duracion.detalleHoras.horasPracticas"}).select("p"))
        for cod in horpras:
            horpra=cod.get_text()
            print(horpra)
        
        
        
        horaut = 0
        horauts = (res.find("div",{"data-form-static":"curso.informacionGeneral.duracion.detalleHoras.horasTrabajoAutonomo"}).select("p"))
        for cod in horauts:
            horaut=cod.get_text()
            print(horaut)
        
        
        
                
        hortit = 0
        hortits = (res.find("div",{"data-form-static":"curso.informacionGeneral.duracion.detalleHoras.horasTitulacion"}).select("p"))
        for cod in hortits:
            hortit=cod.get_text()
            print(hortit)
        

        niv = 0;
        
        instituto = 0;
        institutos = (res.find("h4",{"class":"col-md-offset-4"}).select("span"))
        
        for cod in institutos:
            if niv == 0:
                niv=1
            elif niv == 1:
                niv=2
                instituto=cod.get_text()
                print(instituto) 
        
        
        
        
        titulo = 0
        titulos = (res.find("div",{"data-form-static":"curso.requisitoAcademico.titulacion.titulacionNombre.nombre"}).select("p"))
        for cod in titulos:
            titulo=cod.get_text()
            print(titulo)
            
            
        fecing = 0
        fecings = res.find_all(attrs={"class": "form-control-static ng-binding","data-ng-bind":"curso.informacionResoluciones.fechaIngresoCes"})
        for cod in fecings:
            fecing=cod.get_text()
            print(fecing)
            
            
        fecapr = 0
        fecaprs = res.find_all(attrs={"class": "form-control-static ng-binding","data-ng-bind":"curso.informacionResoluciones.fechaAprobacionCes"})
        for cod in fecaprs:
            fecapr=cod.get_text()
            print(fecapr)
            
            
        fecreg = 0
        fecregs = res.find_all(attrs={"class": "form-control-static ng-binding","data-ng-bind":"curso.informacionResoluciones.fechaRegularizacionCes"})
        for cod in fecregs:
            fecreg=cod.get_text()
            print(fecreg)
            
            
            
        fecfin = 0
        fecssfins = res.find_all(attrs={"class": "form-control-static ng-binding","data-ng-bind":"curso.informacionResoluciones.fechaFinVigenciaCes"})
        for cod in fecssfins:
            fecfin=cod.get_text()
            print(fecfin)
            
        
        feciniacre = 0
        feciniacres = res.find_all(attrs={"class": "form-control-static ng-binding","data-ng-bind":"curso.informacionResoluciones.fechaAcreditacionCeaaces"})
        for cod in feciniacres:
            feciniacre=cod.get_text()
            print(feciniacre)
            
        
        
        fecfinacre = 0
        fecfinacres = res.find_all(attrs={"class": "form-control-static ng-binding","data-ng-bind":"curso.informacionResoluciones.fechaFinAcreditacionCeaaces"})
        for cod in fecfinacres:
            fecfinacre=cod.get_text()
            print(fecfinacre)
            
            
        paralelo = 0
        paralelos = res.find_all(attrs={"class": "form-control-static ng-binding","data-ng-bind":"curso.paralelo.paralelos"})
        for cod in paralelos:
            paralelo=cod.get_text()
            print(paralelo)
            
            
        nroest = 0
        nroests = res.find_all(attrs={"class": "form-control-static ng-binding","data-ng-bind":"curso.paralelo.numeroDeEstudiantes"})
        for cod in nroests:
            nroest=cod.get_text()
            print(nroest)
            
        
        
        nrocohorte = 0
        nrocohortes = res.find_all(attrs={"class": "form-control-static ng-binding","data-ng-bind":"curso.paralelo.cohortesPorAno"})
        for cod in nrocohortes:
            nrocohorte=cod.get_text()
            print(nrocohorte)
        
        

        dft1.loc[x]=[x,codigo,regimen,nivel,tipo,cine, amplio,especifico,detallado,  estado,sede, region, provincia,ciudad,zona, tothora, hordoc, horpra,  horaut,hortit,  instituto,titulo,fecing,fecapr,fecreg,fecfin,feciniacre,fecfinacre,paralelo,nroest,nrocohorte]
        
        print(dft1)
        
        #self.driver.close();
        driver.quit()
    
    except:
        print("Unexpected error:")
        print("ERROR x = " + str(x))
        driver.save_screenshot(path_base + "imagenes/error_%s_%02d.png" % (id, x))
        pass
    
dft1.to_excel(r'C:\Users\Santiago\Downloads\monitor_servicios\export_dataframe_tercernivel.xls', index = False, header=True)
    


logging.info("--")
logging.info("Test de Servicios en Línea")
tiempo_inicio = datetime.now()
logging.info("Inicio: %s" % tiempo_inicio.strftime('%Y-%m-%d %H:%M:%S'))
logging.info("")


logging.info("")
logging.info("Fin: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
if alerta:
    contenido = ''
    with FileReadBackwards(log_actual, encoding="utf-8") as BigFile:
        for line in BigFile:
            contenido = line + '\n' + contenido
            if line.find('--') >= 0:
                break
    contenido = contenido.replace('\n', '<br />').replace('ERROR:', '<span style="color: RED; font-weight: '
                                                                    'bold;">ERROR:</span>' )
            # alerta_correo.enviar_correo(tiempo_inicio.strftime('%Y%m%d%H%M%S'), contenido)
    # teams_notificaciones.enviar_notificacion(contenido)
