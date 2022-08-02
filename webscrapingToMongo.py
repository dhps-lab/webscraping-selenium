from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from datetime import timedelta,datetime 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

import time

urlbase = 'https://www.pagatodo.com.co'

driver = webdriver.Firefox()

def text_of_element(element):
	text = element.get_attribute('href')
	compare_text = '/modules/mod_resultados/secos'
	if text and compare_text in text:
		return text

def find_name_of_lotery(text, keyword):
	if text in [None, ''] or keyword in [None, '']:
		print('Text or keyword not found')
		return None
	index_keyword = text.find(keyword) + len(keyword)
	index_dot = text.find('.')
	text_without_spaces = text[index_keyword:index_dot].replace('-',' ')
	return text_without_spaces.strip()

def last_id_of_element(text):
	if text in [None, '']:
		print('Text not found')
		return None
	index_id = text.find('id') + 3
	return text[index_id:text.find('\'')]

# method temporal while not using database connection
def clean_find_link(text):
	if text in [None, '']:
		print('Text to clean is empty')
		return None
	
	url_complement_lotery = text[32:-1]
	return url_complement_lotery

def generate_link_of_lotery(urlbase, text_lotery):
	if urlbase in [None, ''] or text_lotery in [None, ''] :
		print('Urlbase or text_lotery are empty')
		return None
		
	#query path relative for the lotery
	link_lotery = urlbase + text_lotery
	link_lotery = link_lotery[:link_lotery.find('?')]
	return link_lotery
    	
try:
	driver.get(urlbase + "/resultados.php?plg=resultados-loterias") 
	loterias =	driver.find_elements(By.TAG_NAME,'a') # get all elemens for tag name 'a'
	loterias_map = list(filter(lambda x: x is not None,map(text_of_element,loterias))) # map and filter all elements that are loteries for value of attribute href

	print(loterias_map,' length of', len(loterias_map))

	for loteria in loterias_map:
		loteria = clean_find_link(loteria)
		link_generated = generate_link_of_lotery(urlbase, loteria)
		print('Nombre de la lotería',find_name_of_lotery(loteria,'secos'))
		print('Url de la lotería', link_generated)
		print('Id de la lotería', last_id_of_element(loteria))

except AttributeError:
	print( "Error in attribute: ", AttributeError.name)

finally:
	print('Executing with selenium terminated')
	driver.close()


"""client = MongoClient('localhost',27017)

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
"""












