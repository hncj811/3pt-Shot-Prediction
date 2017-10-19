#!/usr/bin/python

import json
import numpy as np
import csv
import sys
import re
import os
#from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool

from os import listdir
from os.path import isfile, join

files = [f for f in listdir('/home/nvishwa/DataClean') if isfile(join('/home/nvishwa/DataClean', f))]

jsons = list()
csvs = list()

for x in files:
  if(re.match('.+\.json', x)):
    jsons.append(x)
  elif(re.match('[A-Z][A-Z][A-Z]\_[A-Z][A-Z][A-Z]\.csv', x)):
    csvs.append(x)
#print jsons
#print '\n'
#print csvs

stmts = list()

for x in jsons:
  jtokens = x.split('.')
  jteam1 = jtokens[3]
  jteam2 = jtokens[5]
  for y in csvs:
    ctokens = y.split('_')
    cteam1 = ctokens[0]
    cteam2 = ctokens[1]
    if( ''.join(sorted(jteam1 + jteam2)) == ''.join(sorted(cteam1 + cteam2)) ):
      jsonFile = x
      csvFile = y
      quarter = ctokens[5][0:1]
      #print jsonFile, csvFile, quarter
      stmt = 'python prepare.py ' + jsonFile + ' ' + csvFile
      print 'Added ', stmt
      stmts.append(stmt)
      #os.system(stmt)
#pool = Pool(16)

#pool.map(os.system, stmts)

#pool.close()
#pool.join()

