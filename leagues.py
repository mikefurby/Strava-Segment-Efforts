#!/usr/bin/python
import csv
from sys import argv
import os
import datetime
from datetime import date
import pprint

script, club = argv

path=("/home/ubuntu/")
memberlist=(path + club + "/input/membersdiv.csv")
segmentsummary=(path + club + "/input/segmentsummary.csv")
initfile=(path + club + "/initfile.csv")
seglist=(path + club + "/segmentlist.csv")

def htmltables2(divcsv,divhtm):
    with open(divcsv) as r:
        row = csv.reader(r, delimiter=',')
        fdtemp = open("temp.htm", 'w')
        fdh = open(divhtm, 'w')
        fdtemp.write('<table border="1" width="50%">\n')
        fdtemp.write("<a href='javascript:toggleInfo()'>Toggle segment scores</a>\n")
        for element in row:
            fdtemp.write('<tr><td>')
            fdtemp.write('</td><td>'.join(element))
            fdtemp.write('</td></tr>\n')
        fdtemp.write('</table>\n')
        fdtemp.close()
    with open("temp.htm") as r2:
        row2 = csv.reader(r2, delimiter='!')
        for element2 in row2:
            fdh.write("</td><td name='segmentinfo'>".join(element2))
            fdh.write('\n')
        fdh.close()
    if os.path.exists("temp.htm"):
        os.remove("temp.htm")

def readinitfile():
    with open(initfile) as initread:
        initstring = csv.reader(initread)
        for element in initstring:
            Year=element[1]
            Seas=element[3]
            Fort=element[5]
    return (Year,Seas,Fort)

def readseglist():
    MaxSegments=0
    with open(seglist) as r:
        initstring = csv.reader(r)
        for element in initstring:
            MaxSegments+=1
    MaxSegments-=1
    return (MaxSegments)

#This reads the archived div files for the year and takes the segment score by each athlete and adds to a league score file
def leaguetable(athleteid,div,outfile):
#    print (athleteid,div,outfile)
    outfile.write(athleteid)
    FortnightCounter=0
    while (FortnightCounter) != (MaxFortnights):
        FortnightCounter+=1
        SegCounter=0
        while (SegCounter) != (MaxSegments):
            check=0
            SegCounter+=1
            divfile=(path + club + '/archive/' + Year + Seas + str(FortnightCounter) + 'div' + str(div) + "_seg" + str(SegCounter) +
 '.csv')
            try:
              with open (divfile) as f:
                effort = csv.reader(f)
                for element in effort:
                    segscore=(element[0])
#                    komscore=(element[8])
#                    qomscore=(element[9])
                    aurl=element[2]
                    athid2pre=aurl.split("/")[4]
                    athid2=athid2pre.split('"')[0]
                    if (athid2) == (athleteid):
                        outfile.write(',' + segscore) #This is just taking the first value from the divfile which is segscore
                        check=1
              if (check)==0:
                outfile.write(',0') #This is just taking the first value from the divfile which is segscore
            except:
              pass
    outfile.write('\n')

#######MAIN#######
initdata = readinitfile()
segdata = readseglist()
Year=initdata[0]
Seas=initdata[1]
Fort=initdata[2]
MaxSegments=segdata
#print (Year,Seas,Fort)
MaxFortnights=int(Fort)

