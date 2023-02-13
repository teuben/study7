#!/usr/bin/env python
#------------------------------------------------
#       Keyword                      Description               Database Table
#--------------------- --------------------------------------- --------------
#              alma_id                                 ALMA ID         Window
#               win_id                      Spectral window ID         Window
#                  spw                    Spectral window name         Window
#               nlines                         Number of lines         Window
#             nsources                       Number of sources         Window
#                nchan                      Number of channels         Window
#             win_peak                        Window peak flux         Window
#              win_rms                        Window RMS noise         Window
#              win_snr Window Signal to noise ratio (peak/rms)         Window
#                 bmaj                         Beam major axis         Window
#                 bmin                         Beam minor axis         Window
#                  bpa                                 Beam PA         Window
#                freqc                  Frequency center (GHz)         Window
#                freqw                   Frequency width (GHz)         Window
#                 vlsr                     LSR Velocity (km/s)         Window
#            fcoverage                     Frequency coverage?         Window
#             l_win_id                   Spectral window ID(L)          Lines
#             restfreq                          Rest frequency          Lines
#              formula                                 Formula          Lines
#           transition                              Transition          Lines
#             velocity                                Velocity          Lines
#                 vmin                        Minimum velocity          Lines
#                 vmax                        Maximum velocity          Lines
#             mom0flux                        Moment zero flux          Lines
#             mom1peak                         Moment one peak          Lines
#             mom2peak                  Moment two peak (km/s)          Lines
#             s_win_id                   Spectral Window ID(S)        Sources
#             lines_id                                 Line ID        Sources
#                   ra                            RA (Degrees)        Sources
#                  dec                           Dec (Degrees)        Sources
#                 flux                                    Flux        Sources
#           source_snr            Source Signal to noise ratio        Sources
#          source_peak                        Source Peak flux        Sources
#                 smaj                       Source major axis        Sources
#                 smin                       Source minor axis        Sources
#                  spa                               Source PA        Sources
#               region                           Search Region        Sources
#           header_key                                     Key         Header
#           header_val                                   Value         Header
#               obs_id                             Observation           Alma
# source_name_resolver          Source name (astropy Resolver)           Alma
#     source_name_alma                      Source name (ALMA)           Alma
#               ra_dec                    RA Dec (Sexagesimal)           Alma
#             galactic                      Galactic (Degrees)           Alma
#   spatial_resolution             Angular resolution (arcsec)           Alma
#    spatial_scale_max          Largest angular scale (arcsec)           Alma
#                  fov                  Field of view (arcsec)           Alma
#            frequency                         Frequency (GHz)           Alma
#            bandwidth                          Bandwidth (Hz)           Alma
#  spectral_resolution               Spectral resolution (KHz)           Alma
#            band_list                                    Band           Alma
#           start_date                        Observation date           Alma
#     integration_time                    Integration time (s)           Alma
#    polarisation_type  Polarisation type (Single, Dual, Full)           Alma
#     line_sensitivity   Line sensitivity (10 km/s) (mJy/beam)           Alma
#continuum_sensitivity        Continuum sensitivity (mJy/beam)           Alma
#         water_vapour                       Water vapour (mm)           Alma
#         project_code                            Project code           Alma
#       project_title                           Project title           Alma
#              pi_name                                 PI name           Alma
#     proposal_authors                        Proposal authors           Alma
#     project_abstract                        Project abstract           Alma
#    publication_count                       Publication count           Alma
#      science_keyword                         Science keyword           Alma
#  scientific_category                     Scientific category           Alma
#              bibcode                                 Bibcode           Alma
#            pub_title                                   Title           Alma
#         first_author                            First author           Alma
#              authors                                 Authors           Alma
#         pub_abstract                                Abstract           Alma
#     publication_year                                    Year           Alma
#------------------------------------------------

from flask import Flask, render_template, request
import sqlite3 as sql
from astroquery.admit import ADMIT, ADMIT_FORM_KEYS
from astroquery.alma import Alma, tapsql
from astropy.coordinates import SkyCoord
from astropy import units as u
import pandas as pd
#from copy import deepcopy
from operator import itemgetter

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth',25)
cols_to_exclude = ['id','project_abstract','obs_title','fcoverage','science_keyword']


app = Flask(__name__)
db = "../query/admit.db"    
a = ADMIT(db,check_same_thread=False)
columns_to_show = ['obs_id','target_name','s_ra','s_dec','obs_title','proposal_authors','freqc','vlsr','formula','transition']

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search', methods=['POST','GET'])
def search():
    #a.check()
    length = 0
    if request.method == 'POST':
      search_kwargs = request.form.to_dict()
      try:
         s_ra = request.form['s_ra']
         s_dec = request.form['s_dec']
         radius = search_kwargs.pop('radius',None)
         c = None
         if s_ra != '' and s_dec != '' and radius != '':
             c = SkyCoord(s_ra,s_dec,frame='icrs')
             size = float(radius)*u.arcsec
             search_kwargs['region'] = [c,size]
         #remove items with blank values
         # https://stackoverflow.com/questions/12118695/efficient-way-to-remove-keys-with-empty-strings-from-a-dict
         sknew =  dict(filter(itemgetter(1), search_kwargs.items()))
         print(sknew)
         result = a.query(**sknew)
         length=len(result)
         msg = result.to_html(columns=columns_to_show)
         
      except Exception as e:
         msg = "Got Exception : %s"%str(e)
      
      finally:
         return render_template("result.html",length=length,msg = msg)
         #con.close()

if __name__ == "__main__":
    app.run(debug = True)

