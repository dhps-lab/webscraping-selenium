from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from datetime import timedelta,datetime 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from database import Database

import time, json

urlbase = 'https://www.pagatodo.com.co'

driver = webdriver.Firefox()

def text_of_element(element):
	text = element.get_attribute('href')
	compare_text = '/modules/mod_resultados/secos'
	if text and compare_text in text:
		return text

def text_of_element_p(element):
	text = element.get_attribute('textContent')
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

def convert_results_to_data(results,id, name_lotery):
    dirty = {
		"name": "",
		"number": "	",
		"serie": ''
	}
    result_id = {
        "lotery": name_lotery,
        "raffle_id": id,
		"raffle_mayor":{
			"date": results[0],
			"number": results[1],
			"serie": results[2],
      		},
		"dirties": []
	}
    cont = 1
    dirty = dict()
    for i in range(0,len(results)):
        if i > 2:
            if cont == 1: dirty["name"] = results[i]
            if cont == 2: dirty["number"] = results[i]
            if cont == 3: 
                dirty["serie"] = results[i]
                result_id["dirties"].append(dirty)
                dirty = dict()
                cont = 0
            cont = cont+1
    return result_id

def validate_result_exists(connection:Database, id, name_lotery):
    result = connection.find_results(id,name_lotery)
    if result :
        print('Falses result')
        return True
    else :
        print('True result')
        return False
    
def results_amount(current_id, amount_required):
    if current_id - amount_required < 0:
        return current_id - amount_required
    return amount_required

def insert_result(url_dirty,):
    print('Hola')
    
    	
try:
	driver.get(urlbase + "/resultados.php?plg=resultados-loterias") 
	loterias =	driver.find_elements(By.TAG_NAME,'a') # get all elemens for tag name 'a'
	loterias_map = list(filter(lambda x: x is not None,map(text_of_element,loterias))) # map and filter all elements that are loteries for value of attribute href
	connection = Database()
	

	print(loterias_map,' length of', len(loterias_map))

	for loteria in loterias_map:
     
		# Taking the data from each lotery
		loteria = clean_find_link(loteria)
		link_generated = generate_link_of_lotery(urlbase, loteria)
		last_id = last_id_of_element(loteria)
		name_lotery = find_name_of_lotery(loteria,'secos')
		print('Nombre de la lotería',find_name_of_lotery(loteria,'secos'))
		
		counter = int(last_id)
		target = int( last_id) - 52
		while counter >= target:
			exists = validate_result_exists(connection, str(counter), name_lotery)
			if exists == False :
				# Getting all gift's data
				url_secos = link_generated+'?id='+str(counter)
				#print('Url secos: ', url_secos)
				driver.get(url_secos)
				time.sleep(1)
				results = driver.find_elements(By.TAG_NAME,'p')
				results_map = list(filter(lambda x: x is not None,map(text_of_element_p,results)))
				result_to_insert = convert_results_to_data(results_map,str(counter), name_lotery)
				#print(json.dumps(result_to_insert, indent=4))
				connection.insert_result(result_to_insert)
			counter = counter-1

except AttributeError:
	print( "Error in attribute: ", AttributeError.name)

finally:
	print('[END] Executing with selenium terminated')
	driver.close()

