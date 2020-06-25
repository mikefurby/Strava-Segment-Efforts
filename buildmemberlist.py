#!/usr/bin/python
#Version 19.1
import csv
import json
import requests
import time

vsccTokenFile=("/home/ubuntu/Strava/vscc/tokenfiles/strava_tokens.csv")
ycfTokenFile=("/home/ubuntu/Strava/ycf/tokenfiles/strava_tokens.csv")
inputvs3l=("/home/ubuntu/vs3l/divisionsvs3l.csv")

vsccmembers=  ("/home/ubuntu/vscc/input/membersdiv.csv")
ycfmembers=   ("/home/ubuntu/ycf/input/membersdiv.csv")
vs3lmembers=  ("/home/ubuntu/vs3l/input/membersdiv.csv")
vsvlmembers=  ("/home/ubuntu/vsvl/input/membersdiv.csv")
grimpmembers= ("/home/ubuntu/grimpeur/input/membersdiv.csv")
appmembers=   ("/home/ubuntu/apps/input/membersdiv.csv")
ttmembers=    ("/home/ubuntu/vscctt/input/membersdiv.csv")
tcmembers=    ("/home/ubuntu/vstc/input/membersdiv.csv")
acmembers=    ("/home/ubuntu/vstc/input/membersdiv.csv")

clubvscc = "68829"
clubycf = "11111"
clubvs3l = "115367"
clubvsvl = "115367"
clubgrimpeur = "185097"
clubvsccapp = "547520"
clubvscctt = "597519"
clubvstc = "105940"
clubvsac = "23520"

fvscc = open(vsccmembers, 'w')
fycf = open(ycfmembers, 'w')
fvs3l = open(vs3lmembers, 'w')
fvsvl = open(vsvlmembers, 'w')
fgrimp = open(grimpmembers, 'w')
fapp = open(appmembers, 'w')
ftt = open(ttmembers, 'w')
fvstc = open(tcmembers, 'w')
fvsac = open(acmembers, 'w')

with open(vsccTokenFile) as read_token_file:
  token_list = csv.DictReader(read_token_file)
  for athlete in token_list:
      athleteid = athlete['id']
      firstname = athlete['firstname']
      lastname = athlete['lastname']
      athletetoken = athlete['access_token']
      tokenexpiry = athlete['token_expiry']
      avatar = athlete['avatar']
      athletesex= athlete['sex']
      clubs = athlete['clubs']
      premium = athlete['premium']
      athleteurl=('https://www.strava.com/athletes/' + athleteid)

#####read in the vs3l supplementary file
      vs3ldiv="3"
      agegroup=""
      handicap="100"
      if (athletesex) == "F":
          handicap="112"
      with open(inputvs3l) as read_vs3linput:
          vs3l_data = csv.reader(read_vs3linput, delimiter=',')
          for memberrow in vs3l_data:
            vs3lathleteid=memberrow[0]
            if vs3lathleteid == athleteid:
              vs3ldiv=memberrow[2]
              agegroup=memberrow[3]
###strings for vs3l and then all other clubs
      nondivathleteinfostring=(str(athleteid) + ',' + str(firstname) + ',' + str(lastname) + ',' + str(avatar) + ',' + str(athletese
x) + ',' + str(athleteurl) + ',' + str(athletetoken) + ',' + str(tokenexpiry) + ',' + '1' + ',' + str(handicap) + ',' + str(agegroup
) + ',' + str(premium) + ',')
      vs3lathleteinfostring=(str(athleteid) + ',' + str(firstname) + ',' + str(lastname) + ',' + str(avatar) + ',' + str(athletesex)
 + ',' + str(athleteurl) + ',' + str(athletetoken) + ',' + str(tokenexpiry) + ',' + str(vs3ldiv) + ',' + str(handicap) + ',' + str(a
gegroup) + ',' + str(premium) + ',')

      print (vs3lathleteinfostring)
      print (clubs)
####now write the memberlist files.
      if (clubvscc) in (clubs):
            fvscc.write(vs3lathleteinfostring + '\n')
            print ("hit: VSCC")
      if (clubvs3l) in (clubs):
            fvs3l.write(vs3lathleteinfostring + '\n')
            print ("hit: VS3L")
      if (clubvsvl) in (clubs):
            fvsvl.write(nondivathleteinfostring + '\n')
            print ("hit: VSVL")
      if (clubgrimpeur) in (clubs):
            fgrimp.write(nondivathleteinfostring + '\n')
            print ("hit: grimpeur")
      if (clubvsccapp) in (clubs):
            fapp.write(nondivathleteinfostring + '\n')
            fvscc.write(vs3lathleteinfostring + '\n')
            print ("hit: app club")
      if (clubvscctt) in (clubs):
            ftt.write(nondivathleteinfostring + '\n')
            print ("hit: VSCCTT")
      if (clubvstc) in (clubs):
            fvstc.write(nondivathleteinfostring + '\n')
            print ("hit: VSTC")
      if (clubvscc) not in (clubs):
        if (clubvsac) not in (clubs):
          if (clubvsccapp) not in (clubs):
            if (clubvs3l) in (clubs):
              pass
            else: 
              fycf.write(nondivathleteinfostring + '\n')
              print ("hit: YCF")

fvscc.close()
fvs3l.close()
fvsvl.close()
fgrimp.close()
fapp.close()
ftt.close()
fvstc.close()
#not closing ycf here, deal with that next.....
fvsac.close()

with open(ycfTokenFile) as read_token_file:
  token_list = csv.DictReader(read_token_file)
  for athlete in token_list:
      athleteid = athlete['id']
      firstname = athlete['firstname']
      lastname = athlete['lastname']
      athletetoken = athlete['access_token']
      tokenexpiry = athlete['token_expiry']
      avatar = athlete['avatar']
      athletesex= athlete['sex']
      clubs = athlete['clubs']
      premium = athlete['premium']
      athleteurl=('https://www.strava.com/athletes/' + athleteid)
      div="1"
      agegroup=""
      handicap="100"
      if (athletesex) == "F":
          handicap="112"
      nondivathleteinfostring=(str(athleteid) + ',' + str(firstname) + ',' + str(lastname) + ',' + str(avatar) + ',' + str(athletese
x) + ',' + str(athleteurl) + ',' + str(athletetoken) + ',' + str(tokenexpiry) + ',' + str(div) + ',' + str(handicap) + ',' + str(age
group) + ',' + str(premium) + ',')
      fycf.write(nondivathleteinfostring + '\n')

fycf.close()
