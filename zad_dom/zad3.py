#! /usr/bin/python
# coding utf8
# -*- coding: UTF-8 -*
#Urszula Romaniuk

import re 

def finder(line,regx):

	atr = re.compile(regx)
	return str(re.findall(atr,line))[2:-3]

filename = 'ubuntu_status.txt'
expression = r'^[A-Za-z-]{2,}:'
renazw = r'(Package:) ([A-Za-z0-9-]+)'
renazw2=r'(Section:) ([A-Za-z0-9-]+)'
renazw3=r'(Installed-Size:) ([A-Za-z0-9-]+)'


def find_atrbs(filename,regx):

	atrybuty = set()
	
	with open(filename) as file:

	    for line in file: 

	        atrybuty.add(str(finder(line,regx)))

	return atrybuty


z1=(filter(None, find_atrbs(filename,expression)))
print u"lista wszystkich pojawiajacych sie slow kluczowych: {}".format(z1)

def find_packs(file,regx):

	bledy = 0
	nazwy = []

	with open(file) as f:

		for line in f:

			try:
				nazwy.append(str(re.match(regx,line).group(2)))

			except AttributeError:
				bledy+=1
				continue
	return nazwy

# print 'liczba bledow = ' + str(find_packs(filename,renazw)[1])
#print find_packs(filename,renazw)

z2= len(find_packs(filename,renazw))
print u"calkowita liczba zainstalowanych pakietow: {}".format(z2)

def find_sect(file,regx):

        bledy = 0
        nazwy = {}
        with open(file) as f:

                for line in f:

                        try:

                                z=(str(re.match(regx,line).group(2)))
                                try:
                                        nazwy[z]+=1
                                except KeyError:
                                        nazwy[z]=1

                        except AttributeError:
                                bledy+=1
                                continue
        return nazwy


z3= find_sect(filename,renazw2)
print u'liczba pakietow w kazdej sekcji: {}'.format(z3)

def find_kB(file,regx):

	bledy = 0
	nazwy = []

	with open(file) as f:

		for line in f:

			try:
				nazwy.append(str(re.match(regx,line).group(2)))

			except AttributeError:
				bledy+=1
				continue
	return nazwy


def count(file,regx):
        z=find_kB(file,regx)
        c=0
        for i in xrange(len(z)):
                c+= int(z[i])
        return c
        
    
z4= count(filename,renazw3)

print u"calkowity rozmiar wszystkich pakietow po instalacji: {} kB".format(z4)
