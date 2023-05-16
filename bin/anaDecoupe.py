#!/usr/bin/python3

import sys
import re
import xml.etree.ElementTree as ET


# lecture fichier découpé
dico = {}
tree = ET.parse(sys.argv[1])
root = tree.getroot()
for tag in root.findall("./mot"):
	tab = []
	for v in tag.findall("syllabe"):
		tab.append(v.text)
	print("-".join(tab))


