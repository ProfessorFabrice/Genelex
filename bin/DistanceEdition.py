#!/usr/bin/python3

#import difflib
import Levenshtein as L
import sys

class DistanceEdition(object):
	
	def __init__(self):
		self.mot1 = ""
		self.mot2 = ""
		
	def put(self,mot1,mot2):
		self.mot1 = mot1
		self.mot2 = mot2
		
	# calcul de distance d'édition avec valeur phon
	def distance(self,type=["jaro"],cut=None):
		m1 = self.mot1
		m2 = self.mot2
		mesure = []
		if "jaro" in type:
			mesure.append(L.jaro(m1,m2,score_cutoff=cut))
		if "jarow" in type:
			mesure.append(L.jaro_winkler(m1,m2,score_cutoff=cut))
		if "ratio" in type:
			mesure.append(L.ratio(m1,m2,score_cutoff=cut))
		if "base" in type:
			mesure.append(min(len(m1),len(m2))/max(len(m1),len(m2)))
		if "leven" in type:
			mesure.append(L.distance(m1,m2))
		if "edit" in type:
			mesure.append(1/sum([1 if x[0]=='replace' else 0 for x in L.editops(m1,m2)]))
		if len(mesure)>0:
			dst = sum(mesure)/len(mesure)
		else:
			dst = 0
		return dst
		
	# simple distance de Jaro winkler
	def leven(self):
		m1 = self.mot1
		m2 = self.mot2
		dst = L.distance(m1,m2)
		return dst
		
	# simple distance de Jaro winkler
	def edit(self):
		m1 = self.mot1
		m2 = self.mot2
		dst = L.editops(m1,m2)
		return dst
		


if __name__ == '__main__':
	de = DistanceEdition()
	de.put(sys.argv[1],sys.argv[2])
	print(de.distance(["jarow","base"],0.9))
	print(de.distance(["jarow","base"]))