athletedict = {}
with open(memberlist) as read_memberlist:
    member = csv.reader(read_memberlist, delimiter=',')
    for row in member:
        athlete=row[0]
        athletedict[athlete] = {}
        athletedict[athlete]["first"] = row[1] 
        athletedict[athlete]["last"] = row[2] 
        athletedict[athlete]["avatar"] = row[3] 
        athletedict[athlete]["sex"] = row[4] 
        athletedict[athlete]["url"] = row[5] 
        athletedict[athlete]["token"] = row[6] 
        athletedict[athlete]["tokenexpiry"] = row[7] 
        athletedict[athlete]["div"] = row[8] 
        athletedict[athlete]["hcap"] = row[9] 
        athletedict[athlete]["cat"] = row[10] 
        athletedict[athlete]["total_elevation"] = 0.0 
        athletedict[athlete]["grimp_badge1"] = ""
        athletedict[athlete]["grimp_badge2"] = ""
        athletedict[athlete]["grimp_badge3"] = ""
        athletedict[athlete]["climbcount1"]=0
        athletedict[athlete]["y1climbcount1"]=0
        athletedict[athlete]["y2climbcount1"]=0
        athletedict[athlete]["y3climbcount1"]=0
        athletedict[athlete]["y4climbcount1"]=0
        athletedict[athlete]["climbcount2"]=0
        athletedict[athlete]["climbcount3"]=0
        athletedict[athlete]["allclimb"]=0
        segmentindex=0
        with open (segmentsummary) as read_segments:
            segments = csv.DictReader(read_segments)
            for segment in segments:
                elev=float(segment['elevation'])
                segefforts=(path + club + "/efforts/segmentefforts_concise_" + str(segmentindex+1) + ".csv")
                athletedict[athlete][segmentindex] = {}
                athletedict[athlete][segmentindex]["Segment_Reps"] = 0
                with open (segefforts) as read_efforts:
                    efforts = csv.reader(read_efforts)
                    for effort in efforts:
                        athleteid2=effort[1]
                        if (athlete) == (athleteid2):
                            athletedict[athleteid2][segmentindex]["Segment_Reps"] += 1
                            athletedict[athlete]["total_elevation"] += elev 
                if (athletedict[athlete][segmentindex]["Segment_Reps"]) >= 1:
                    athletedict[athlete]["climbcount1"]+=1
                    if segmentindex+1>0 and segmentindex+1 <21:
                        athletedict[athlete]["y1climbcount1"]+=1
                    elif segmentindex+1>20 and segmentindex+1 <41:
                        athletedict[athlete]["y2climbcount1"]+=1
                    elif segmentindex+1>40 and segmentindex+1 <61:
                        athletedict[athlete]["y3climbcount1"]+=1
                    elif segmentindex+1>60 and segmentindex+1 <81:
                        athletedict[athlete]["y4climbcount1"]+=1
                if (athletedict[athlete][segmentindex]["Segment_Reps"]) >= 2:
                    athletedict[athlete]["climbcount2"]+=1
                if (athletedict[athlete][segmentindex]["Segment_Reps"]) >= 3:
                    athletedict[athlete]["climbcount3"]+=1
                if (athletedict[athlete]["climbcount1"])==20:
                    athletedict[athlete]["allclimb"]=1000
                segmentindex+=1
        athletedict[athlete]["grimp_badge1"] = ""
        athletedict[athlete]["grimp_badge2"] = ""
        athletedict[athlete]["grimp_badge3"] = ""
        athletedict[athlete]["completion_bonus"]=0
        if athletedict[athlete]["climbcount1"]>19:
            athletedict[athlete]["grimp_badge1"] =("/grimpeur/grimpeur.jpg")
            athletedict[athlete]["completion_bonus"]=1000
            if athletedict[athlete]["climbcount2"]>19:
                athletedict[athlete]["grimp_badge2"] =("/grimpeur/grimpeur.jpg")
                if athletedict[athlete]["climbcount3"]>19:
                    athletedict[athlete]["grimp_badge3"] =("/grimpeur/grimpeur.jpg")
                else:
                    athletedict[athlete]["grimp_badge3"] =("/badges/" + str(athletedict[athlete]["climbcount3"]) + "climbs.jpg")
            else:
                athletedict[athlete]["grimp_badge2"] =("/badges/" + str(athletedict[athlete]["climbcount2"]) + "climbs.jpg")
        else:
            athletedict[athlete]["grimp_badge1"] =("/badges/" + str(athletedict[athlete]["climbcount1"]) + "climbs.jpg")

        athletedict[athlete]["grimp_badge_yoy"] = ""
        stars=0
        if athletedict[athlete]["y1climbcount1"]==20:
            stars+=1
        if athletedict[athlete]["y2climbcount1"]==20:
            stars+=1
        if athletedict[athlete]["y3climbcount1"]==20:
            stars+=1
        if athletedict[athlete]["y4climbcount1"]==20:
            stars+=1
        yoybadge=("/badges/yoy" + str(stars) + ".jpg")
        athletedict[athlete]["grimp_badge_yoy"] = yoybadge
        elevtotal=(athletedict[athlete]["total_elevation"]) 
        if (elevtotal)==0:
            mountaingif="/grimpeur/0m.gif"
        elif elevtotal>0 and elevtotal<85:
            mountaingif="/grimpeur/0m.gif"
        elif elevtotal>84 and elevtotal<288 :
            mountaingif="/grimpeur/storith.gif"
        elif elevtotal>287 and elevtotal<978 :
            mountaingif="/grimpeur/greenhow.gif"
        elif elevtotal>977 and elevtotal<1345 :
            mountaingif="/grimpeur/scafell_pike.gif"
        elif elevtotal>1344 and elevtotal<1912 :
            mountaingif="/grimpeur/ben_nevis.gif"
        elif elevtotal>1911 and elevtotal<3150 :
            mountaingif="/grimpeur/mont_ventoux.gif"
        elif elevtotal>3149 and elevtotal<4810 :
            mountaingif="/grimpeur/altodeletras.gif"
        elif elevtotal>4809 and elevtotal<8848 :
            mountaingif="/grimpeur/mont_blanc.gif"
        elif elevtotal>8847 and elevtotal<10200 :
            mountaingif="/grimpeur/everest.gif"
        elif elevtotal>10199 and elevtotal<21230 :
            mountaingif="/grimpeur/mauna_kea.gif"
        else:
            mountaingif="/grimpeur/olympus_mons.gif"
        athletedict[athlete]["mountain_gif"]=(mountaingif) 

        totalreps=0
        prcount=0
        inaday=0
        inaday2=0
        inadaydate=""
        athefforts=(path + club + "/efforts/riders/segmentefforts_concise_" + str(athlete) + ".csv")
        with open (athefforts) as atheff:
            efforts = csv.reader(atheff)
            for row in efforts:
                inaday2=0
                totalreps+=1
                if row[8]=="1" or row[7]!="None":
                    prcount+=1
                datetimeobject=(datetime.datetime.strptime(row[4],'%Y-%m-%dT%H:%M:%SZ'))
                effdate=datetimeobject.date()
                daycount=(path + club + "/efforts/riders/segmentefforts_concise_" + str(athlete) + ".csv")
                with open(daycount) as dc:
                    for row in dc:
                        if str(effdate) in row:
                            inaday2+=1
                if inaday2 > inaday:
                    inaday=inaday2 
                    inadaydate=effdate
        athletedict[athlete]["in_a_day"] = inaday
        athletedict[athlete]["in_a_day_date"] = inadaydate
        athletedict[athlete]["total_reps"] = totalreps
        athletedict[athlete]["total_prs"] = prcount
        if totalreps > 99:
            athletedict[athlete]["repbadge"]=("/badges/hillreps100.jpg")
        elif totalreps > 74:
            athletedict[athlete]["repbadge"]=("/badges/hillreps75.jpg")
        elif totalreps > 49:
            athletedict[athlete]["repbadge"]=("/badges/hillreps50.jpg")
        elif totalreps > 24:
            athletedict[athlete]["repbadge"]=("/badges/hillreps25.jpg")
        else:
            athletedict[athlete]["repbadge"]=("/grimpeur/0pcgrimpeur.gif")
