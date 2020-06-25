#!/usr/bin/python
import csv
import time
from sys import argv
import pprint
import datetime
from datetime import date
import operator
import shutil
from segfiles import combineEffortFiles

script, club = argv

path=("/home/ubuntu/")
memberlist=(path + club + "/input/membersdiv.csv")
segmentsummary=(path + club + "/input/segmentsummary.csv")
divnames=(path + club + "/divnames.txt")
initfile=(path + club + "/initfile.csv")
athletedict = {}
segmentdict = {}


divnamelist=[]
divheadlist=[]
divstartscores=[]
divtypes=[]
divyn=[]
eachdiv=[]
TotalDivs=0
with open((divnames),'r') as f:
     for line in f:
         eachdiv=(line.split(','))
         TotalDivs+=1
         divnamelist.append(eachdiv[0])
         divheadlist.append(eachdiv[1])
         divstartscores.append(eachdiv[2])
         divtypes.append(eachdiv[3])
         divyn.append(eachdiv[4])


todayunformat=date.today()
today=todayunformat.strftime("%d %b %Y")
uthisweek1=date.today() - datetime.timedelta(days=1)
uthisweek2=date.today() - datetime.timedelta(days=2)
uthisweek3=date.today() - datetime.timedelta(days=3)
uthisweek4=date.today() - datetime.timedelta(days=4)
uthisweek5=date.today() - datetime.timedelta(days=5)
uthisweek6=date.today() - datetime.timedelta(days=6)
uthisweek7=date.today() - datetime.timedelta(days=7)
print today
thisweek1=uthisweek1.strftime("%d %b %Y")
thisweek2=uthisweek2.strftime("%d %b %Y")
thisweek3=uthisweek3.strftime("%d %b %Y")
thisweek4=uthisweek4.strftime("%d %b %Y")
thisweek5=uthisweek5.strftime("%d %b %Y")
thisweek6=uthisweek6.strftime("%d %b %Y")
print thisweek1
print thisweek2
print thisweek3
print thisweek4
print thisweek5
print thisweek6
#this is just comparing two scores, it does look if one if higher or lower, so it works with both low-to-high and high-to-low scorin
g methods
###I think prevscore is unnecessary, I could compare times instead of creating a new set of values to compare
def divscoring(score,prevscore,divscore,fd,effrow):
                    global prevscore_returned
                    global divscore_returned
                    if (divscore>1):
                      if (score == prevscore):
                        fd.write(str(divscore+1) + ",")
                      else:
                        fd.write(str(divscore) + ",")
                    else:
                        fd.write(str(divscore) + ",")
                    fd.write(",".join(effrow))
                    fd.write("\n")
                    divscore-=1
                    prevscore=score
                    if (divscore==0):
                        divscore=1
                    prevscore_returned=prevscore
                    divscore_returned=divscore
                    return prevscore_returned
                    return divscore_returned

#could embed into the divscoring defintion...if I really wanted.
def komscoring(score,prevscore,divscore,fd,effrow):
                    global divscore_returned
                    if (divscore==0):
                      divscore=score
                    fd.write(str(divscore) + ",")
                    fd.write(",".join(effrow))
                    fd.write("\n")
                    divscore_returned=0
                    return divscore_returned

def htmltables(divcsv,divhtm,divname):
    with open(divcsv) as r:
        row = csv.reader(r, delimiter=',')
        fdh = open(divhtm, 'w')
        fdh.write('<h3>%s</h3>\n' % divname)
        fdh.write('<table border="1" width="50%">\n')
        for element in row:
            fdh.write('<tr><td>')
            fdh.write("</td><td>".join(element))
            fdh.write('</td></tr>\n')
        fdh.write('</table>\n')
        fdh.close()

def concat(outfilename):
    with open(outfilename, 'w') as outfile:
        div=0
        for infilename in divhtmlist:
            print divyn[div]
            if divyn[div] == 'y':#added to filter out the unwanted divs
                print 'hello'
                with open(infilename) as infile:
                    for line in infile:
                        if line.strip():
                            outfile.write(line)
            div+=1

