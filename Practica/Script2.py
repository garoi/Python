# coding: utf-8

import csv
import math
import urllib
import operator
import webbrowser
import xml.etree.ElementTree as ET

sock = urllib.urlopen("http://wservice.viabicing.cat/getstations.php?v=1")
xmlSource = sock.read()
sock.close()

root = ET.fromstring(xmlSource)

llista_final = []
llista_paraulas_and = []
restaurants = []
llista_paraulas_or = []

def tractar_llista_or(s):
	cont = 0
	cont_dos = 0
	entro = False
	while cont < len(s):
		carac = s[cont]
		if carac == "'":
			if entro == True:
				llista_paraulas_or.append(s[cont_dos+1:cont])
				entro = False
			else:
				entro = True
				cont_dos = cont
		cont = cont + 1

def tractar_llista_and(s):
	cont = 0
	cont_dos = 0
	entro = False
	while cont < len(s):
		carac = s[cont]
		if carac == "'":
			if entro == True:
				llista_paraulas_and.append(s[cont_dos+1:cont])
				entro = False
			else:
				entro = True
				cont_dos = cont
		cont = cont + 1

def agafar_or():
	primera_iteracio = True
	with open('restaurants.csv', 'rb') as f:
		reader = csv.reader(f, delimiter = ',')
		for row in reader:
			if primera_iteracio == True:
				primera_iteracio = False
			else:
				for para in llista_paraulas_or:
					if row[0].find(para) != -1:
						llista_final.append(row[0])
						break

def agafar_and():
	primera_iteracio = True
	with open('restaurants.csv', 'rb') as f:
		reader = csv.reader(f, delimiter = ',')
		for row in reader:
			if primera_iteracio == True:
				primera_iteracio = False
			else:
				tot_correcte = []
				for para in llista_paraulas_and:
					if row[0].find(para) != -1:
						tot_correcte.append(True)
				if len(tot_correcte) == len(llista_paraulas_and):
					llista_final.append(row[0])

def fer_and():
	cont = 0
	if llista_final !=[]:
		while cont < len(llista_final):
			elem = llista_final[cont]
			for para in llista_paraulas_and:
				if elem.find(para) == -1:
					llista_final.pop(cont)
					cont  = cont - 1
			cont  = cont + 1
		cont = 0
		if len(llista_final) > 1:
			while cont < len(llista_final):
				cont2 = 0
				while cont2 < len(llista_final):
					if llista_final[cont] == llista_final[cont2] and cont2 != cont:
						llista_final.pop(cont)
						cont = cont - 1
					cont2 = cont2 + 1
				cont = cont + 1

def restaurants_seleccionats():
	primera_iteracio = True
	for elem in llista_final:
		with open('restaurants.csv', 'rb') as f:
			reader = csv.reader(f, delimiter = ',')
			for row in reader:
				if primera_iteracio == True:
					primera_iteracio = False
				else:
					if elem == row[0]:
						aux2 = []
						aux2.append(row[0])
						aux2.append(row[1])
						aux2.append(row[2])
						aux2.append(row[3])
						aux2.append(row[4])
						aux2.append(row[5])
						aux2.append(row[6])
						aux2.append(row[7])
						aux2.append(row[8])
						aux2.append(row[9])
						aux3 = []
						aux2.append(aux3)
						restaurants.append(aux2)
						break

entrada = raw_input("Entra la teva consulta: ");
if entrada[0] == '"' and entrada[1] =="'":
	paraula = entrada[(entrada.index('"')+2):(len(entrada)-2)]
	llista_paraulas_and.append(paraula)
	agafar_and()
elif entrada[1] == "(":
	cont = 0
	entro = False
	cont_dos = 0
	while cont < len(entrada):
		carac = entrada[cont]
		if carac == "[":
			tcont = cont
			while entrada[cont] != "]":
				cont = cont + 1
			tractar_llista_or(entrada[tcont+1:cont-1])
			agafar_or()
		elif carac == "'":
			if entro == True:
				llista_paraulas_and.append(entrada[cont_dos+1:cont])
				entro = False
			else:
				entro = True
				cont_dos = cont
		cont = cont + 1
	agafar_and()
elif entrada[1] == "[":
	cont = 0
	entro = False
	cont_dos = 0
	while cont < len(entrada):
		carac = entrada[cont]
		if carac == "(":
			tcont = cont
			while entrada[cont] != ")":
				cont = cont + 1
			tractar_llista_and(entrada[tcont+1:cont])
			agafar_and()
		elif carac == "'":
			if entro == True:
				llista_paraulas_or.append(entrada[cont_dos+1:cont])
				entro = False
			else:
				entro = True
				cont_dos = cont
		cont = cont + 1
	agafar_or()


fer_and()
if llista_final != []:
	restaurants_seleccionats()
	for estacio in root.findall('station'):
		slots = int(estacio.find('slots').text)
		bikes = int(estacio.find('bikes').text)
		carrer = estacio.find('street').text
		numeroCarrer = estacio.find('streetNumber').text
		latitud = estacio.find('lat').text
		longitud = estacio.find('long').text
		latb = float(latitud)
		lonb = float(longitud)
		for restaurant in restaurants:
			latr = float(restaurant[7])
			lonr = float(restaurant[8])
			r = 6371000
			c = float(math.pi)/float(180.0)
			d = 2*r*math.asin(math.sqrt(math.sin(c*(latb-latr)/2)**2 + math.cos(c*latr)*math.cos(c*latb)*math.sin(c*(lonb-lonr)/2)**2))
			if d <= 1000:
				bicing = restaurant[10]
				aux = (slots,bikes, carrer, numeroCarrer, d)
				bicing.append(aux)
				restaurant[10] = bicing
html_inici = """<html>
<head>
	<title>Practica Python</title>
	<meta charset="utf-8" />
</head>
<body>\n"""

html_filas = """<tr bgcolor="#3366FF" align="center">
<td><strong>Nom Restaurant</strong></td>
<td><strong>Dades</strong></td>
<td><strong>Bicings Slots</strong></td>
<td><strong>Bicings Lliures</strong></td>
</tr>"""

html = open('index.html', 'w')
html.write(html_inici)
if restaurants != []:
	html.write('<table border="1">\n')
	html.write(html_filas)
	for elem in restaurants:
		html.write('<tr>\n')
		html.write('<td>\n' + '<strong>' + elem[0] + '</strong>' + '\n</td>')
		html.write('<td>\n' + elem[1] + '<br>' + elem[2] + '<br>' + elem[3] + '<br>' + elem[4] + '<br>' + elem[5] + '<br>' + elem[6] + '<br>' + elem[9] + '</td>\n')
		aux = elem[10]
		aux.sort(key=operator.itemgetter(4))
		html.write('<td>')
		for e in aux:
			if e[0] >= 1:
				html.write(str(e[2]) + " " + str(e[3]) + str(", "))
		html.write('</td>')
		html.write('<td>')
		for e in aux:
			if e[1] >= 1:
				html.write(str(e[2]) + " " + str(e[3]) + str(", "))
		html.write('</td>')
		html.write('</tr>\n')
	html.write('</table>\n')
	html.write('</body>\n')
else:
	html.write('<h1>LA TEVA CONSULTA NO HA DONAT RESULTATS</h1>')

nav = raw_input("Vols obrir el navegador i veure la teva consula? y/n: ");
if nav == "y":
	webbrowser.open('index.html')