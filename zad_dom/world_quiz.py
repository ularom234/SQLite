# -*- coding: cp1250 -*-
#Urszula Romaniuk
from numpy import random
import sqlite3
import datetime as t
from sys import argv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#odkodowuje nazwy i nie wyrzuca bledu o kodowaniu ASCII



def create_table(x=0):
	cur.execute("CREATE TABLE IF NOT EXISTS wyniki_quizu(seria int, wyniki int, data real)")

def pytania():
        pkt=0
        bledy=0
        for i in range(5):
                panstwo,miasto = c.execute('SELECT p.name, m.name FROM country p JOIN city m ON m.ID = p.CAPITAL ORDER BY random() LIMIT 1;').fetchone()
                #losowalo wczesnie ze wszytskich stolic a ma byc z miast
                #miasto2,miasto3,miasto4 = c.execute('SELECT m.name FROM city m JOIN country p ON m.id = p.capital ORDER BY random() LIMIT 3;').fetchall()
                miasto2,miasto3,miasto4 = c.execute('SELECT name FROM city ORDER BY random() LIMIT 3;').fetchall()
                m=[miasto2,miasto3,miasto4]
                while miasto in m:
                                miasto2,miasto3,miasto4 = c.execute('SELECT m.name FROM city m JOIN country p ON m.id = p.capital ORDER BY random() LIMIT 3;').fetchall()
                                m=[miasto2,miasto3,miasto4]
                m.append(miasto)
                random.shuffle(m)
                x=m.index(miasto)
                string = "Stolica panstwa '{} jest miasto:\n1. '{}\n2. '{}\n3. '{}\n4. '{}\n"
                pytanie=string.format(panstwo,m[0],m[1],m[2],m[3])
                odpowiedz = raw_input(pytanie)
                try:
                        if int(odpowiedz) == x+1:
                                pkt+=1
        
                        else:
                                pkt+=0
        
                except ValueError:
                        bledy+=1
                        print bledy
                        
        print u'Trafiles/as ', pkt,'/5'    
        return pkt

def wynik(gra,pkt):
	teraz=t.datetime.now()
	teraz=str(teraz)
	cur.execute('INSERT INTO wyniki_quizu VALUES(?,?,?);',(gra,pkt,teraz))
	conn.commit()

        

con = sqlite3.connect('zad1.db')
cur = con.cursor()
create_table()
conn = sqlite3.connect('World.db')
c = conn.cursor()


if __name__ == '__main__':
	try:
		if argv[1]=='reset':
			cur.execute('''drop table if exists wyniki_quizu''')
			con.commit()
		elif argv[1]=='wyniki':
			dane=cur.execute('select wyniki from wyniki_quizu order by data').fetchall()
			if len(dane)==0:
				print u'brak wyników'
			elif len(dane)==1:
                                print 'srednia w seri ', dane[0][0], '/5'
                        else:
				#print dane
				for i in xrange(len(dane)):
                                        print 'srednia w seri ', i+1,':', dane[i][0], '/5'         


	except IndexError:
		odp='t'
		gra=0
		while odp=='t':
			gra+=1
			pkt=pytania()
			wynik(gra,pkt)
			con.commit()
			odp=raw_input('Czy grasz dalej? (t/n)')

    
conn.close()
con.close()
