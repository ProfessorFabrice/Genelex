#!/usr/bin/env python3

import os
import sys
import re
import argparse

#base = os.path.dirname(os.path.abspath(__file__))+"/.."
base = "/home/fabrice/Developpe/corpindex-dev"
sys.path.append(base+"/Corpindex")
sys.path.append(base+"/Corpindex/greffon")

SILENT=True
SEUIL=0.9

from Dico import Dico

# generation d'un dictionnaire à partir d'une sortie

parser = argparse.ArgumentParser(description="interrogation d'un index (version 0.9)")
parser.add_argument("-v", "--verbose", help="active affichage informations",action="store_true",default=False)
parser.add_argument('-i', "--input", type=str, help='fichier corpus',required=True)
parser.add_argument("-d", "--dicts", type=str, nargs='+',help="dictionaries simple words",default=[],required=True)
parser.add_argument('-t', "--vf", type=str, help='type',default="V")

args = parser.parse_args()
args = vars(args)

verb = args['verbose']
input = args['input']
dicts = args["dicts"]
vf = args["vf"]

# dictionnaires
def initDico(dicts):
	dc = Dico(verb)
	dc.load(dicts)
	return dc
	
dico = initDico(dicts)

print(">f\tl\tc\td")
for elt in open(input):
	elt = elt.rstrip().split("\t")
	if len(elt)==5:
		if elt[4] == "True" or elt[4] == "False":
			#print(elt)
			[t,mot,v,s] = elt[0:4]
			if t[0] == vf or t[0].lower() == vf:
				res = dico.get(v)
				if len(res)>0:
					l = res[0]["l"]
					c = res[0]["c"][0]
					print("\t".join([mot,l,c,vf]))
