#!/usr/bin/env python3

import os
import sys
import re
import argparse
from shell_utils import shell
import xml.etree.ElementTree as ET

#base = os.path.dirname(os.path.abspath(__file__))+"/.."
base = "/home/fabrice/Developpe/corpindex-dev"
sys.path.append(base+"/Corpindex")
sys.path.append(base+"/Corpindex/greffon")

SILENT=True
SEUIL=0.9

from Cquery import Cquery
from Variantes import Variantes
from Dico import Dico
from DistanceEdition import DistanceEdition

parser = argparse.ArgumentParser(description="interrogation d'un index (version 0.9)")
parser.add_argument("-v", "--verbose", help="active affichage informations",action="store_true",default=False)
parser.add_argument("-d", "--dicts", type=str, nargs='+',help="dictionaries simple words",default=[],required=True)
parser.add_argument('-i', "--input", type=str, help='fichiers à traiter',required=True)
parser.add_argument('-r', "--rules", type=str, help='fichiers de règles de transduction',required=True)
args = parser.parse_args()
args = vars(args)

verb = args['verbose']
input = args['input']
dicts = args['dicts'] 
rules = args['rules'] 

BIN=os.path.dirname(os.path.abspath(__file__))
REPRES=os.path.dirname(os.path.abspath(input))
decoupeListe = f'{BIN}/decoupeListe.sh'

VERB = True

# log
def log(msg):
	if VERB:
		sys.stderr.write("LOG: "+msg+"\n")

# création dictionnaire
def createDico(t):
	res = {}
	for elt in t:
		for e in elt:
			k = e[0]
			if k not in res:
				res[k] = []
			res[k].append(e)
	return res
			
# calcul d'un fscore entre deux mesures
# b indique que la mesure r est b fois plus important que p
def fscore(p,r,b=1):
	b2 = b*b
	return (1+b2)*(p*r)/(b2*p+r)

# dictionnaires
def initDico(dicts):
	dc = Dico(verb)
	dc.load(dicts)
	return dc

# initialisation dictionnaires (classement par taille des formes)
def initSimilarite(dico):
	lstForme = set(dico.dictSw.keys())
	dicoTaille = {}
	for f in lstForme:
		t = len(f)
		if t not in dicoTaille:
			dicoTaille[t] = []
		dicoTaille[t].append(f)
	return dicoTaille

	
# construction d'un index
def buildIdx(fichier,dicts,verb=False):
	cq = Cquery()
	cq.verbose = verb
	cq.dicts = dicts
	cq.featureList += ["m","d","r"]
	cq.open(fichier,mode="f",ldict=dicts)
	return cq

# liste des mots inconnus
def inconnus(cq,name):
	res = set()
	conc = cq.cqpl('[c="?"]')
	for elt in conc:
		forme = cq.getElement(elt[0])[0]
		res.add(forme)
	log("nombres inconnus : "+str(len(res)))
	ptfic = open(name,"w")
	for elt in res:
		ptfic.write(elt+"\n")
	ptfic.close()

# découpage en syllabes
def syllabe(namein):
	dcp = shell(decoupeListe+" "+namein,capture=True,silent=SILENT)
	root = ET.fromstring(dcp.stdout)
	res = []
	for tag in root.findall("./mot"):
		tab = []
		for v in tag.findall("syllabe"):
			tab.append(v.text)
		res.append("-".join(tab))
	return res

# calcul de variantes
def variantes(formes,rules,dico):
	resultat = []
	seuil = 0.4
	de = DistanceEdition()	
	vari = Variantes(rules)
	maxiter = 6
	vari.setMaxIter(maxiter)
	for elt in formes:
		#log("variante:"+elt)
		elt = "-"+elt.rstrip()+"-"
		eltnorm = re.sub("-","",elt)
		if len(eltnorm)>3: # si le mot est trop petit on ne le regarde pas
			vari.change(elt)
			tabres = []
			for v in vari.getVarRegles(): # parcours des résultat de variation v[0] variante, v[1] règles utilisés
				vnorm = re.sub("-","",v[0])
				res = dico.get(vnorm)
				#print(eltnorm,vnorm,v[0],len(res))
				if len(res) != 0:
					lstlem = {x["l"] for x in res}
					de.put(elt,v[0])
					dst = de.distance(["jarow","base"])
					if dst>0:
						s = sum([float(x[-3:]) for x in v[1]])
						x = 1 - s/maxiter
						dstT = fscore(dst,x,1.5)
						tabres.append((eltnorm,vnorm,lstlem,v[1],dst,x,dstT))
			if len(tabres)>0:
				tabres = sorted(tabres,key=lambda x:x[6],reverse=True)
				resultat.append(tabres)
	return resultat

# calcul de similarité	
def similarite(formes,dicoTaille,dico):
	de = DistanceEdition()
	seuil = 0.8
	resultat = []
	for mot in formes:
		tabres = []
		mot = re.sub("-","",mot)
		#log("simil:"+mot)
		l = len(mot)
		if l in dicoTaille or l-1 in dicoTaille or l+1 in dicoTaille:
			for f in dicoTaille[l-1]+dicoTaille[l]+dicoTaille[l+1]:
				de.put(mot,f)
				md = de.distance(["jarow"],cut=SEUIL)
				if md>0:
					res = dico.get(f)
					lstlem = {x["l"] for x in res}
					tabres.append([mot,f,lstlem,md])
		tabres = sorted(tabres,key=lambda x:x[3],reverse=True)
		resultat.append(tabres)
	return resultat


	


dictionnaire = initDico(dicts)
dicoTaille = initSimilarite(dictionnaire)
cq = buildIdx(input,dictionnaire,verb=True)
inconnus(cq,"lstinc.txt")
dcp = sorted(syllabe("lstinc.txt"))
log("fin syllabe : "+str(len(dcp)))
fic = open("decoupe.txt","w")
for elt in dcp:
	fic.write(elt+"\n")
fic.close()
ndicv = variantes(dcp,rules,dictionnaire)
log("fin variantes")
f = {}
for elt in ndicv:
	k = elt[0][0]
	f[k] = elt
dv = createDico(ndicv)
log("fin variantes")
ndics = similarite(f,dicoTaille,dictionnaire)
log("fin similarité")
ds = createDico(ndics)
inter=set(dv).intersection(set(ds))
dvm = set(dv).difference(inter)
dsm = set(ds).difference(inter)
for f in inter:
	print("formeC\t",f)
	for v in dv[f]:
		print("\tv\t",v)
	for s in ds[f]:
		print("\ts\t",s)
for f in dvm:
	print("formeD\t",f)
	for v in dv[f]:
		print("\tv\t",v)
for f in dsm:
	print("formeS\t",f)
	for s in ds[f]:
		print("\ts\t",s)
	
