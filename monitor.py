import os
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
from dotenv import load_dotenv

load_dotenv()

paso = 0
alerta = False
path_base = '/home/edisson/PycharmProjects/monitor_servicios/'
log_actual = path_base + 'logs/monitor_%s.log' % datetime.now().strftime('%Y%m%d')


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
        self.driver = webdriver.Chrome(path_base + 'chromedriver', options=options)
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
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
        self.driver.get("https://www.ups.edu.ec/")
        self.driver.implicitly_wait(5)
        self.driver.set_window_size(1040, 1040)
        self.driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
        self.driver.find_element(By.LINK_TEXT, "Acceder").click()
        self.driver.find_element(By.LINK_TEXT, "Recordar Contraseña").click()
        self.driver.find_element(By.ID, "email").click()
        print(self.driver.page_source)
        self.driver.find_element(By.ID, "email").send_keys(os.environ.get("CORREO_ESTUDIANTE"))
        self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(3) > input").click()

    def test_olvido_su_usuario(self):
        self.driver.get("https://www.ups.edu.ec/")
        self.driver.set_window_size(1040, 1040)
        self.driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
        self.driver.find_element(By.LINK_TEXT, "Acceder").click()
        self.driver.find_element(By.LINK_TEXT, "Olvidó su usuario?").click()
        self.driver.find_element(By.ID, "txtcedula").click()
        self.driver.find_element(By.ID, "txtcedula").send_keys(os.environ.get("CEDULA_COLABORADOR"))
        self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(3) > input").click()
        self.buscar_texto_en_pagina(os.environ.get("CORREO_COLABORADOR"))

    def test_iniciar_sesion(self):
        self.driver.get("https://www.ups.edu.ec/")
        self.driver.set_window_size(1040, 1040)
        self.driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
        self.driver.find_element(By.LINK_TEXT, "Acceder").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys(os.environ.get("CORREO_ESTUDIANTE"))
        self.driver.find_element(By.ID, "password").send_keys(os.environ.get("PASSWORD_ESTUDIANTE"))
        self.driver.find_element(By.NAME, "submit").click()
        # self.driver.find_element(By.CSS_SELECTOR, "#plantillaXhtml > h3").click()
        self.buscar_texto_en_pagina(os.environ.get("NOMBRE_ESTUDIANTE"))

    def test_bolsa_de_trabajo(self):
        self.driver.get("https://bolsadetrabajo.ups.edu.ec/index.xhtml")
        self.driver.set_window_size(1040, 1040)
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "idLoginForm:idUsuarioTxt").send_keys(os.environ.get("CEDULA_COLABORADOR"))
        self.driver.find_element(By.ID, "idLoginForm:idPasswordTxt").send_keys(os.environ.get("CEDULA_COLABORADOR"))
        # self.driver.find_element(By.XPATH, "//[starts-with(@id, 'idLoginForm:j_id')]").send_keys(Keys.ENTER)
        self.driver.implicitly_wait(10)
        # self.driver.save_screenshot(path_base + 'imagenes/bolsa_de_trabajo.png')
        # self.buscar_texto_en_pagina('Nombre de usuario y/o contraseña incorrectos')

    def test_dspace(self):
        self.driver.get("https://dspace.ups.edu.ec/")
        self.driver.set_window_size(1040, 1040)
        self.driver.find_element(By.XPATH, "//p[contains(.,\'Tesis\')]").click()
        self.driver.find_element(By.XPATH, "//p[contains(.,\'Grado\')]").click()
        self.driver.find_element(By.ID, "tbusqueda").click()
        self.driver.find_element(By.ID, "tbusqueda").send_keys("Quintuña")
        self.driver.find_element(By.ID, "tbusqueda").send_keys(Keys.ENTER)
        self.driver.find_element(By.LINK_TEXT,
                                 "Diseño, construcción e implementación del portal Web del Instituto de Teología y "
                                 "Pastoral para Laicos INTEPAL").click()
        self.buscar_texto_en_pagina("Quintuña Padilla, Edisson Pompilio")
        self.driver.find_element(By.LINK_TEXT, "Sign on to:").click()
        self.driver.find_element(By.LINK_TEXT, "My DSpace").click()
        self.driver.find_element(By.LINK_TEXT, "Enter LDAP Netid and Password").click()
        self.driver.find_element(By.NAME, "login_netid").click()
        self.driver.find_element(By.NAME, "login_netid").send_keys(os.environ.get("CORREO_ESTUDIANTE"))
        self.driver.find_element(By.NAME, "login_password").send_keys(os.environ.get("PASSWORD_ESTUDIANTE"))
        self.driver.find_element(By.NAME, "login_submit").click()
        self.buscar_texto_en_pagina("Mi DSpace : Edisson Pompilio Quintuña Padilla")
        self.driver.find_element(By.LINK_TEXT, "Registrado como equintuna@est.ups...").click()
        self.driver.find_element(By.LINK_TEXT, "Salir").click()
        self.buscar_texto_en_pagina("Ha salido de DSpace")

    def test_pagos_en_linea(self):
        self.driver.get("https://www.ups.edu.ec/c/portal/logout")
        self.driver.get("https://www.ups.edu.ec/")
        self.driver.set_window_size(1040, 1040)
        self.driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
        self.driver.find_element(By.LINK_TEXT, "Pagos en linea").click()
        self.driver.find_element(By.XPATH, "//span[contains(.,\'Estudiantes y Colaboradores\')]").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys(os.environ.get("CORREO_ESTUDIANTE"))
        self.driver.find_element(By.ID, "password").send_keys(os.environ.get("PASSWORD_ESTUDIANTE"))
        self.driver.find_element(By.NAME, "submit").click()
        # self.driver.find_element(By.XPATH, "//a[contains(.,\'PAGOS PENDIENTES\')]").click()
        self.driver.find_element(By.ID, "btnsalir:btnSalirSinGuardar").click()


logging.info("--")
logging.info("Test de Servicios en Línea")
tiempo_inicio = datetime.now()
logging.info("Inicio: %s" % tiempo_inicio.strftime('%Y-%m-%d %H:%M:%S'))
logging.info("")

test = Monitor()

test.__init__(identificador=tiempo_inicio.strftime('%Y%m%d%H%M%S'))

test.test_general(test.test_recuperar_contrasena)
test.test_general(test.test_olvido_su_usuario)
test.test_general(test.test_iniciar_sesion)
test.test_general(test.test_bolsa_de_trabajo)
test.test_general(test.test_dspace)
test.test_general(test.test_pagos_en_linea)

test.finalizar_monitor()
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