#pprint.pprint (athletedict)



divnamelist=[]
divheadlist=[]
divstartscores=[]
divtypes=[]
eachdiv=[]
divs=0
divnames=(path + club + "/divnames.txt")
with open((divnames),'r') as f:
     for line in f:
         eachdiv=(line.split(','))
         divs+=1
         divnamelist.append(eachdiv[0])
         divheadlist.append(eachdiv[1])
         divstartscores.append(eachdiv[2])
         divtypes.append(eachdiv[3])
print ("Total Divisions: " + str(divs))
print (divnamelist)

leagues=[]
openlgs=[]
for div in range(divs):
    leagues.append(path + club + '/output/leaguetable' + str(div+1) + '.csv')
    openlgs.append(open(leagues[div],'w'))

#Loop through each athlete and create an entry in the league file for each division with the score that they earned.
#scores out of 10 for the VS3L type, and need kom/qom score table for Grimpeur style
for athleteid in athletedict:
        athlete=athleteid
        print (athlete)
        gender=(athletedict[(athleteid)]["sex"])
        division=(athletedict[(athleteid)]["div"])
        ag=(athletedict[(athleteid)]["cat"])
#        print (division,gender,ag)
        if (division) == "1":#this scores on divscore
            lgfile=openlgs[(int(division)-1)]
        elif (division) == "2":
            lgfile=openlgs[(int(division)-1)]
        elif (division) == "3":
            lgfile=openlgs[(int(division)-1)]
        else:
            division=4
            lgfile=openlgs[(int(division)-1)]
        leaguetable(athlete,division,lgfile)
        if (gender) == 'F':
            division="5"
            lgfile=openlgs[(int(division)-1)]
            leaguetable(athlete,division,lgfile)
        elif (gender) == 'M':
            division="9"
            lgfile=openlgs[(int(division)-1)]
            leaguetable(athlete,division,lgfile)
        if ((ag) == 'V40') or ((ag) == 'V45'):
            division="6"
            lgfile=openlgs[(int(division)-1)]
            leaguetable(athlete,division,lgfile)
        if ((ag) == 'V50') or ((ag) == 'V55') or ((ag) == 'V60'):
            division="7"
            lgfile=openlgs[(int(division)-1)]
            leaguetable(athlete,division,lgfile)
        division="8"#all athletes handicap - this scores on divscore, like all of the above
        lgfile=openlgs[(int(division)-1)]
        leaguetable(athlete,division,lgfile)
        division="10"#all athletes kom - want this to score on komscore
        lgfile=openlgs[(int(division)-1)]
        leaguetable(athlete,division,lgfile)
        division="11"#all men-kom women-qom - want this to score on qomscore
        lgfile=openlgs[(int(division)-1)]
        leaguetable(athlete,division,lgfile)

