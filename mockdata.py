#! /usr/bin/env python
#
#

import sqlite3
from sqlite3 import Error




def create_connection(db_file):
    
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# --------------------------------------------------------------------------------
#  if a new field is added to a table:
#     1. CREATE TABLE needs new one
#     2. create_XXX() needs new INSERT line
#     3. where create_XXX() is called, needs a new one
#

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

def create_alma(conn, entry):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO alma(id,proposal_id,object,ra,dec)
                        VALUES(?, ?,          ?,     ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid

def add_alma(conn, entry):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO alma(proposal_id,object,ra,dec)
                        VALUES(?,          ?,     ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid

# --------------------------------------------------------------------------------

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

def create_spw(conn, entry):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO spw(id, alma_id, spw, nlines, nchan)
                       VALUES(?,  ?,       ?,   ?,      ?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid

# --------------------------------------------------------------------------------


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

def create_lines(conn, entry):
    """
    Create a new project into the lines table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO lines(id, spw_id, transition, velocity, start_chan, end_chan, nsources)
                         VALUES(?,  ?,      ?,          ?,        ?,          ?,        ?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid

# --------------------------------------------------------------------------------

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

def create_sources(conn, entry):
    """
    Create a new project into the sources table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO sources(id, lines_id, ra, dec, size, peak, flux, snr)
                           VALUES(?,  ?,        ?,  ?,   ?,    ?,    ?,    ?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid

def main():
    database = "mockdata.db"

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn,    alma_table)
        create_table(conn,     spw_table)
        create_table(conn,   lines_table)
        create_table(conn, sources_table)
    else:
        print("Error! cannot create the database connection.")

def work():
    """ now insert some data in db
    """
    database = "mockdata.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # mode: 0=unknown   1=alma  2=spw  3=lines 4=sources
        mode = 0
        lines = open('mockdata.txt').readlines()
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
                id = create_alma(conn,  (int(w[0]), w[1], w[2], float(w[3]), float(w[4])))
            elif mode==2:
                print(mode,'>>',line)
                id = create_spw(conn,  (int(w[0]), int(w[1]), int(w[2]), int(w[3]), int(w[4])))                
            elif mode==3:
                print(mode,'>>',line)
                id = create_lines(conn,  (int(w[0]), int(w[1]), w[2], float(w[3]), int(w[4]), int(w[5]), int(w[6])))
            elif mode==4:
                print(mode,'>>',line)
                id = create_sources(conn,  (int(w[0]), int(w[1]), float(w[2]), float(w[3]), float(w[4]), float(w[5]), float(w[6]), float(w[7])))
def work2():
    """ now insert some more data in db
    """
    database = "mockdata.db"

    # create a database connection
    conn = create_connection(database)
    id = add_alma(conn, ("2022.3.0001.A",   "NGC5678",    20.0,  -20.0))
    print('new',id)
                                    

if __name__ == '__main__':
    main()
    work()
    work2()
    print("Wrote mockdata.db")
