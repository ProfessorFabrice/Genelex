#!/usr/bin/env python3

import sys
import re
import argparse

base = "/home/fabrice/Developpe/corpindex-dev"
sys.path.append(base+"/Corpindex")
sys.path.append(base+"/Corpindex/greffon")

from Cquery import Cquery
from Dico import Dico

parser = argparse.ArgumentParser(description="interrogation d'un index (version 0.9)")
parser.add_argument("-v", "--verbose", help="active affichage informations",action="store_true",default=False)
parser.add_argument('-i', "--input", type=str, help='fichier corpus',required=True)
parser.add_argument('-f', "--filtre", type=str, help='filtre',default="False")
parser.add_argument('-o', "--out", type=str, help='type de sortie',default="xml")
parser.add_argument('-r', "--result", type=str, help='fichiers résultat',required=True)
parser.add_argument("-d", "--dicts", type=str, nargs='+',help="dictionaries simple words",default=[],required=True)
parser.add_argument("-a", "--all", help="active affichage tout",action="store_true",default=False)
args = parser.parse_args()
args = vars(args)

verb = args['verbose']
input = args['input']
result = args["result"]
filtre = args["filtre"]
out = args["out"]
all = args["all"]
dicts = args["dicts"]


cq = Cquery()
cq.featureList += ["m","d","r"]
cq.open(input)
dicoT = Dico(verb)
dicoT.load(dicts)


def sortieXml(test,v,s,f):
	print('<lex type="'+test+'" f="'+f+'">')
	print("\t<v>"+v[1]+"</v>")
	print("\t<s>"+s[1]+"</s>")
	conc = cq.getConcordance('[l="'+f+'"]')
	for c in conc:
		print("\t<conc>"+" ".join([x for x in c["l"]])+" <q>"+" ".join([x for x in c["q"]])+"</q> "+" ".join([x for x in c["r"]])+"</conc>")
	print("</lex>")
	
def sortieCsv(test,v,s,f):
	if test=="True":
		print("A",end="")
	else:
		print(" ",end="")
	res1 = dicoT.get(v[1])
	res2 = dicoT.get(s[1])
	l1 = ""
	l2 = ""
	if len(res1)>0:
		l1 = res1[0]["l"]
	if len(res2)>0:
		l2 = res2[0]["l"]
	print("\t"+"\t".join([f,v[1]+"("+l1+")",s[1]+"("+l2+")",test]))
	print("\t"+"\t".join(["",str(v[-1]),str(s[-1])]))
	conc = cq.getConcordance('[l="'+f+'"]')
	for c in conc:
		l = " ".join([x for x in c["l"]])
		q = " ".join([x for x in c["q"]])
		r = " ".join([x for x in c["r"]])
		print("\t"+"\t".join(["\t","\t",l,q,r]))

etat = 0
dico = {"formeC":{},"formeD":{},"formeS":{}}
for elt in open(result):
	elt = elt.rstrip()
	tab = elt.split("\t")
	if re.search("^forme",tab[0]):
		t = tab[0]
		f = tab[1][1:]
		dico[t][f] = {"v":[],"s":[]}
	else:
		vs = tab[1]
		tab[2] = eval(tab[2])
		#print(t,f,vs,tab[2])
		dico[t][f][vs].append(tab[2])
if out == "csv":
	print("res\tforme\tvariante\tmv\tsimilarité\tvs\tégal\tgauche\trequete\tdroit")
for t in dico:
	for f in dico[t]:
		if len(dico[t][f]["v"]) == 0:
			v = ["-","XXX"]
		else:
			v = dico[t][f]["v"][0]
		if len(dico[t][f]["s"]) == 0:
			s = ["-","XXX"]
		else:
			s = dico[t][f]["s"][0]
		test = str(v[1] == s[1])
		if test == filtre or all:
			if out == "xml":
				sortieXml(test,v,s,f)
			else:
				#print("\nv=",v,"\ns=",s,"\nf=",f,"\n")
				sortieCsv(test,v,s,f)