leaguesfinal=[]
openlgsfinal=[]
for div in range(divs):
    openlgs[div].close()
    leaguesfinal.append(path + club + '/output/leaguefinal' + str(div+1) + '.csv')
    openlgsfinal.append(open(leaguesfinal[div],'w'))

def buildleagues(lgs,lgsfinal,fmo,div):
    print (lgs,lgsfinal,fmo,div)
    with open(lgs) as divscores:
###the scores are being read as strings so use quote.nonnumeric to make them floats, then convert to integers.
        athletescores = csv.reader(divscores, delimiter=',',quoting=csv.QUOTE_NONNUMERIC)
        sc=[]
        sc_unsorted=[]
        for scores in athletescores:
            print (scores)
            iscores=[]
            iscores_unsort=[]
            for score in scores:
                if score=="":
                    score=float(0)
                iscores.append(int(score))
                iscores_unsort.append(int(score))
            athleteid=str(int(scores[0]))
            sc=iscores
            sc_unsorted=iscores_unsort
            sc.remove(iscores[0])#remove athleteid from the list and have the segment scores only so we can sum them
            sc_unsorted.remove(iscores_unsort[0])#remove athleteid from the list and have the segment scores only so we can sum them
            fmo.write((athletedict[athleteid]["first"]) + ' ' + (athletedict[athleteid]["last"]))
            count=0
            entries=0
            for score in sc:
                fmo.write(',' + str(sc[count]))
                count+=1
                if score != 0:
                    entries+=1
            fmo.write('\n')
            sc.sort(reverse=True)#is this the best place to do the sort? only needed for vs3l and top 10 from 12 scores
            warriorbadge=('<img src="/grimpeur/0pcgrimpeur.gif" align="left" height="50px" hspace="5">')
            if (entries >= 6):
              if club == "vs3l":
                warriorbadge=('<img src="/icons/warriorbutton.jpg" height="50px" hspace="5">')
              elif club == "ycf":
                warriorbadge=('<img src="/ycf/ycf.png" height="50px" hspace="5">')