def insertline1(infile,insertstring):
    tempfile=(path + club + "/output/temp.tmp")
    ftemp=open(tempfile,'w')
    ftemp.write(insertstring)
    ftemp.write("\n")
    finp=open(infile)
    for line in finp:
        if line.strip():
            ftemp.write(line)
    finp.close()
    ftemp.close()
    shutil.copy(tempfile,infile) 


####main()
combineEffortFiles(club)

with open(memberlist) as read_memberlist:
    member = csv.reader(read_memberlist, delimiter=',') #should changed to dict.Reader
    athlete_list=[]
    for row in member:
        athlete=row[0]
        athlete_list.append(athlete)
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
        segmentindex=0 #should change to unumerate
        with open (segmentsummary) as read_segments:
            segments = csv.DictReader(read_segments)
            for segment in segments:
                seg_id=segment['segment_id']
                elev=float(segment['elevation'])
                segefforts=(path + club + "/efforts/segmentefforts_concise_" + str(segmentindex+1) + ".csv")
                athletedict[athlete][segmentindex] = {}
                athletedict[athlete][segmentindex]["Segment_Reps"] = 0
                with open (segefforts) as read_efforts:
                    efforts = csv.reader(read_efforts)
                    for effort in efforts:
                        athleteid2=effort[1]
                        elapsed=int(effort[3])
                        if (athlete) == (athleteid2):
                            athletedict[athleteid2][segmentindex]["Segment_Reps"] += 1
                            athletedict[athlete]["total_elevation"] += elev
                segmentindex+=1
        athefforts=(path + club + "/efforts/riders/segmentefforts_concise_" + str(athlete) + ".csv")
        totalreps=0
        with open (athefforts) as atheff:
            efforts = csv.reader(atheff)
            for row in efforts:
                totalreps+=1
        athletedict[athlete]["total_reps"] = totalreps
#pprint.pprint (athletedict)


seg_count = 0
with open(segmentsummary) as read_segments:
    segment = csv.DictReader(read_segments)
    for row in segment:
        seg_count +=1
        segid = row['segment_id']
        segmentdict[segid]={}
        start = row['start_date']
        end = row['end_date']
        segname = row['name']
        elev = row['elevation']
        kom = row['kom']#no longer usable, need to replace
        qom = row['qom']#no longer usable, need to replace
        mlead = 36000#figure out the club lead time and base the score on that
        flead = 36000

        csva=(path + club + "/output/finala" + str(seg_count) + ".csv")
        csvb=(path + club + "/output/finalb" + str(seg_count) + ".csv")#ordered in vs3l division scoring
        csvc=(path + club + "/output/finalc" + str(seg_count) + ".csv")#ordered in vs3l handicap scoring
        csvd=(path + club + "/output/finald" + str(seg_count) + ".csv")#ordered in grimp kom scoring
        csve=(path + club + "/output/finale" + str(seg_count) + ".csv")#ordered in grimp qom scoring
        efforts=(path + club + "/efforts/segmentefforts_concise_" + str(seg_count) + ".csv")
        todaysefforts=(path + club + "/output/todaysefforts" + str(seg_count) + ".csv")
        todayseffortsTXT=(path + club + "/output/todaysefforts" + str(seg_count) + ".txt")
        todayseffortsHTM=(path + club + "/output/todaysefforts" + str(seg_count) + ".htm")
        fa = open(csva, 'w')
        ftc = open(todaysefforts,'w')
        ftt = open(todayseffortsTXT,'w')

