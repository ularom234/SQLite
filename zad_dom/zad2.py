import csv
BAZA = 'ZAD2.db'
from sqlite3 import connect
from sys import argv
from csv import reader

O = '''CREATE TABLE OKREGI (
    NR_OKREGU INT PRIMARY KEY,
    SIEDZIBA_OKW TEXT,
    LICZABA_WYBORCOW     INT
);'''

L= '''CREATE TABLE LISTY (
    NR INT PRIMARY KEY, --REFERENCES OKREGI 
    PARTIE TEXT
);'''
W= '''CREATE TABLE WYNIKI (
    NR_OKREGU INT PRIMARY KEY,  --REFERENCES OKREGI,
    GLOSY_WAZNE INT,
    GLOSY_NIEWAZNE INT,
    PiS INT,
    PO INT,
    Partia_Razem INT,
    KORWiN INT,
    PSL INT,
    Zjednoczona_Lewica_SLD_TR_PPS_UP_Zieloni INT,
    Kukiz15 INT,
    Nowoczesna_Ryszarda_Petru INT,
    JOW_Bezpartyjni INT,
    Zbigniew_Stonoga INT,
    RSRP INT,
    Zjednoczeni_dla_slaska INT,
    Samoobrona INT,
    Grzegorz_Brauna INT,
    Kongres_Nowej_Prawicy INT,
    Mniejszosc_Niemiecka INT,
    Obywatele_do_Parlamentu INT
);'''




def popliku(plik):
        plik=reader(plik,delimiter=',')
        n=0
        for linia in plik:
                if n==0:
                        nazwy=linia[6::]
                        for i in xrange(len(nazwy)):
                                p=unicode(nazwy[i].decode('utf-8'))
                                db.execute('insert into LISTY values(?,?);',(i+1,p))
                        n=1
                else:
                        n=unicode(linia[0].decode('utf-8'))
                        s=unicode(linia[1].decode('utf-8'))
                        l=unicode(linia[3].decode('utf-8'))
                        #db.execute("insert into WYNIKI('NR_OKREGU') values(?);",(n,))
                        db.execute('insert into OKREGI values(?,?,?);',(n,s,l))
                        r=linia[4::]
                        r.append(n)
                        for i in xrange(len(r)):
                                if r[i]=='':
                                        r[i]=None
                                
                        napis="insert into WYNIKI('GLOSY_WAZNE','GLOSY_NIEWAZNE','PiS','PO','Partia_Razem','KORWiN','PSL','Zjednoczona_Lewica_SLD_TR_PPS_UP_Zieloni','Kukiz15','Nowoczesna_Ryszarda_Petru','JOW_Bezpartyjni','Zbigniew_Stonoga','RSRP','Zjednoczeni_dla_slaska','Samoobrona','Grzegorz_Brauna','Kongres_Nowej_Prawicy','Mniejszosc_Niemiecka','Obywatele_do_Parlamentu','NR_OKREGU') values({})".format(','.join('?'*20))
                        db.execute(napis,tuple(r))


#plik='2015-gl-lis-okr.csv'
                        
if __name__ == '__main__':
        with connect(BAZA) as db: 
                db.execute('drop table if exists OKREGI')
                db.execute(O)
                db.execute('drop table if exists LISTY')
                db.execute(L)
                db.execute('drop table if exists WYNIKI')
                db.execute(W)
                with open(argv[1]) as plik:
                        popliku(plik)                                                            
                db.commit()
                
        with connect(BAZA) as db:
                (n,) = db.execute('select count(*) from OKREGI').fetchone()
                (n2,) = db.execute('select count(*) from LISTY').fetchone()
                (n3,) = db.execute('select count(*) from WYNIKI').fetchone()
        print 'wstawiono do tabeli OKREGI {} wierszy'.format(n)
        print 'wstawiono do tabeli LISTY {} wierszy'.format(n2)
        print 'wstawiono do tabeli WYNIKI {} wierszy'.format(n3)