####need to add the top 10 score only piece for vs3l
            topten=0
            if div==9 or div==10:
                scorestocount=80
                bonus=athletedict[athleteid]['completion_bonus']
            else:
                bonus=0
                if club == "ycf":
                    scorestocount=6
                else:
                    scorestocount=10
            count=0
            for eachscore in sc:
                count+=1
                if eachscore=='':
                    eachscore='0'
                if count<=(scorestocount):
                    topten+=int(eachscore)
            topten+=bonus
            first=athletedict[athleteid]['first']
            last=athletedict[athleteid]['last']
            prc=(str(athletedict[athleteid]["total_prs"]) + 'x <img src ="/icons/pr1icon.gif" height="35px">')
            gy=('<img src ="' + athletedict[athleteid]['grimp_badge_yoy'] + '" height="50px">')
            gb1=('<img src ="' + athletedict[athleteid]['grimp_badge1'] + '" height="50px">')
            gb2=('<img src ="' + athletedict[athleteid]['grimp_badge2'] + '" height="50px">')
            gb3=('<img src ="' + athletedict[athleteid]['grimp_badge3'] + '" height="50px">')
            mg=('<img src ="' + athletedict[athleteid]['mountain_gif'] + '" height="50px">')
            rb=('<img src ="' + athletedict[athleteid]['repbadge'] + '" height="35px" width="50px">' + str(athletedict[athleteid]['t
otal_reps']))
            iad=('<img src ="/badges/inaday' + str(athletedict[athleteid]['in_a_day']) + '.jpg" height="50px">')
            url=('<a href="' + athletedict[athleteid]['url'] + '">')
            avatar=('<img src="' + athletedict[athleteid]['avatar'] + '" height="50px">')
            if divtypes[div] == 'v':
                lgsfinal.write(avatar + ',' + url + first + ' ' + last + '</a>,' +  str(topten) + ',' + warriorbadge)
                for eachscore in sc_unsorted:
                    lgsfinal.write('!' + str(eachscore))
                lgsfinal.write('\n')
            elif divtypes[div] == 'g':
                lgsfinal.write(avatar + ',' + url + first + ' ' + last + '</a>,' +  str(topten) + ',' + mg + ',' + gb1 + ',' + gb2 +
 ',' + gb3 + ',' + rb + ',' + iad + ',' + prc)
#                lgsfinal.write(avatar + ',' + url + first + ' ' + last + '</a>,' +  str(topten) + ',' + mg + ',' + gy + ',' + rb + 
',' + iad + ',' + prc)
                lgsfinal.write('\n')

matrices=[]
openmatrix=[]
htmmatrices=[]
for div in range(divs):
    matrices.append(path + club + '/output/matrix' + str(div+1) + '.csv')
    htmmatrices.append(path + club + '/output/matrix' + str(div+1) + '.htm')
    openmatrix.append(open(matrices[div],'w')) #need to close this 
    fm=(matrices[div])
    fmo=(openmatrix[div])
    fmh=(htmmatrices[div])
    fmo.write(",1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20\n")
    buildleagues(leagues[div],openlgsfinal[div],fmo,div)
    fmo.close()
    htmltables2(fm,fmh)

openlsorted=[]
lsorted=[]
for div in range(divs):
    openlgsfinal[div].close()
    lsorted.append(path + club + '/output/leaguetablesorted' + str(div+1) + '.csv')
    openlsorted.append(open(lsorted[div],'w'))


for div in range(divs):
    with open(leaguesfinal[div]) as divscores:
        scores = csv.reader(divscores, delimiter=',')
        sortedscores=sorted(scores,key=lambda row: int(row[2]), reverse=True)
        for effrow in sortedscores:
            openlsorted[div].write(','.join(effrow))
            openlsorted[div].write("\n")

live=[]
openlive=[]
for div in range(divs):
    openlsorted[div].close()
    live.append(path + club + '/output/liveleague' + str(div+1) + '.htm')
    openlive.append(open(live[div],'w'))
    htmltables2(lsorted[div],live[div])

for div in range(divs):
    openlive[div].close()