#open and read tghe file once to get the fastest m and f times
        with open(efforts) as read_efforts:
            effort = csv.reader(read_efforts, delimiter=',')
            for effrow in effort:
              athleteid2=effrow[1]
              if (athleteid2) not in (athlete_list):
                pass
              else:
                segtime=int(effrow[3])
                sex=athletedict[athleteid2]["sex"]
                print (sex)
                if sex == 'F':
                    print (str(segtime) + str(type(segtime)))
                    print (str(flead) + str(type(flead)))
                    if (segtime) < (flead):
                        flead = (segtime)
                        print("Improvement!")
                    else:
                        print("no improvement")
                else:
                    if (segtime) < (mlead):
                        mlead = (segtime)
                print (flead)
        qom=flead#reuse the existing qom/kom vars below
        kom=mlead

        with open(efforts) as read_efforts:
            effort = csv.reader(read_efforts, delimiter=',')
#now go around the loop again and fill in the results
            for effrow in effort:
              segmentid=(segid)
              athleteid2=effrow[1]
              if (athleteid2) not in (athlete_list):
                pass
              else:
                activity=effrow[2]
                segtime=effrow[3]
                effortdate=effrow[4]
                segname=effrow[5]
                elevation=effrow[6]
                komrank=effrow[7]
                prrank=effrow[8]
                komscore= int(kom) * 1000 / int(segtime)
                qomscore= int(qom) * 1000 / int(segtime)
                handicap=athletedict[athleteid2]["hcap"]
                hcapscore= int(komscore) * int(handicap) / 100
                if (prrank) != "None":
                    komgif=("/icons/pr" + prrank + "icon.gif")
                elif (komrank) != "None":
                    komgif=("/icons/kom" + komrank + "icon.gif")
                else:
                    komgif=""
                komgifurl=('<img src="%s" height="50px">' % komgif)
                avatar=athletedict[athleteid2]["avatar"]
                first=athletedict[athleteid2]["first"]
                last=athletedict[athleteid2]["last"]
                newtime=str(datetime.timedelta(seconds=int(segtime)))
                newdate=(effortdate)
                d=datetime.datetime.strptime(effortdate, '%Y-%m-%dT%H:%M:%SZ')
                newdate=(datetime.date.strftime(d, "%d %b %Y"))
                div=athletedict[athleteid2]["div"]
                sex=athletedict[athleteid2]["sex"]
                if sex!="F":
                    qomscore=komscore
                cat=athletedict[athleteid2]["cat"]
                reps=athletedict[athleteid2][(seg_count-1)]["Segment_Reps"]

                fa.write("<img src=\"" + avatar + "\" height=\"50px\">,")
                fa.write("<a href=\"http://www.strava.com/athletes/" + athleteid2 + "\">")
                fa.write(first + ' ' + last + "</a>,")
                fa.write(segtime + ",")
                fa.write("<a href=\"https://www.strava.com/activities/" + activity + "\">" + newtime + "</a>,")
                fa.write(newdate + ",Division" + div + "," + sex + ",")
                fa.write(str(komscore) + "," + str(qomscore) + "," + str(hcapscore) + ",")
                fa.write(cat + ",")
                fa.write(komgifurl + "," + str(reps))
                fa.write("\n")
                if (newdate) == (today) or (newdate) == (thisweek1) or (newdate) == (thisweek2) or newdate == (thisweek3) or (newdat
e) == (thisweek4) or (newdate) == (thisweek5) or (newdate) == (thisweek6):
                    ftc.write("<img src=\"" + avatar + "\" height=\"50px\">,")
                    ftc.write("<a href=\"http://www.strava.com/athletes/" + athleteid2 + "\">")
                    ftc.write(first + ' ' + last + "</a>,")
                    ftc.write(segtime + ",")
                    ftc.write("<a href=\"https://www.strava.com/activities/" + activity + "\">" + newtime + "</a>,")
                    ftc.write(newdate + ",Division" + div + "," + sex + ",")
                    ftc.write(str(komscore) + "," + str(qomscore) + "," + str(hcapscore) + ",")
                    ftc.write(cat + ",")
                    ftc.write(komgifurl + "," + str(reps))
                    ftc.write("\n")
        ftt.write(segname + "\n")
        ftt.close()
        ftc.close()
        fa.close()

