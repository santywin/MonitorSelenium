# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 17:47:12 2022

@author: Santiago
"""
import psycopg2, psycopg2.extras
import pandas as pd
import numpy as np

def download():    
    
    conn = psycopg2.connect(database='lala',user='lala',password='PB2Cx3fDEgfFTpPn', host='172.16.101.55')

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    print("Bajando datos de empleados")
    cur.execute("select document from counselor;")# ORDER BY id")
    data =cur.fetchall();
    df = pd.DataFrame(np.array(data), columns = data[0].keys())

    
    return df


def downloadDescargados():    
    
    conn = psycopg2.connect(database='senescyt',user='postgres',password='admin123', host='127.0.0.1')

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    print("Bajando datos de empleados")
    cur.execute("select cedula as document from principal;")# ORDER BY id")
    data =cur.fetchall();
    df = pd.DataFrame(np.array(data), columns = data[0].keys())

    
    return df

