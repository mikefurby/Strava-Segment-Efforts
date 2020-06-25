import csv
from sys import argv
import time

def readeffortfile(infile,outfile):
        try:
            with open (infile) as read:
                lines = read.readlines()            
                for line in lines:
                    linestr=line.strip()
                    outfile.write(linestr + '\n')
                    print(linestr)
            print("File does exist: " + infile)
        except:
            print("File does not exist: " + infile)
#        time.sleep(1)

class combineEffortFiles():
    def __init__(self,club):
        path1=("/home/ubuntu/")
        path2=(path1 + "Strava/")
        segsumm=(path1 + club + "/input/segmentsummary.csv")
        memberfile=(path1 + club + "/input/membersdiv.csv")
        concise=(path1 + club + "/efforts/segmentefforts_concise.csv")
        webform=(path2 + club + "/efforts/segmentefforts_concise_webform.csv")
        webhook=(path2 + club + "/efforts/segmentefforts_concise_webhook.csv")
        vsccwebhook=(path2 + "vscc/efforts/segmentefforts_concise_webhook.csv")
        full_concise=(path1 + club + "/efforts/segmentefforts_full_concise.csv")

###delete rider file info###could combine with below but no real need, this keeps is simpler to understand why I have this here.
        with open(memberfile) as m:
            members=csv.reader(m)
            for member in members:
                id=member[0]
                rfile=(path1 + club + "/efforts/riders/segmentefforts_concise_" + id + ".csv")
                try:
                    open(rfile,'w').close()
                except:
                    pass

        with open (full_concise,'w') as fc:
            fc.write("segment_id,athlete_id,activity_id,elapsed_time,start_date,segment_name,segment_elevation,top_10,pr,\n")
            readeffortfile(concise,fc)#this first because it has the headers
            readeffortfile(webform,fc)
            readeffortfile(webhook,fc)
            readeffortfile(vsccwebhook,fc)
            with open(memberfile) as m:
                members=csv.reader(m)
                for member in members:
                    id=member[0]
                    reauth=(path2 + club + "/efforts/segmentefforts_concise_" + id + ".csv")
                    readeffortfile(reauth,fc)

        #activity_list=[]
        #activity_list_sorted=[]
        with open(segsumm) as rsegs:
            all_segments = csv.DictReader(rsegs)
            for index,segs in enumerate(all_segments,start=1):
                activity_list=[]
                activity_list_sorted=[]
                segment_id = segs["segment_id"]
                segment_name = segs["name"]
                print("rows checked: " + str(index) + str(segment_id) + segment_name)
                eachseg=(path1 + club + "/efforts/segmentefforts_concise_" + str(index) + ".csv")
                with open (eachseg,'w') as w:
                    with open(full_concise) as readefforts:
                        efforts=csv.DictReader(readefforts)
                        #print (str(readefforts))
                        for row in efforts:
                            segment_id_match = row["segment_id"]
                            #print(segment_id_match)
                            if segment_id == segment_id_match:
                                athlete_id = row["athlete_id"]
                                #print("We have a match: " + segment_id + segment_name + " athlete "+ athlete_id)
                                rider_concise=(path1 + club + "/efforts/riders/segmentefforts_concise_" + athlete_id + ".csv")
                                segment_string = (str(row["segment_id"]) + ',' + row["athlete_id"] + ',' + row["activity_id"] + ',' 
+ row["elapsed_time"] + ',' + row["start_date"] + ',"' + row["segment_name"] + '",' + row["segment_elevation"] + ',' + row["top_10"]
 + ',' + row["pr"] + ',' + '\n')
                                if (row["activity_id"]) == 'none':
                                    print("Webform entered with no activity ID and so it is included in segment_effort_concise_" +  
str(index) + ".csv")
                                    w.write(segment_string)
                                elif (row["activity_id"]) == "activity_id":
                                    print("Filtering out csv fields line. Not using this yet in the per segment concise files")
                                elif (int(row["activity_id"])) not in activity_list:
                                    #print("Unique activity")
                                    w.write(segment_string)
                                    with open(rider_concise,'a') as rider:
                                        rider.write(segment_string)
                                    activity_list.append(int(row["activity_id"]))
                                else:
                                    print("Duplicate activity. Filtered out from segment_effort_concise_" +  str(index) + ".csv " + 
str(row["activity_id"]))
                                    w.write(segment_string)
                                    with open(rider_concise,'a') as rider:
                                        rider.write(segment_string)
                                    activity_list.append(int(row["activity_id"]))
                                    #print(segment_string)
        
        #print(activity_list)
        activity_list.sort()
        #print(activity_list)


if __name__ == '__main__':
    script, club = argv
    combineEffortFiles(club)
