# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

path_base = '/home/edisson/PycharmProjects/monitor_servicios/'

class TestCES1():

    def __init__(self, identificador=""):
        self.id = identificador
        self.driver = webdriver.Chrome(path_base + 'chromedriver', options=options)
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.set_page_load_timeout(30)  # Tiempo en segundos

    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_cES1(self):
        self.driver.get("http://appcmi.ces.gob.ec/oferta_vigente/maestrias/postgrados.php")
        self.driver.set_window_size(1270, 669)
        self.driver.switch_to.frame(1)
        self.driver.find_element(By.ID, "Consultar").click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(2)
        self.driver.find_element(By.NAME, "submit").click()
        self.driver.find_element(By.CSS_SELECTOR, "td > .btn").click()
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) .btn").click()
        self.driver.find_element(By.CSS_SELECTOR, "td > .btn").click()
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(4) .btn").click()
        print(self.driver.page_source)
        self.driver.find_element(By.CSS_SELECTOR, "td > .btn").click()


test = TestCES1()
test.test_cES1()


