from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from datetime import timedelta,datetime 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

import time

driver = webdriver.Firefox()

driver.get("https://www.pagatodo.com.co/resultados?acordeon=loterias") 

client = MongoClient('localhost',27017)

db = client.loterias
bogota = db.bogota

datatimefecha=datetime(2014,2,13,0,0)

while datatimefecha < datetime.today():
	
	strfecha=str(datatimefecha).split(" ")[0].split("-")
	elemento =	driver.find_element_by_id("edit-datapiker-loterias")
	elemento.send_keys(strfecha[2]+"/"+strfecha[1]+"/"+strfecha[0])
	elemento2 = driver.find_element_by_id("form-baloto-loterias")
	elemento2.submit() 
	time.sleep(2)
	nuevo = driver.find_elements_by_tag_name("table") 
	datos = nuevo[3].text.split("\n")
	#print (datos) 
	datatimefecha=datatimefecha+timedelta(days=7)
	driver.get("https://www.pagatodo.com.co/resultados?acordeon=loterias")
	if 'Lotería de Bogotá' in datos :
		indice = datos.index('Lotería de Bogotá')
		print (datos[indice]+'->'+datos[indice+1]+' resultado ->'+datos[indice+2]+' serie->'+datos[indice+3])
		datoNuevo = {
			'Loteria' : datos[indice],
			'fecha' : datos[indice+1],
			'resultado' : datos[indice+2],
			'serie' : datos[indice+3]
		}
		result = bogota.insert_one(datoNuevo)




driver.close()








