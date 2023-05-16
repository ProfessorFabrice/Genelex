#!/usr/bin/python3

import argparse
import re
import sys
import glob
import os

base = "/home/fabrice/Developpe/corpindex-dev"
sys.path.append(base+"/Corpindex")
sys.path.append(base+"/Corpindex/greffon")

from Dico import Dico
from DistanceEdition import DistanceEdition

dico =  Dico()
de = DistanceEdition()
dicoTaille = {}
dicoSort = {}

class P:
	pass
	
parser = argparse.ArgumentParser(description="construction d'un dictionnaire de variantes par distance")
parser.add_argument("-v", "--verbose", help="active affichage informations sur stderr",action="store_true",default=False)
parser.add_argument("-vv", "--stdverbose", help="active affichage informations sur stdout",action="store_true",default=False)
parser.add_argument("-s", "--seuil", type=float,help="seuil de selection 0 < s <= 1",default="0.65")
parser.add_argument('-l', "--list", type=str, nargs='+',help='liste des mots',required=True)
parser.add_argument("-d", "--dicts", type=str, nargs='+', help="dictionnaires à utiliser")
args = parser.parse_args(namespace=P)
args = vars(args)

# affiche messages
affout = None
if P.verbose:
	affout = sys.stderr
if P.stdverbose:
	affout = sys.stdout

def affiche(txt):
	if affout:
		affout.write("LOG dist:"+txt+"\n")

# initialisation dictionnaires (classement par taille des formes)
def initSimilarite():
	lstForme = set(dico.dictSw.keys())
	for f in lstForme:
		t = len(f)
		if t not in dicoTaille:
			dicoTaille[t] = []
		dicoTaille[t].append(f)
			

# calcul de similarité
	
def similarite(mot):
	res = {}
	l = len(mot)
	if l in dicoTaille or l-1 in dicoTaille or l+1 in dicoTaille:
		for f in dicoTaille[l-1]+dicoTaille[l]+dicoTaille[l+1]:
			de.put(mot,f)
			md = de.distance(["jarow"])
			if md>P.seuil:
				res[f] = md
	return res



dico = Dico()
de = DistanceEdition()
tabdico = []

# lecture dictionnaires
for dicos in P.dicts:
	affiche("initialisation "+dicos)
	tabdico.append(dicos)
dico.load(tabdico,'dico')
affiche("fin lecture")

# initialisation
initSimilarite()
affiche("fin initialisation")


cpt = 0
resTot = []
for ficlist in P.list:
	for i in open(ficlist):
		cpt += 1
		m = i.rstrip('\n')
		dicRes = []
		if len(dico.get(m)) == 0 and len(m)>2:
			affiche(m)
			res = similarite(m)
			for elt in res:
				dst = res[elt]
				if dst>0.9:
					tab = dico.get(elt)
					for ldic in tab:
						aff = m+"\t"+elt+"\t"+ldic["l"]+"\t"+ldic["c"]+"\t"+ldic["m"]+"\tL"
						dicRes.append((aff,dst))
		dicRes = sorted(dicRes,key=lambda x:x[1],reverse=True)
		resTot += dicRes
for elt in resTot:
	print(elt[0]+"\t"+str(elt[1]))					