#sort the final list of efforts into fastest first, then remove any duplicate athlete (slower) efforts
        f = open(csvb, 'w')
        with open(csva) as read_efforts:
            effort = csv.reader(read_efforts)
            sortedeffort = sorted(effort,key=lambda row: int(row[2])) #this is sorting on time i.e. vs3l fastest (lowest number) fir
st.
            seen = set()
            for effrow in sortedeffort:
                if effrow[1] in seen: continue
                seen.add(effrow[1])
                f.write(",".join(effrow))
                f.write("\n")
        f.close()

#sort the final list of efforts into highest hcap score first, then remove any duplicate athlete (slower) efforts
        f = open(csvc, 'w')
        with open(csva) as read_efforts:
            effort = csv.reader(read_efforts)
            sortedefforthcap = sorted(effort,key=lambda row: int(row[9]), reverse=True)#sort on hcap score, high to low
            seen = set()
            for effrow in sortedefforthcap:
                if effrow[1] in seen: continue
                seen.add(effrow[1])
                f.write(",".join(effrow))
                f.write("\n")
        f.close()

#sort the final list of efforts into highest kom score first, then remove any duplicate athlete (slower) efforts
        f = open(csvd, 'w')
        with open(csva) as read_efforts:
            effort = csv.reader(read_efforts)
            sortedefforthcap = sorted(effort,key=lambda row: int(row[7]), reverse=True)#sort on komscore, high to low
            seen = set()
            for effrow in sortedefforthcap:
                if effrow[1] in seen: continue
                seen.add(effrow[1])
                f.write(",".join(effrow))
                f.write("\n")
        f.close()

#sort the final list of efforts into highest qom score first, then remove any duplicate athlete (slower) efforts
        f = open(csve, 'w')
        with open(csva) as read_efforts:
            effort = csv.reader(read_efforts)
            sortedefforthcap = sorted(effort,key=lambda row: int(row[8]), reverse=True)#sort on komscore, high to low
            seen = set()
            for effrow in sortedefforthcap:
                if effrow[1] in seen: continue
                seen.add(effrow[1])
                f.write(",".join(effrow))
                f.write("\n")
        f.close()


        with open(initfile) as initread:
            initstring = csv.reader(initread)
            for element in initstring:
                Year=element[1]
                Seas=element[3]
                Fort=element[5]

        divnum=0
        divcsvlist=[]
        archdivcsvlist=[]
        divhtmlist=[]
        prevscorelist=[]#don't think I need this times and compare those
        divscorelist=[]
        while divnum < TotalDivs:
            divcsvlist.append(path + club + "/output/div" + str(divnum+1) + "_seg" + str(seg_count) + ".csv")
            archdivcsvlist.append(path + club + "/archive/" + Year + Seas + Fort + "div" + str(divnum+1) + "_seg" + str(seg_count) +
 ".csv")
            divhtmlist.append(path + club + "/output/div" + str(divnum+1) + "_seg" + str(seg_count) + ".htm")
            prevscorelist.append(int(10000))
            divscorelist.append(int(divstartscores[divnum]))
            divnum+=1
        divnum=0
        fdlist=[]
        while divnum < TotalDivs:
            fd=open(divcsvlist[divnum], 'w')
            fdlist.append(fd)
            divnum+=1

        with open(csvb) as read_efforts_b:
            effortb = csv.reader(read_efforts_b)
            for effrow in effortb:
                timesecs=effrow[2]
                komscore=effrow[7]
                qomscore=effrow[8]
                hcapscore=effrow[9]
                if (effrow[5]) == "Division1": 
                    divscoring(timesecs,prevscorelist[0],divscorelist[0],fdlist[0],effrow)
                    prevscorelist[0]=prevscore_returned
                    divscorelist[0]=divscore_returned
                elif (effrow[5]) == "Division2": 
                    divscoring(timesecs,prevscorelist[1],divscorelist[1],fdlist[1],effrow)
                    prevscorelist[1]=prevscore_returned
                    divscorelist[1]=divscore_returned
                elif (effrow[5]) == "Division3": 
                    divscoring(timesecs,prevscorelist[2],divscorelist[2],fdlist[2],effrow)
                    prevscorelist[2]=prevscore_returned
                    divscorelist[2]=divscore_returned
                else: 
                    divscoring(timesecs,prevscorelist[3],divscorelist[3],fdlist[3],effrow)
                    prevscorelist[3]=prevscore_returned
                    divscorelist[3]=divscore_returned
                if (effrow[6]) == "F": 
                    divscoring(timesecs,prevscorelist[4],divscorelist[4],fdlist[4],effrow)
                    prevscorelist[4]=prevscore_returned
                    divscorelist[4]=divscore_returned
                elif (effrow[6]) == "M": 
                    divscoring(timesecs,prevscorelist[8],divscorelist[8],fdlist[8],effrow)
                    prevscorelist[8]=prevscore_returned
                    divscorelist[8]=divscore_returned
                if (effrow[10]=="V40") or (effrow[9]=="V45"): 
                    divscoring(timesecs,prevscorelist[5],divscorelist[5],fdlist[5],effrow)
                    prevscorelist[5]=prevscore_returned
                    divscorelist[5]=divscore_returned
                elif (effrow[10]=="V50") or (effrow[9]=="V55") or (effrow[9]=="V60"): 
                    divscoring(timesecs,prevscorelist[6],divscorelist[6],fdlist[6],effrow)
                    prevscorelist[6]=prevscore_returned
                    divscorelist[6]=divscore_returned
        with open(csvc) as read_efforts_c:
            effortc = csv.reader(read_efforts_c)
            for effrow in effortc:
                    timesecs=effrow[2]
                    komscore=effrow[7]
                    qomscore=effrow[8]
                    hcapscore=effrow[9]
                    divscoring(hcapscore,prevscorelist[7],divscorelist[7],fdlist[7],effrow)
                    prevscorelist[7]=prevscore_returned
                    divscorelist[7]=divscore_returned
        with open(csvd) as read_efforts_d:
