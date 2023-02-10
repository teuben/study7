#!/usr/bin/env python
from flask import Flask, render_template, request
import sqlite3 as sql
from astroquery.admit import ADMIT, ADMIT_FORM_KEYS
from astroquery.alma import Alma, tapsql
from astropy.coordinates import SkyCoord
from astropy import units as u
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth',25)
cols_to_exclude = ['id','project_abstract','obs_title','fcoverage','science_keyword']


app = Flask(__name__)
db = "../query/admit.db"    
a = ADMIT(db,check_same_thread=False)
columns_to_show = ['obs_id','target_name','s_ra','s_dec','obs_title','proposal_authors','freqc','vlsr','bmaj']

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search', methods=['POST','GET'])
def search():
    #a.check()
    if request.method == 'POST':
      search_kwargs = dict()
      try:
         if request.form['obs_id'] != '':
             search_kwargs['alma_id'] = request.form['obs_id']
         if request.form['target_name'] != '':
             search_kwargs['source_name_alma'] = request.form['target_name']
         s_ra = request.form['s_ra']
         s_dec = request.form['s_dec']
         radius = request.form['radius']
         c = None
         if s_ra != '' and s_dec != '' and radius != '':
             c = SkyCoord(s_ra,s_dec,frame='icrs')
             size = float(radius)*u.arcsec
             search_kwargs['region'] = [c,size]
         print(search_kwargs)
         result = a.query(**search_kwargs)
         length=len(result)
         msg = result.to_html(columns=columns_to_show)
         
      except Exception as e:
         msg = "Got Exception : %s"%str(e)
      
      finally:
         return render_template("result.html",length=length,msg = msg)
         #con.close()

if __name__ == "__main__":
    app.run(debug = True)

