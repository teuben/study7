#! /usr/bin/env python
#
#
#  import admit_study7.log as "admit" (L/W/S)
#  import admit_sq.log     as "alma"  (A)
#
#  Warning:  there isn't a lot of sanity checking if that data is properly structured
#            re-entering same data will enter it twice

import os, sys
import sqlite3
from sqlite3 import Error

# --------------------------------------------------------------------------------
#  if a new field is added to a table:
#     1. CREATE TABLE needs new one
#     2. create_XXX() needs new INSERT line
#     3. where create_XXX() is called, needs a new one
# --------------------------------------------------------------------------------

header_table = """
CREATE TABLE IF NOT EXISTS header (
    id integer PRIMARY KEY,
        key text NOT NULL,
        val text NOT NULL
);
"""

alma_table = """
CREATE TABLE IF NOT EXISTS alma (
    id integer PRIMARY KEY,
        obs_id text NOT NULL,
        target_name text NOT NULL,
        s_ra FLOAT,
        s_dec FLOAT,
        frequency FLOAT
);
"""

win_table = """
CREATE TABLE IF NOT EXISTS win (
    id integer PRIMARY KEY,
    a_id INTEGER NOT NULL,
    freqc FLOAT,
    freqw FLOAT,
    vlsr FLOAT,
    nlines INTEGER,
    nsources INTEGER,
    nchan INTEGER,
    rms FLOAT,
    bmaj FLOAT,
    bmin FLOAT,
    bpa FLOAT,
    fcoverage FLOAT,
    FOREIGN KEY (a_id) REFERENCES alma (id)
);
"""

cont_table = """
CREATE TABLE IF NOT EXISTS cont (
    id integer PRIMARY KEY,
    a_id INTEGER NOT NULL,
    cont text NOT NULL,
    nsources INTEGER,
    FOREIGN KEY (a_id) REFERENCES alma (id)
);
"""

lines_table = """
CREATE TABLE IF NOT EXISTS lines (
    id integer PRIMARY KEY,
    w_id INTEGER NOT NULL,
    formula text NOT NULL,
    transition text NOT NULL,
    restfreq FLOAT, 
    vmin FLOAT,
    vmax FLOAT,
    mom0flux FLOAT,
    mom1peak FLOAT,
    mom2peak FLOAT,
    FOREIGN KEY (w_id) REFERENCES win (id)
);
"""

sources_table = """
CREATE TABLE IF NOT EXISTS sources (
    id integer PRIMARY KEY,
    w_id INTEGER NOT NULL,
    l_id INTEGER,
    ra FLOAT,
    dec FLOAT,
    peak FLOAT,
    flux FLOAT,
    smaj FLOAT,
    smin FLOAT,
    spa FLOAT,
    snr FLOAT,
    FOREIGN KEY (w_id) REFERENCES win (id),
    FOREIGN KEY (l_id) REFERENCES lines (id)
);
"""