#this doesn't need divscoring actually since the komscores are added in grimpeur - could remove this......
            effortd = csv.reader(read_efforts_d)
            for effrow in effortd:
                    timesecs=effrow[2]
                    komscore=effrow[7]
                    qomscore=effrow[8]
                    hcapscore=effrow[9]
                    komscoring(komscore,prevscorelist[9],0,fdlist[9],effrow)
                    prevscorelist[9]=prevscore_returned
                    divscorelist[9]=divscore_returned
        with open(csve) as read_efforts:
#this doesn't need divscoring actually since the komscores are added in grimpeur - could remove this......
            effort = csv.reader(read_efforts)
            for effrow in effort:
                    timesecs=effrow[2]
                    komscore=effrow[7]
                    qomscore=effrow[8]
                    hcapscore=effrow[9]
                    komscoring(qomscore,prevscorelist[10],0,fdlist[10],effrow)
                    prevscorelist[10]=prevscore_returned
                    divscorelist[10]=divscore_returned

        divnum=0
        while divnum < TotalDivs:
            fdlist[divnum].close()
            htmltables(divcsvlist[divnum],divhtmlist[divnum],divnamelist[divnum])
            shutil.copy(divcsvlist[divnum],archdivcsvlist[divnum]) 
            divnum+=1

        htmltables(todaysefforts,todayseffortsHTM,"")
        insertline1(todayseffortsHTM,'<h3><a href=\"https://www.strava.com/segments/' + segid + '">' + segname + '</a></h3>')

        segtable=(path + club + "/output/segtable" + str(seg_count) + ".htm")
        archivesegtable=(path + club + "/archive/" + Year + Seas + Fort + "segtable" + str(seg_count) + ".htm")
        concat(segtable)
        insertline1(segtable,'<h2><a href=\"https://www.strava.com/segments/' + segid + '">' + segname + '</a></h2><h3>From ' + star
t + ' to ' + end + '</h3><br><h3>Overall Scratch Time</h3>')
        shutil.copy(segtable,archivesegtable) 

#END
