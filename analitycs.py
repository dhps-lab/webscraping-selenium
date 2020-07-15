from pymongo import MongoClient

import matplotlib.pyplot as plt

class ResultadosAño:
	"""docstring for ResultadosAño"""
	year=''
	listax=''
	listay=''
	def __init__(self, year, listax,listay):
		self.year = year
		self.listax = listax
		self.listay = listay


client = MongoClient('localhost',27017)
db = client.loterias
bogota = db.bogota



fechaCont=0
listaObjs=[]
listay=[]
listax=[]
datos = bogota.find().sort('fecha')
for dato in datos:
	print(dato['fecha']+' '+dato['resultado']+' '+dato['serie'])
	fecha= dato['fecha'].split('-')
	print (fecha)
	if int(fecha[0])>fechaCont:
		print (fechaCont)
		if fechaCont!=0:
			obj = ResultadosAño(fechaCont,listax,listay)
			listaObjs.append(obj)
			listay=[]
			listax=[]
		fechaCont=int(fecha[0])
	numeroFecha = int(fecha[1])+(int(fecha[2])/31)
	listax.append(numeroFecha)
	listay.append(int(dato['resultado']))
print (len(listaObjs))
plt.subplot(listaObjs[0].listax,listaObjs[0].listay,'b.',listaObjs[1].listax,listaObjs[1].listay,'y.',listaObjs[2].listax,listaObjs[2].listay,'g.',listaObjs[3].listax,listaObjs[3].listay,'r.',listaObjs[4].listax,listaObjs[4].listay,'y*',listaObjs[5].listax,listaObjs[5].listay,'g^',listaObjs[6].listax,listaObjs[6].listay,'bs')
plt.axis([1,2,0,9999])
plt.subplot(listaObjs[0].listax,listaObjs[0].listay,'b.',listaObjs[1].listax,listaObjs[1].listay,'y.',listaObjs[2].listax,listaObjs[2].listay,'g.',listaObjs[3].listax,listaObjs[3].listay,'r.',listaObjs[4].listax,listaObjs[4].listay,'y*',listaObjs[5].listax,listaObjs[5].listay,'g^',listaObjs[6].listax,listaObjs[6].listay,'bs')
plt.axis([2,3,0,9999])
plt.subplot(listaObjs[0].listax,listaObjs[0].listay,'b.',listaObjs[1].listax,listaObjs[1].listay,'y.',listaObjs[2].listax,listaObjs[2].listay,'g.',listaObjs[3].listax,listaObjs[3].listay,'r.',listaObjs[4].listax,listaObjs[4].listay,'y*',listaObjs[5].listax,listaObjs[5].listay,'g^',listaObjs[6].listax,listaObjs[6].listay,'bs')
plt.axis([3,4,0,9999])
plt.subplot(listaObjs[0].listax,listaObjs[0].listay,'b.',listaObjs[1].listax,listaObjs[1].listay,'y.',listaObjs[2].listax,listaObjs[2].listay,'g.',listaObjs[3].listax,listaObjs[3].listay,'r.',listaObjs[4].listax,listaObjs[4].listay,'y*',listaObjs[5].listax,listaObjs[5].listay,'g^',listaObjs[6].listax,listaObjs[6].listay,'bs')
plt.axis([4,5,0,9999])
plt.subplot(listaObjs[0].listax,listaObjs[0].listay,'b.',listaObjs[1].listax,listaObjs[1].listay,'y.',listaObjs[2].listax,listaObjs[2].listay,'g.',listaObjs[3].listax,listaObjs[3].listay,'r.',listaObjs[4].listax,listaObjs[4].listay,'y*',listaObjs[5].listax,listaObjs[5].listay,'g^',listaObjs[6].listax,listaObjs[6].listay,'bs')
plt.axis([7,6,0,9999])
plt.grid(True)
plt.show()