class AdmitData(object):
    """
    This is the A-W-L-S table design for study7
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
            self.create_table( header_table)
            self.create_table(   alma_table)
            self.create_table(    win_table)
            self.create_table(   cont_table)
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


    def create_header(self, entry):
        """
        Create a new project into the header table
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO header(key,val)
                              VALUES(?,  ?)'''
        cur = self.conn.cursor()
        cur.execute(sql, entry)
        self.conn.commit()
        return cur.lastrowid
    

    def create_alma(self, entry):
        """
        Create a new project into the alma table
        :param project:
        :return: project id
        obs_id == member_ous_uid
        """
        sql = ''' INSERT INTO alma(obs_id, target_name, s_ra, s_dec, frequency)
                            VALUES(?,      ?,           ?,    ?,     ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, entry)
        self.conn.commit()
        return cur.lastrowid
    

    def create_win(self, entry):
        """
        Create a new project into the win table
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO win(a_id,freqc,freqw,vlsr,nlines,nsources,nchan,rms,bmaj,bmin,bpa,fcoverage)
                           VALUES(?,   ?,    ?,    ?,   ?,     ?,       ?,    ?,  ?,   ?,   ?,  ?) '''
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
        sql = ''' INSERT INTO lines(w_id,formula,transition,restfreq,vmin,vmax,mom0flux,mom1peak,mom2peak)
                             VALUES(?,   ?,      ?,         ?,       ?,   ?,   ?,       ?,       ?) '''
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
        sql = ''' INSERT INTO sources(w_id,l_id,ra,dec,peak,flux,smaj,smin,spa,snr)
                               VALUES(?,   ?,   ?, ?,  ?,   ?,   ?,   ?,   ?,  ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, entry)
        self.conn.commit()
        return cur.lastrowid


    def add_study7(self, dir_name, dryrun=False):
        """
        now insert some data in db from 


        @todo   dryrun should be run first to ensure the data are consistent
        """

        log_study7 = dir_name + '/admit_study7.log'
        log_aq     = dir_name + '/admit_aq.log'
        if not os.path.exists(log_study7):
            print("Warning: no %s" % log_study7)
            return 
        if not os.path.exists(log_aq):
            print("Warning: no %s" % log_aq)
            return

        
        with self.conn:
            # read the "aq" log for A table
            lines = open(log_aq).readlines()
            print("%d lines %s" % (len(lines),log_aq))
            a={}
            for line in lines:
                if line[0] == '#': continue
                x = line.split()
                a[x[0]] = ' '.join(x[1:])
            a_id = self.create_alma((a['obs_id'], a['target_name'], float(a['s_ra']), float(a['s_dec']), float(a['frequency'])))
            alma = a
            
            
            a = {}
            # read the "study7" log for the W/L/S
            mode = 0
            s_stack = []
            lines = open(log_study7).readlines()
            print("%d lines %s" % (len(lines),log_study7))
            S=[]
            L=[]
            for line in lines:
                line = line.strip()
                if len(line) == 0: continue
                if line[0] == '#': continue
                x = line.split()

                if len(x[0]) > 1:
                    a[x[0]] = x[1]
                    continue

                if x[0] == 'L':  L.append(x[1:])
                if x[0] == 'S':  S.append(x[1:])
                    
            nsources = int(a['nsources'])
            nlines = int(a['nlines'])

            if len(L) != nlines:
                print("Warning: len(L),nlines = %d,%d not the same" % (nlines,len(L)))
                
            w_id = self.create_win((a_id,
                                    float(a['freqc']),
                                    float(a['freqw']),
                                    float(a['vlsr']),
                                    int(a['nlines']),
                                    int(a['nsources']),
                                    int(a['nchan']),
                                    float(a['rms']),
                                    float(a['bmaj']),
                                    float(a['bmin']),
                                    float(a['bpa']),
                                    float(a['fcoverage'])
            ))

            l_stack = []
            for iL in range(nlines):
                l_id = self.create_lines((w_id,
                                          L[iL][0],
                                          L[iL][1],
                                          float(L[iL][2]),
                                          float(L[iL][3]),
                                          float(L[iL][4]),
                                          0.0,
                                          0.0,
                                          0.0
                ))
                l_stack.append(l_id)

            s_stack = []
            for iS in range(nsources):
                s_id = self.create_sources((w_id,
                                            0,
                                            float(S[iS][0]),
                                            float(S[iS][1]),
                                            float(S[iS][2]),
                                            float(S[iS][3]),
                                            float(S[iS][4]),
                                            float(S[iS][5]),
                                            float(S[iS][6]),
                                            float(S[iS][7])
                ))
                s_stack.append(s_id)
            if len(S) < nsources:
                print("Warning: not enough Sources from CubeSum - very unusual")
            elif len(S) == nsources:
                print("Warning: no LineCube sources given, it seems")
            elif len(S) < nsources*(nlines+1):
                print("Warning: not enough LineCube sources given, it seems")
            elif len(S) > nsources*(nlines+1):
                print("Warning: too many LineCube sources given, it seems")
            
                


if __name__ == '__main__':
    db_name = 'admit.db'
    if len(sys.argv) == 1:
        print("Usage: %s admit_dir(s)" % sys.argv[0])
        print("Will write/append to %s" % db_name)
        sys.exit(0)
    md = AdmitData(db_name)
    for dir in sys.argv[1:]:
        md.add_study7(dir)
    print("Warning:  Don't run on the same data twice")
    print("Data written/appended to %s" % db_name)
