# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 09:35:06 2022

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

browser = webdriver.Chrome()
browser.get('https://scholar.google.com/citations?user=kukA0LcAAAAJ')
html = browser.page_source

soup = BeautifulSoup(html, 'lxml')

name = soup.select_one('#gsc_prf_in').text

cititations_all = soup.select_one('tr:nth-child(1) .gsc_rsb_sc1+ .gsc_rsb_std').text
cititations_since_2016 = soup.select_one('tr:nth-child(1) .gsc_rsb_std+ .gsc_rsb_std').text

h_index_all = soup.select_one('tr:nth-child(2) .gsc_rsb_sc1+ .gsc_rsb_std').text
h_index_since_2016 = soup.select_one('tr:nth-child(2) .gsc_rsb_std+ .gsc_rsb_std').text

i_10_index_all = soup.select_one('tr~ tr+ tr .gsc_rsb_sc1+ .gsc_rsb_std').text
i_10_index_since_2016 = soup.select_one('tr~ tr+ tr .gsc_rsb_std+ .gsc_rsb_std').text

data = {
    "Name": [name],
    "Citations": cititations_all,
    "Citations Since 2016": cititations_since_2016,
    "h-index": h_index_all,
    "h-index Since 2016": h_index_since_2016,
    "i10-index": i_10_index_all,
    "i10-index Since 2016": i_10_index_since_2016,
}

df = pd.DataFrame(data)

print(df)
