#!/usr/bin/python

import json
import numpy as np
import csv
import sys

jsonFile = sys.argv[1]
csvFile = sys.argv[2]



data = ''
with open(jsonFile) as dataFile:
  data = json.load(dataFile)


def dist(a, b):
  d= 0.
  for x in range(0, len(a)): 
    d = d + (a[x] -b[x])^2
  return d^(1/2)

def findPlayer(id, players):
  for x in range(0, len(players)-1):
    if id == players[int(x)][1]:
      return int(x)

events = data['events']
shotat = 0.02
mademiss = 1
basket1 = np.array([5.25, 25])
basket2 = np.array([88.75, 25])

#basket1 = np.array([25, 5.25])
#basket2 = np.array([25, 88.75])

# features to be captured:
#gameclock = 0
#shotclock = 0
shooter_x = 0
shooter_y = 0
nearest_def_x = 0
nearest_def_y = 0
min_distance_def = 94

# Files:
pos = 'pos'
neg = 'neg'
pos_f = open(pos, 'a')
neg_f = open(neg, 'a')
#quarter = 1
dups = set()
with open(csvFile, 'rb') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  for row in spamreader:
    shotat = float(row[2][0:1])*60 + int(row[2][3:4])
    #print "shot: " + str(shotat)
    mademiss = int(row[4])

    event_ind = int(row[0])
    #print "Event: " + str(event_ind) + "\tResult: " + str(mademiss)
    #print events[event_ind]['eventId']
    minimum_distance = 0
    shooterid = int(row[1])
    shooterteam =0
    moment_ind = 0
    #print event_ind, len(events)
    moments = None
    for e in events:
        if(event_ind == int(e['eventId'])):
          moments = e['moments']
          break;
    '''
    if(int(events[event_ind - 1]['eventId']) == event_ind ):
      moments = events[event_ind - 1]['moments']
    else:
      for e in reversed(events):
        if(event_ind == int(e['eventId'])):
          moments = events[event_ind - 1]['moments']
          break;
    '''
    #print len(moments)

    for moment in moments:
      players = moment[5]
      shooter = 1
      moment_ind +=1
      #print players[shooter]
      #print players[5][1]
      while(shooter < 11 and shooterid != players[shooter][1]): shooter= shooter+1

      if(shooter == 11):
        print "Couldn't find shooter"
        continue 
      shooterteam = players[shooter][0]
      ball = np.array([ players[0][2], players[0][3], players[0][4] ] )
      #time = float(moment[2])  #int(moment[2])
      shooterPt = np.array([ players[shooter][2], players[shooter][3], players[shooter][4] ])
      #find appropriate moment
      balldist = np.linalg.norm( np.array([ ball[0], ball[1] ]) - np.array([ shooterPt[0], shooterPt[1] ]) )
      if( 7.9 < ball[2] <  8.9 and  balldist <= 5.5):
        # Distance from the nearest defender
        
        min_distance_def = 94.
        nearestdefender = shooterPt  # just placeholding
        adjust = 0
        gameclock = moment[2] # Record the gameclock
        shotclock = moment[3] # Record the shot clock
        print "shot clock: " + str(shotclock) + ", " + str(gameclock)
        print "found right moment"
 
        for p in range (1,11):
          defender = np.array([players[p][2], players[p][3], players[p][4]])
          curDist = np.linalg.norm(shooterPt - defender)
          if(players[p][0] != shooterteam and curDist < min_distance_def):
            min_distance_def = curDist
            nearestdefender = defender
        
        # Distance from basket
        dist_from_basket = 94.
        xyball = np.array([ball[0], ball[1]])
        #print moments[moment_ind - 2][5][0]
        try:
          prev_ball_pos = moments[moment_ind + 40][5][0]
        except IndexError:
        #moments2 = events[event_ind - 2]['moments']
        #prev_ball_pos = moments2[len(moments2) -3][5][0]
          prev_ball_pos = players[0]
        xyballprev = np.array([prev_ball_pos[2], prev_ball_pos[3]])
        shooter_x = shooterPt[0]
        shooter_y = shooterPt[1]
        #print xyballprev
        dist_basket1_this =  np.linalg.norm(xyball - basket1)
        dist_basket1_prev =  np.linalg.norm(xyballprev - basket1)
        if(dist_basket1_prev < dist_basket1_this): # moving towards this basket
          dist_from_basket = np.linalg.norm(np.array([shooter_x, shooter_y]) - basket1)
        else:
          dist_from_basket = np.linalg.norm(np.array([shooter_x, shooter_y]) - basket2) 
        if(np.linalg.norm(xyball - xyballprev) == 0): dist_from_basket = 24.0
          # Compute min time
        min_time = 24.
        #print "shot clock: " +str(min_time) + " "+ str(shotclock) + ", " + str(gameclock)
        try: 
          min_time = float(shotclock)
          #print "shot clock: " +str(min_time) + shotclock + ", " + gameclock
        except TypeError:
          if(str(gameclock) != None):
            min_time = float(gameclock)
        if(dist_from_basket >= 42.1 and min_time >=5.2):
          dist_from_basket = 24.5
          min_distance_def = 7.7
 
        if(mademiss == 1):
          line = str(min_time) + ' ' + str(dist_from_basket) + ' ' + str(min_distance_def)
          if line not in dups:
            pos_f.write(line)
            pos_f.write('\n')
            dups.add(line)
        else:
          line = str(min_time) + ' ' + str(dist_from_basket) + ' ' + str(min_distance_def)
          if line not in dups:
            neg_f.write(line)
            neg_f.write('\n')
            dups.add(line)
        break
        moment_ind = moment_ind + 1
      #event_ind = event_ind + 1
      #un hide for a sample, else the program runs for ALL data and will take a while
      #break
pos_f.close()
neg_f.close()

