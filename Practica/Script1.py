# coding: utf-8

import csv

from HTMLParser import HTMLParser

allrest=[]


class restaurant(object):
    nom = ""
    adreca = ""
    districte = ""
    barri = ""
    postal = ""
    telefon = ""
    telefon2 = ""
    latitud = ""
    longitud = ""
    web = ""

    def afegir_nom(self, nom):
        if self.nom == "":
            self.nom = nom
        else:
            self.nom = self.nom + '&' + nom

    def afegir_adreca(self, adreca):
        if adreca.find('C') == 0:
            self.adreca = "Carrer" + adreca[1:]
        elif adreca.find('P') == 0 and adreca.find('l') == 1:
            self.adreca = "Plaça" + adreca[2:]
        elif adreca.find('G') == 0 and adreca.find('V') == 2:
            self.adreca = "Gran Via" + adreca[4:]
        elif adreca.find('A') == 0 and adreca.find('v') == 1:
            self.adreca = "Avinguda" + adreca[2:]
        elif adreca.find('P') == 0 and adreca.find('t') == 1 and adreca.find('g') == 2 and adreca.find('e') == 3:
            self.adreca = "Passatge" + adreca[4:]
        elif adreca.find('P') == 0 and adreca.find('g') == 1:
            self.adreca = "Passeig" + adreca[2:]
        elif adreca.find('R') == 0 and adreca.find('b') == 1 and adreca.find('l') == 2 and adreca.find('a') == 3:
            self.adreca = "Rambla" + adreca[4:]
        elif adreca.find('P') == 0 and adreca.find('t') == 1 and adreca.find('j') == 2 and adreca.find('a') == 3:
            self.adreca = "Platja" + adreca[4:]
        elif adreca.find('T') == 0 and adreca.find('r') == 1 and adreca.find('a') == 2 and adreca.find('v') == 3:
            self.adreca = "Travessera" + adreca[4:]
        else:
            self.adreca = adreca

    def afegir_districte(self, districte):
        self.districte = districte

    def afegir_barri(self, barri):
        self.barri = barri

    def afegir_postal(self, postal):
        self.postal = postal

    def afegir_telefon(self, telefon):
        if telefon.find('+34') != -1:
            if self.telefon != "" and telefon != self.telefon:
                self.telefon2 = telefon
            else:
                self.telefon = telefon

    def afegir_latitud(self, latitud):
        self.latitud = latitud

    def afegir_longitud(self, longitud):
        self.longitud = longitud

    def afegir_web(self, web):
        webdos = ' '.join(web[0])
        pag_web_ini = webdos.find('http')
        if pag_web_ini != -1:
            self.web = webdos[pag_web_ini:]


class MHTMLParser(HTMLParser):

    crest = restaurant()
    ctag = ""

    def handle_starttag(self, tag, attrs):
        self.ctag = tag
        if tag == 'v:vcard':
            self.crest = restaurant()
        if tag == 'v:url':
            self.crest.afegir_web(attrs)

    def handle_endtag(self, tag):
        self.ctag = ""
        if tag == 'v:vcard':
            allrest.append(self.crest)

    def handle_data(self, data):
        if self.ctag == 'v:fn':
            self.crest.afegir_nom(data)
        if self.ctag == 'v:street-address':
            self.crest.afegir_adreca(data)
        if self.ctag == 'xv:district':
            self.crest.afegir_districte(data)
        if self.ctag == 'xv:neighborhood':
            self.crest.afegir_barri(data)
        if self.ctag == 'v:postal-code':
            self.crest.afegir_postal(data)
        if self.ctag == 'rdf:value':
            self.crest.afegir_telefon(data)
        if self.ctag == 'v:latitude':
            self.crest.afegir_latitud(data)
        if self.ctag == 'v:longitude':
            self.crest.afegir_longitud(data)



f = open('restaurants.rdf', 'rb') # obre l'arxiu
rdfSource = f.read()
f.close()

csvOpen = open('restaurants.csv', 'wb')
csvSource = csv.writer(csvOpen)

parser = MHTMLParser()
parser.feed(rdfSource)

csvSource.writerow(["Nom"] + ["Adreça"] + ["Districte"] + ["Barri"] + ["Codi Postal"] + ["Telèfon"] +
["Telèfon 2"] + ["Latitud"] + ["Longitud"] + ["Web"])
for r in allrest:
    csvSource.writerow([r.nom] + [r.adreca] + [r.districte] + [r.barri] + [r.postal] + [r.telefon] +
    [r.telefon2] + [r.latitud] + [r.longitud] + [r.web])