#!/usr/bin/python3

import argparse
import sys
import glob
sys.path.append("/home/fabrice/Developpe/corpindex-dev/Corpindex")
sys.path.append("/home/fabrice/Bricole/EnCours/Ancfran/bin")
import os
import re

from Dico import Dico
from Variantes import Variantes
from DistanceEdition import DistanceEdition

class P:
	pass
	
parser = argparse.ArgumentParser(description="construction d'un dictionnaire de variantes par distance")
parser.add_argument("-v", "--verbose", help="active affichage informations sur stderr",action="store_true",default=False)
parser.add_argument("-vv", "--stdverbose", help="active affichage informations sur stdout",action="store_true",default=False)
parser.add_argument("-r", "--rules", help="règles de variation",default="")
parser.add_argument("-n", "--nb", type=int,help="profondeur récursion",default=5)
parser.add_argument('-l', "--list", type=str, nargs='+',help='liste des mots',required=True)
parser.add_argument("-d", "--dicts", type=str, nargs='+', help="dictionnaires à utiliser")
args = parser.parse_args(namespace=P)
args = vars(args)

seuil = 0.8

# affiche messages
affout = None
if P.verbose:
	affout = sys.stderr
if P.stdverbose:
	affout = sys.stdout

def afficheLf(txt):
	if affout:
		affout.write("LOG phon:"+txt+"\n")

def affiche(txt):
	if affout:
		affout.write("LOG phon:"+txt)

#  gestion fichiers règles
if P.rules != "":
	vari = Variantes(P.rules)
else:
	vari = Variantes()
	
if P.nb>0:
	vari.setMaxIter(P.nb)

dico = Dico()
de = DistanceEdition()
tabdico = []

# lecture dictionnaires
for dicos in P.dicts:
	afficheLf("=initialisation "+dicos)
	tabdico.append(dicos)
dico.load(tabdico,'dico')
afficheLf("fin lecture")

cpt = 0
for ficlist in P.list:
	for elt in open(ficlist):
		elt = "-"+elt.rstrip()+"-"
		eltnorm = re.sub("-","",elt)
		cpt += 1
		affiche(elt)
		if len(eltnorm)>3: # si le mot est trop petit on ne le regarde pas
			affiche(str(cpt)+'    '+elt+'              '+chr(13))
			vari.change(elt)
			tabres = []
			for v in vari.getVarRegles(): # parcours des résultat de variation v[0] variante, v[1] règles utilisés
				vnorm = re.sub("-","",v[0])
				res = dico.get(vnorm)
				#print(vnorm,res)
				if len(res) != 0:
					# print(vnorm)
					for elex in res:
						try: # parcequ'il y a peut être des bugs dans le dico...
							de.put(eltnorm,vnorm)
							vd = de.distance("jarow")
							#print(vd,seuil)
							if vd>seuil:
								tabres.append((eltnorm,elex,vd,vnorm,v[1]))
						except:
							raise
			tabres = sorted(tabres,key=lambda x:x[2],reverse=True)
			if len(tabres)>0:
				for eltdic in tabres:
					print("\t".join([eltdic[0],eltdic[1]["l"],eltdic[1]["c"],eltdic[1]["d"]+":V:"+str(eltdic[2])[:5],str(eltdic[2]),eltdic[3],str(eltdic[4])]))
			else:
				print("============>\t"+eltnorm,elt)
affiche("FIN PHONO")
