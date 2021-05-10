#! /usr/bin/python
# coding: utf8
#Urszula Romaniuk

import sqlite3
import matplotlib.pyplot as py
import numpy as np

full='hocl-ge2017-results-full.csv'
summary='hocl-ge2017-results-summary.csv'
BAZA='wybory.db'

SCHEMA = {
    'KRAJ': '''
        create table KRAJ (
            ID integer primary key,
            NAZWA text UNIQUE
            
        )''',
    'REGION': '''
        create table REGION (
            ONS_region_ID text primary key,
            NAZWA text,
            KRAJ_ID int references KRAJ
        )''',
    'OKREGI_WYBORCZE': '''
        create table OKREGI_WYBORCZE (
            ONS_ID text primary key,            
            NAZWA text,
            TYP text,
			DECLARATON_TIME text NOT NULL,
            ELEKTORATE int NOT NULL,
            VALID_VOTES int NOT NULL,
            INVALID_VOTES int NOT NULL,
            ONS_REGION_ID text references REGION
        )''',
    'PARTIE':'''
        create table PARTIE(
            ID integer primary key,
            PARTY_NAME text UNIQUE,
            PARTY_ABBREVIATION text
        )''',
    'KANDYDACI':'''
        create table KANDYDACI(
			ID integer primary key,
            FIRSTNAME text,
            SURNAME text,
            GENDER text,
            SITTING_MP text,
            FORMER_MP text,
            VOTES int,
            PARTY_ID int references PARTIE,
            ONS_ID text references OKREGI_WYBORCZE
        )'''
            
}


QUERY= (u'''SELECT p.PARTY_NAME AS partia,
       count(p.PARTY_NAME) as ilosc,
       o.nazwa AS okreg
  FROM OKREGI_WYBORCZE o
       JOIN
       KANDYDACI k ON o.ONS_ID = k.ONS_ID
       JOIN
       PARTIE p ON k.PARTY_ID = p.ID
 WHERE votes = (
                   SELECT max(votes) 
                     FROM KANDYDACI kd
                          JOIN
                          OKREGI_WYBORCZE ow ON ow.ONS_ID = kd.ONS_ID
                    WHERE ow.nazwa = okreg
               )
 GROUP BY partia
 ORDER BY ilosc DESC;''',

'''SELECT  (max(k.votes) * 100) / (o.valid_votes * 1) as procenty,
       o.nazwa AS okreg
  FROM okregi_wyborcze o
       JOIN
       kandydaci k ON o.ONS_ID = k.ONS_ID
       JOIN
       PARTIE p ON k.PARTY_ID = p.ID
 GROUP BY okreg
''')


def create_db(db):
    for table in SCHEMA:
        db.execute('drop table if exists {}'.format(table))
    for ddl in SCHEMA.values():
        db.execute(ddl)


def get_rows(filename):
    from csv import reader
    with open(filename) as f:
        rows = reader(f)
        rows.next()
        for row in rows:
            cursor.execute('''
            INSERT OR IGNORE INTO KRAJ (NAZWA) VALUES (?)
            ''', (row[5],) )
            zapytanie = cursor.execute("SELECT ID FROM KRAJ WHERE KRAJ.NAZWA = '{}'".format(row[5])).fetchone()
            cursor.execute('''
            INSERT OR IGNORE INTO REGION VALUES (?, ?, ?)
            ''', (row[1], row[4], zapytanie[0] ))
            cursor.execute('''
            INSERT OR IGNORE INTO OKREGI_WYBORCZE VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row[0], row[2], row[6], row[7], row[11], row[12], row[13], row[1]) )


        
def get_rows2(filename):
    from csv import reader
    with open(filename) as f:
        rows = reader(f)
        rows.next()
        for row in rows:
            cursor.execute('''
            INSERT OR IGNORE INTO PARTIE (PARTY_NAME, PARTY_ABBREVIATION) VALUES (?, ?)
            ''', row[7:9] )
            
            zapytanie = cursor.execute('''SELECT ID FROM PARTIE WHERE PARTIE.PARTY_NAME = "{}" '''.format(row[7])).fetchone()
            cursor.execute('''
            INSERT INTO KANDYDACI (FIRSTNAME, SURNAME, GENDER, SITTING_MP, FORMER_MP, VOTES, PARTY_ID, ONS_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row[9], row[10], row[11], row[12], row[13], row[14], zapytanie[0], row[0]) )
            


if __name__ == '__main__':
    from sys import argv
    from sqlite3 import connect
    try:
        filename = argv[1]
        filename2 = argv[2]
    except IndexError:
        exit('argumentem ma byc nazwa pliku csv. Argument1:  ' + summary + ' Argument2:  ' + full)

    with sqlite3.connect(BAZA) as db:
        cursor = db.cursor()
        create_db(cursor)
        get_rows(filename)
        get_rows2(filename2)

    with sqlite3.connect(BAZA) as db:
        for tab in SCHEMA:
            (n,) = db.execute('select count(*) from {}'.format(tab)).fetchone()
            print u'Tabela {}: wstawiono {} rekordów'.encode('utf8').format(tab, n)

    with sqlite3.connect(BAZA) as db:
        cursor=db.cursor()
        cursor.execute(QUERY[0])
        colnames = [r[0] for r in cursor.description]
        print
        print "Wynik zapytania"
        print '=' * 32
        print '{:26}|{:3}'.format(colnames[0],colnames[1])
        print '-' * 32
        for row in cursor:
            print '{:26}|{:3}'.format(row[0],row[1])
        print '=' * 32

    with sqlite3.connect(BAZA) as db:
        cursor=db.cursor()
        cursor.execute(QUERY[1])
        L=[]
        for row in cursor:
            L.append(row[0])
        bins = np.linspace(0, 100, 21)
        py.hist(L,bins)
        py.title("Histogram")
        py.xlabel(u"procent uzyskanych głosów [%]")
        py.ylabel(u"rozkład liczby wygrywających kandydatów")
        py.show()
