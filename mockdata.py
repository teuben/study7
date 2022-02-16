#! /usr/bin/env python
#
#
#  import some mockdata into a MockData
#  see mocktable.txt for a sample
#

import sqlite3
from sqlite3 import Error

# --------------------------------------------------------------------------------
#  if a new field is added to a table:
#     1. CREATE TABLE needs new one
#     2. create_XXX() needs new INSERT line
#     3. where create_XXX() is called, needs a new one
# --------------------------------------------------------------------------------

alma_table = """
CREATE TABLE IF NOT EXISTS alma (
	id integer PRIMARY KEY,
        proposal_id text NOT NULL,
        object text NOT NULL,
        ra FLOAT,
        dec FLOAT
);
"""

spw_table = """
CREATE TABLE IF NOT EXISTS spw (
	id integer PRIMARY KEY,
	alma_id INTEGER NOT NULL,
	spw INTEGER,
	nlines INTEGER,
        nchan INTEGER,
	FOREIGN KEY (alma_id) REFERENCES alma (id)
);
"""

lines_table = """
CREATE TABLE IF NOT EXISTS lines (
	id integer PRIMARY KEY,
        spw_id INTEGER NOT NULL,
        transition text NOT NULL,
        velocity FLOAT,
        start_chan INTEGER,
        end_chan INTEGER,
        nsources INTEGER,
	FOREIGN KEY (spw_id) REFERENCES spw (id)
);
"""

sources_table = """
CREATE TABLE IF NOT EXISTS sources (
	id integer PRIMARY KEY,
        lines_id INTEGER NOT NULL,
        ra FLOAT,
        dec FLOAT,
        size FLOAT,
        peak FLOAT,
        flux FLOAT,
        snr FLOAT,
	FOREIGN KEY (lines_id) REFERENCES lines (id)
);
"""


class MockData(object):
    """
    This is a simplified A-W-L-S table design for study7
    """
    def __init__(self, db_file):
        self.db   = db_file
        self.conn = None

        # create_connection
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        # create tables
        if self.conn is not None:
            self.create_table(   alma_table)
            self.create_table(    spw_table)
            self.create_table(  lines_table)
            self.create_table(sources_table)
        else:
            print("Error! cannot create the database connection.")
            

    def create_table(self, create_table_sql):
        """
        create a table from the create_table_sql statement
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)


    def create_alma(self, entry):
        """
        Create a new project into the alma table
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO alma(id,proposal_id,object,ra,dec)
                            VALUES(?, ?,          ?,     ?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, entry)
        self.conn.commit()
        return cur.lastrowid

    def add_alma(self, entry):
        """
        Add a new project into the alma table
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO alma(proposal_id,object,ra,dec)
                            VALUES(?,          ?,     ?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, entry)
        self.conn.commit()
        return cur.lastrowid



    def create_spw(self, entry):
        """
        Create a new project into the spw table
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO spw(id, alma_id, spw, nlines, nchan)
                           VALUES(?,  ?,       ?,   ?,      ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, entry)
        self.conn.commit()
        return cur.lastrowid



    def create_lines(self, entry):
        """
        Create a new project into the lines table
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO lines(id, spw_id, transition, velocity, start_chan, end_chan, nsources)
                             VALUES(?,  ?,      ?,          ?,        ?,          ?,        ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, entry)
        self.conn.commit()
        return cur.lastrowid


    def create_sources(self, entry):
        """
        Create a new project into the sources table
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO sources(id, lines_id, ra, dec, size, peak, flux, snr)
                               VALUES(?,  ?,        ?,  ?,   ?,    ?,    ?,    ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, entry)
        self.conn.commit()
        return cur.lastrowid


    def work1(self, txt_file):
        """
        now insert some data in db from a mock txt_file
        """
        with self.conn:
            # mode: 0=unknown   1=alma  2=spw  3=lines 4=sources
            mode = 0
            lines = open(txt_file).readlines()
            print("Found %d lines" % len(lines))
            for line in lines:
                line = line.strip()
                if line[:2] == '##': continue
                w = line.split()
                if w[0] == '#':
                    if   w[1] == 'alma':     mode=1
                    elif w[1] == 'spw':      mode=2
                    elif w[1] == 'lines':    mode=3
                    elif w[1] == 'sources':  mode=4
                    else:
                        print("mode %s not supported" % w[1])
                    continue
                if mode==1:
                    print(mode,'>>',line)
                    id = self.create_alma((int(w[0]), w[1], w[2], float(w[3]), float(w[4])))
                elif mode==2:
                    print(mode,'>>',line)
                    id = self.create_spw((int(w[0]), int(w[1]), int(w[2]), int(w[3]), int(w[4])))                
                elif mode==3:
                    print(mode,'>>',line)
                    id = self.create_lines((int(w[0]), int(w[1]), w[2], float(w[3]), int(w[4]), int(w[5]), int(w[6])))
                elif mode==4:
                    print(mode,'>>',line)
                    id = self.create_sources((int(w[0]), int(w[1]), float(w[2]), float(w[3]), float(w[4]), float(w[5]), float(w[6]), float(w[7])))


    def work2(self):
        """ now add some new data in the db
        """

        id = self.add_alma(("2022.3.0001.A",   "NGC5678",    20.0,  -20.0))
        print('new',id)
                                    

if __name__ == '__main__':
    md = MockData('mockdata.db')
    md.work1('mockdata.txt')
    md.work2()
