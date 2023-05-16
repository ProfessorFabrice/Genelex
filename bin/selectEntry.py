#!/usr/bin/python3


import sys
import re

reAna = re.compile("(.*?)\t(.*?)\t(.*?)\t(.*?:([DV]):([.0-9]+))")
seuil = 0.6

# lecture dico
dico = {}
for elt in open(sys.argv[1]):
	analyse = reAna.search(elt)
	if analyse:
		f = analyse.group(1)
		l = analyse.group(2)
		c = analyse.group(3)
		d = analyse.group(4)
		val = float(analyse.group(6))
		if f not in dico:
			dico[f] = [[l,c,d,val]]
		else:
			dico[f].append([l,c,d,val])

print(">f\tl\tc\td")
# selection
for f in dico:
	tri = sorted(dico[f],key=lambda x:x[3],reverse=True)
	maxi = tri[0][3]
	fin = False
	seuilInit = 0
	while len(tri)>0 and not fin:
		e = tri.pop(0)
		if e[3]>seuil and e[3]>=seuilInit:
			seuilInit = e[3]
			print("\t".join([f,e[0],e[1],e[2]]))
		else:
			fin = True
			#sys.stderr.write("rejet->"+"\t".join([f,e[0],e[1],e[2]])+"\n")
			#print("rejet->"+"\t".join([f,e[0],e[1],e[2]]))
			break
