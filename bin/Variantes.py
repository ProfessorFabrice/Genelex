#!/usr/bin/python3

import sys
import re
import os
from DistanceEdition import *

class Variantes(object):
	
	def __init__(self,ficr = "variantes.txt",maxiter = 5):
		self.vr = {}
		self.variantes = {}
		self.cout = {}
		self.ficr = ficr
		self.init()
		#print(self.variantes)
		self.maxIter = maxiter
		self.bMaxIter = True
		
	
	# les variantes sont stockées dans un dictionnaire
	# la clef est une reg exp et la valeur un liste de valeurs de remplacement séparée par des '|'
	def init(self):
		# doublement de consonnes
		for c in "btcdnmplr":
			self.variantes[c] = c+c
			self.cout[c] = "0.5"
			self.variantes[c+c] = c
			self.cout[c+c] = "0.5"
			self.variantes[c+"-"+c] = c
			self.cout[c+"-"+c] = "0.5"
		# règles
		#for elt in open(os.path.dirname(os.path.abspath(__file__))+"/"+self.ficr):
		#print("ouverture de",self.ficr)
		for elt in open(self.ficr):
			if elt != "":
				if elt[0] != "#":
					telt = elt.rstrip().split("\t")
					try:
						if len(telt)==3:
							self.variantes[telt[1]] = telt[2]
							self.cout[telt[1]] = telt[0]
						else:
							self.variantes[telt[0]] = telt[1]
					except IndexError:
						print("==>",elt)
						raise
						exit(0)
						pass
						
						
	def __change(self,deb,fin,tab,limit=5):
		ok = False
		if fin != "" and len(tab)<limit:
			for v in self.variantes:
				reser = re.search("(?P<deb>.*?)(?P<motif>"+v+")(?P<fin>.*)",fin)
				if reser:
					deb2 = deb + reser.group("deb")
					fin2 = reser.group("fin") 
					for elt in self.variantes[v].split("|"):
						if reser.group("motif") != elt:
							ru = tab+[reser.group("motif")+":"+elt+":"+str(self.cout[v])]
						else:
							ru = tab
						self.__change(deb2+elt,fin2,ru,limit-1)
		#if not ok:
		if deb+fin in self.vr:
			svarOrig = sum([float(x[-3:]) for x in self.vr[deb+fin]])
			svarNew = sum([float(x[-3:]) for x in tab])
			if svarOrig > svarNew:
				self.vr[deb+fin] = [x for x in tab]
		else:
			self.vr[deb+fin] = [x for x in tab]
					
	def change(self,mot):
		self.vr ={}
		if self.bMaxIter:
			limite = self.maxIter
		else:
			limite = mot.count("-") + 1
			if limite == 1:
				limite = 5
			limite = min(limite,8)
		self.__change("",mot,[],limite)

	def getVariations(self):
		return [x for x in self.vr]

	def getVarRegles(self):
		return [(x,self.vr[x]) for x in self.vr]
		
	def setMaxIter(self,m):
		self.maxIter = m
		self.bMaxIter = True
		
	# calcul d'un fscore entre deux mesures
	# b indique que la mesure r est b fois plus important que p
	def fscore(self,p,r,b=1):
		b2 = b*b
		return (1+b2)*(p*r)/(b2*p+r)


if __name__ == '__main__':
	de = DistanceEdition()
	if len(sys.argv)>1:
		vari = Variantes(sys.argv[1])
	else:
		vari = Variantes()
	mot = sys.argv[2]
	maxiter = 6
	vari.setMaxIter(maxiter)
	print(mot,"=")
	vari.change(mot)
	for elt in vari.getVarRegles():
		s = sum([float(x[-3:]) for x in elt[1]])
		x = 1 - s/maxiter
		de.put(mot,elt[0])
		dst = de.distance(["jarow","base"])
		dstT = vari.fscore(dst,x,1.5)
		#dst2 = de.distance(["base"])
		#print(str(dstT)+"\t"+str(x)+"\t"+str(dst)+"\t"+elt[0]+"\t"+str(elt[1])+"\t"+re.sub("-","",elt[0]))
		print(dstT,"x=",x,"dst=",dst,"mot=",mot,"var=","s=",s,re.sub("-","",elt[0]))
		#vv = Variantes(sys.argv[1])
		#vv.change(elt[0])
		#for v in vv.getVarRegles():
		#	print("\t",v[0]+"\t"+str(v[1]))

