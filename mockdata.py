#! /usr/bin/env python
#
#
#  import some mockdata into a MockData
#  see mocktable.txt for a sample
#
#  Warning:  there isn't a lot of sanity checking if that data is properly structured

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
        proposal text NOT NULL,
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
	nsources INTEGER,
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
	FOREIGN KEY (spw_id) REFERENCES spw (id)
);
"""

sources_table = """
CREATE TABLE IF NOT EXISTS sources (
	id integer PRIMARY KEY,
        spw_id INTEGER NOT NULL,
        lines_id INTEGER,
        ra FLOAT,
        dec FLOAT,
        flux FLOAT,
	FOREIGN KEY (spw_id) REFERENCES spw (id)
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
        sql = ''' INSERT INTO alma(proposal,object,ra,dec)
                            VALUES(?,       ?,     ?, ?) '''
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
        sql = ''' INSERT INTO alma(proposal,object,ra,dec)
                            VALUES(?,       ?,     ?, ?) '''
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
        sql = ''' INSERT INTO spw(alma_id, spw, nlines, nsources, nchan)
                           VALUES(?,       ?,   ?,      ?,        ?) '''
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
        sql = ''' INSERT INTO lines(spw_id, transition, velocity, start_chan, end_chan)
                             VALUES(?,      ?,          ?,        ?,          ?) '''
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
        sql = ''' INSERT INTO sources(spw_id, lines_id, ra, dec, flux)
                               VALUES(?,      ?,        ?,  ?,   ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, entry)
        self.conn.commit()
        return cur.lastrowid


    def mock(self, txt_file, dryrun=False):
        """
        now insert some data in db from a mock txt_file
        this is V2 of the mock format

        @todo   dryrun should be run first to ensure the data are consistent
        """
        with self.conn:
            mode = 0
            s_stack = []
            lines = open(txt_file).readlines()
            print("Found %d lines" % len(lines))
            for line in lines:
                line = line.strip()
                if len(line) == 0: continue
                if line[0] == '#': continue
                w = line.split()
                print('>>',line)
                
                if   w[0] == 'A': mode=1
                elif w[0] == 'W': mode=2
                elif w[0] == 'L': mode=3
                elif w[0] == 'S': mode=4
                else:
                    print("mode %s not supported - skipping line" % w[0])
                    continue

                if mode==1:
                    if len(s_stack) > 0:
                        print("there is a source stack left")
                    a_id = self.create_alma((w[1], w[2], float(w[3]), float(w[4])))
                    w_id = l_id = s_id = 0
                elif mode==2:
                    nl = int(w[2])
                    ns = int(w[3])
                    w_id = self.create_spw((a_id, int(w[1]), nl, ns, int(w[4])))
                    s_stack = []
                    for i in range(ns):  s_stack.append(0)
                elif mode==3:
                    l_id = self.create_lines((w_id, w[1], float(w[2]), int(w[3]), int(w[4])))
                    for i in range(ns):  s_stack.append(l_id)
                elif mode==4:
                    if len(s_stack) > 0:
                        l_id = s_stack.pop(0)
                        s_id = self.create_sources((w_id, l_id, float(w[1]), float(w[2]), float(w[3])))
                    else:
                        print("no stack left for another source; skipping")
                else:
                    print("should never get here")

if __name__ == '__main__':
    md = MockData('mockdata.db')
    md.mock('mockdata.txt')
    print("Wrote mockdata.db")