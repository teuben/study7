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
from astropy.time import Time
import argparse as ap

version = '24-feb-2022'

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
        obs_id              text NOT NULL,
        target_name         text NOT NULL,
        s_ra                FLOAT,
        s_dec               FLOAT,
        frequency           FLOAT,
        t_min               FLOAT, 
        project_abstract    text NOT NULL,
        obs_title           text NOT NULL,
        science_keyword     text NOT NULL,
        scientific_category text NOT NULL,
        proposal_authors    text NOT NULL
);
"""

win_table = """
CREATE TABLE IF NOT EXISTS win (
    id integer PRIMARY KEY,
    a_id INTEGER NOT NULL,
    spw TEXT,
    freqc FLOAT,
    freqw FLOAT,
    vlsr FLOAT,
    nlines INTEGER,
    nsources INTEGER,
    nchan INTEGER,
    peak_w FLOAT,
    rms_w FLOAT,
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
    w_id          INTEGER NOT NULL,
    formula       text NOT NULL,
    transition    text NOT NULL,
    restfreq      FLOAT, 
    vmin          FLOAT,
    vmax          FLOAT,
    mom0flux      FLOAT,
    mom1peak      FLOAT,
    mom2peak      FLOAT,
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
    peak_s FLOAT,
    flux FLOAT,
    smaj FLOAT,
    smin FLOAT,
    spa FLOAT,
    snr_s FLOAT,
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
            self.create_table(  lines_table)
            self.create_table(sources_table)
            # self.create_table(   cont_table)
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
        sql = ''' INSERT INTO alma(obs_id, target_name, s_ra, s_dec, frequency, t_min, project_abstract, obs_title, science_keyword, scientific_category,  proposal_authors)
                            VALUES(?,      ?,           ?,    ?,     ?,         ?,     ?,                 ?,         ?,               ?,                    ?) '''
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
        sql = ''' INSERT INTO win(a_id,spw,freqc,freqw,vlsr,nlines,nsources,nchan,peak_w,rms_w,bmaj,bmin,bpa,fcoverage)
                           VALUES(?,   ?,  ?,    ?,    ?,   ?,     ?,       ?,    ?,     ?,    ?,   ?,   ?,  ?) '''
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
        sql = ''' INSERT INTO sources(w_id,l_id,ra,dec,peak_s,flux,smaj,smin,spa,snr_s)
                               VALUES(?,   ?,   ?, ?,  ?,     ?,   ?,   ?,   ?,  ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, entry)
        self.conn.commit()
        return cur.lastrowid


    def add_study7(self, dir_name, dryrun=False, aq=True, debug=False):
        """
        now insert some data in db from 


        @todo   dryrun should be run first to ensure the data are consistent
        """

        log_study7 = dir_name + '/admit_study7.log'
        log_aq     = dir_name + '/admit_aq.log'
        if not os.path.exists(log_study7):
            print("Warning: no %s" % log_study7)
            return 0
        if not os.path.exists(log_aq):
            print("Warning: no %s" % log_aq)
            return 0

        
        with self.conn:
            # write some history
            h_id = self.create_header(('version',version))
            # read the "aq" log for A table
            lines = open(log_aq).readlines()
            if len(lines) < 20:
                print("short %d lines %s" % (len(lines),log_aq))
            a={}
            for line in lines:
                line = line.strip()
                if len(line) == 0: continue
                if not aq and line[:11] == '# </backup>':
                    # @todo   not supported yet;  t_min is needed, and it's not in the backup
                    #         remaining keywords also not in backup
                    # date_obs    2018-01-05T10:02:40.272001
                    # t_min       58123.420166 - 58123.445496
                    t = Time(a['date_obs'])
                    a['t_min'] = t.mjd
                    a['proposal_abstract'] = '-'
                    a['obs_title'] = '-'
                    a['science_keyword'] = 'cal'
                    a['scientific_category'] = 'cal'
                    a['proposal_authors'] = 'cal'
                    break
                if line[0] == '#': continue
                x = line.split()
                a[x[0]] = ' '.join(x[1:])
            if 'obs_id' in a:
                a_id = self.create_alma((a['obs_id'], a['target_name'], float(a['s_ra']),
                                         float(a['s_dec']), float(a['frequency']), float(a['t_min']),
                                         a['proposal_abstract'], a['obs_title'], a['science_keyword'],
                                         a['scientific_category'], a['proposal_authors']))
            else:
                print("Warning: entering a dummy alma record")
                a_id = self.create_alma(('dummy', 'dummy', 0.0, 0.0, 10.0, 5000.0, 'dummy', 'dummy', 'dummy', 'dummy', 'dummy'))

            # big cheat
            if 'spw' in a:
                spw = a['spw']
            else:
                spw = '???'
            alma = a

            a = {}
            # read the "study7" log for the W/L/S
            mode = 0
            s_stack = []
            lines = open(log_study7).readlines()
            if len(lines) < 20:
                print("short %d lines %s" % (len(lines),log_study7))
            S=[]
            L=[]
            for line in lines:
                line = line.strip()
                if len(line) == 0: continue
                if line[0] == '#': continue
                x = line.split()

                if len(x[0]) > 1:
                    a[x[0]] = ' '.join(x[1:])
                    continue

                if x[0] == 'L':  L.append(x[1:])
                if x[0] == 'S':  S.append(x[1:])
                    
            nsources = int(a['nsources'])
            nlines = int(a['nlines'])

            if len(L) != nlines:
                print("Warning: len(L),nlines = %d,%d not the same" % (nlines,len(L)))
                
            w_id = self.create_win((a_id,
                                    spw,
                                    float(a['freqc']),
                                    float(a['freqw']),
                                    float(a['vlsr']),
                                    int(a['nlines']),
                                    int(a['nsources']),
                                    int(a['nchan']),
                                    float(a['peak']),
                                    float(a['rms']),
                                    float(a['bmaj']),
                                    float(a['bmin']),
                                    float(a['bpa']),
                                    float(a['fcoverage'])
            ))

            l_stack = []
            for iL in range(nlines):
                mom_key = 'L_%s_%s' % (L[iL][0],L[iL][2])
                if mom_key in a:
                    mom0flux = a[mom_key].split()[0]
                    mom1peak = a[mom_key].split()[1]
                    mom2peak = a[mom_key].split()[2]
                else:
                    mom0flux = 0.0
                    mom1peak = 0.0
                    mom2peak = 0.0

                l_id = self.create_lines((w_id,
                                          L[iL][0],
                                          L[iL][1],
                                          float(L[iL][2]),
                                          float(L[iL][3]),
                                          float(L[iL][4]),
                                          mom0flux,
                                          mom1peak,
                                          mom2peak
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

            if debug:
                print("Found %s sources in CubeSum and %d lines in Cube" % (nsources,nlines))
                print("Found %d sources in CubeSum and LineCube's" % len(S))

            if len(S) == nsources*(nlines+1):
                for iL in range(nlines):
                    l_id = l_stack.pop(0)
                    for iS in range(nsources):
                        iSL = iS + (iL+1)*nsources
                        s_id = self.create_sources((w_id,
                                                    l_id,
                                                    float(S[iSL][0]),
                                                    float(S[iSL][1]),
                                                    float(S[iSL][2]),
                                                    float(S[iSL][3]),
                                                    float(S[iSL][4]),
                                                    float(S[iSL][5]),
                                                    float(S[iSL][6]),
                                                    float(S[iSL][7])
                        ))
            else:
                print("Warning: not the right number of sources")
            return 1


# @todo need an option to ignore the admit_aq, e.g. for calibrators it overwrites target_name, s_ra, s_dec        

#
#   -d db_name
#   -c            treat like calibrator
#

if __name__ == '__main__':
    db_name = 'admit.db'
    qa = True

    parser = ap.ArgumentParser(description='Ingest study7 admit projects in a A/W/L/S database')
    parser.add_argument('-d','--db_name'  ,nargs=1, help='Database file [admit.db]')
    parser.add_argument('-c','--cal'      ,action='store_true', help='Special cheat for calibrators')
    parser.add_argument('--version', action='version', version='%(prog)s ' + version)
    parser.add_argument('admit_dirs', nargs='*')
    try:
        args = vars(parser.parse_args())
    except:
        sys.exit(1)

    db_name = args['db_name'][0]
    aq = not args['cal']
    if not aq:
        print("Warning: special calibrator treatment for %s" % db_name)

    
    md = AdmitData(db_name)
    nadd = 0
    for ddir in args['admit_dirs']:
        nadd = nadd + md.add_study7(ddir, aq=aq)
    print("Added %d / %d admit results" % (nadd,len(args['admit_dirs'])))
