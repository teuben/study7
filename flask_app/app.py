#------------------------------------------------
#       Keyword                      Description               Database Table
#--------------------- --------------------------------------- --------------
#------------------------------------------------

from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
import sqlite3 as sql
from astroquery.admit import ADMIT, ADMIT_FORM_KEYS
from astroquery.alma import Alma, tapsql
from astropy.coordinates import SkyCoord
from astropy import units as u
import pandas as pd
from copy import deepcopy
from operator import itemgetter

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth',25)
cols_to_exclude = ['id','project_abstract','obs_title','fcoverage','science_keyword']


app = Flask(__name__)
# made up key. it's an md5 hash of "LMT DATABASE SEARCH"
app.secret_key = "864feb319aa38d67b46f40f657442192"
#app.config['SECRET_KEY'] = "864feb319aa38d67b46f40f657442192"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "null"
#app.config['SESSION_PERMANENT']= False
Session(app)
#db = "example_lmt.db"    
db = "/lma/www/html/lmtsearch/study7/flask_app/example_lmt.db"    
a = ADMIT(db,check_same_thread=False)

@app.route('/')
def home():
    return render_template('search.html')


@app.route('/download', methods=['POST','GET'])
def download():
    if request.method == 'POST':
        selected = request.form.getlist('selectedData')
        rows = [int(q) for q in selected]

        obsnum = session['result'].iloc[rows]['obsnum']
        print(obsnum)
        return render_template('download.html',selected=rows,obsnum=obsnum.values)
    
@app.route('/search', methods=['POST','GET'])
def search():
    #a.check()
    columns_to_show = ['Select','obsnum','target_name','s_ra','s_dec','instrument','obs_title','obs_creator_name','freqc','vlsr','calibration_status' ]
    length = 0
    backendlink="https://dp.lmtgtm.org/dataverse/lmtdata/?q=obsnum%3A"
    if request.method == 'POST':
      search_kwargs = request.form.to_dict()
      try:
         s_ra = search_kwargs.pop('s_ra','')
         s_dec = search_kwargs.pop('s_dec','')
         radius = search_kwargs.pop('radius','')
         c = None
         #NB this does not allow "give me everything at a certain RA". oh well.
         if s_ra != '' and s_dec != ''  and radius != '':
             c = SkyCoord(s_ra,s_dec,frame='icrs')
             print('SKY COORD: ',c)
             size = float(radius)*u.arcsec
             search_kwargs['target_region'] = [c,size]
         #remove items with blank values
         # https://stackoverflow.com/questions/12118695/efficient-way-to-remove-keys-with-empty-strings-from-a-dict
         sknew =  dict(filter(itemgetter(1), search_kwargs.items()))
         print(sknew)
         session['result'] = a.query(**sknew)
         result=deepcopy(session['result'])
         print("COLUMNS ",result.columns)
         length=len(result)
         if 'formula' in result.columns:
            columns_to_show.append('formula')
         if 'transition' in result.columns:
            columns_to_show.append('transition')
         # replace UID with alma archive link to UID
         i = 0
         for v in result['obsnum']:
            result.loc[i,'obsnum'] = f'<a href="{backendlink}{v}">{v}</a>'
            i = i+1
         checkbox = []
         for i in range(len(result.index)):
            # value of checkbox will be dataframe row number
            checkbox.append(f'<input class="form-check-input" type="checkbox" value="{i}" id="defaultCheck{i}" name="selectedData">')
         result['Select'] = checkbox
         msg = result.to_html(classes=['table', 'table-striped','table-bordered','text-end'],columns=columns_to_show,escape=False)
         
      except Exception as e:
         msg = "Got Exception : %s"%str(e)
      
      finally:
         return render_template("result.html",length=length,msg = msg)
         #con.close()

def searchALMA():
    #a.check()
    columns_to_show = ['obs_id','target_name','s_ra','s_dec','obs_title','proposal_authors','freqc','vlsr', 'nchan']
    length = 0
    almalink = "https://almascience.nrao.edu/aq/?result_view=observations&observationsProjectCode="
    if request.method == 'POST':
      search_kwargs = request.form.to_dict()
      try:
         s_ra = search_kwargs.pop('s_ra','')
         s_dec = search_kwargs.pop('s_dec','')
         radius = search_kwargs.pop('radius','')
         c = None
         #NB this does not allow "give me everything at a certain RA". oh well.
         if s_ra != '' and s_dec != ''  and radius != '':
             c = SkyCoord(s_ra,s_dec,frame='icrs')
             size = float(radius)*u.arcsec
             search_kwargs['region'] = [c,size]
         #remove items with blank values
         # https://stackoverflow.com/questions/12118695/efficient-way-to-remove-keys-with-empty-strings-from-a-dict
         sknew =  dict(filter(itemgetter(1), search_kwargs.items()))
         print(sknew)
         result = a.query(**sknew)
         print("COLUMNS ",result.columns)
         length=len(result)
         if 'formula' in result.columns:
            print("adding formula")
            columns_to_show.append('formula')
         if 'transition' in result.columns:
            print("adding columns")
            columns_to_show.append('transition')
         # replace UID with alma archive link to UID
         i = 0
         for v in result['obs_id']:
            result.loc[i,'obs_id'] = f'<a href="{almalink}{v}">{v}</a>'
            i = i+1
         msg = result.to_html(classes=['table', 'table-striped'],columns=columns_to_show,escape=False)
         
      except Exception as e:
         msg = "Got Exception : %s"%str(e)
      
      finally:
         return render_template("result.html",length=length,msg = msg)
         #con.close()


if __name__ == "__main__":
    app.run(debug = True)

