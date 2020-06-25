import csv
import json
import argparse

infile=""
outfile=""



def writefile(infile,outfile):
            print("infile:"+ infile)
            print("outfile:"+ str(outfile))
            with open (infile) as i:
                lines = i.readlines()
                for line in lines:
                    outline=line.strip()
                    outfile.write(outline + '\n')


class segmentMap():

    def concat(self,club):
        self.club = club
        maphead="/home/ubuntu/" + club + "/maps/maphead.htm"
        latlng="/home/ubuntu/" + club + "/maps/polyline.htm"
        maptail="/home/ubuntu/" + club + "/maps/maptail.htm"
        clubmap="/home/ubuntu/" + club + "/maps/mapsgrimpeur.html"
        with open (clubmap,'w') as m:
            writefile(maphead,m)
            writefile(latlng,m)
            writefile(maptail,m)

    def __init__(self,club):
        self.club = club
        print ("hello world!" + club)
        segsumm=("/home/ubuntu/" + club + "/input/segmentsummary.csv")
        seglist=[]
        with open (segsumm) as s:
            segments = csv.DictReader(s)
            for segment in segments:
                segid=(segment["segment_id"])
                name=(segment["name"])
                seglist.append([segid,name])

        maphtm=("/home/ubuntu/" + club + "/maps/polyline.htm")
        with open (maphtm,'w') as mh:
          for seg in seglist:
            segstream=("/home/ubuntu/" + club + "/input/" + seg[0] + "_stream.csv")
            segname=(seg[1])
            segname=segname.replace("'","")
            with open (segstream) as ss:
                streams=json.load(ss)
                mh.write("var latlngs = ")
                for stream in streams:
                    if (stream["type"]) == "latlng":
#                        print (str(stream["data"]))
                        print (str(stream["data"][0]))##this is the first latlng pair
                        firstll=str(stream["data"][0])
                        #mh.write(str(stream["data"]))
                        mh.write("[")
                        reset=0
                        for pos in (stream["data"]):
                            if (reset)==0:
                                mh.write(str(pos)+',')
                            if (reset) < 3: 
                                reset+=1
                            else:
                                reset=0
                  #           latlng = (pos)
                  #           latpoint = (pos[0])
                  #           lngpoint = (pos[1])
                        print (str(pos))##this is the last latlng pair
                mh.write("];\n")
                mh.write("var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);\n")
                mh.write("L.marker(" + firstll + ",{icon:grimpmapicon}).addTo(map)\n")
                mh.write("    .bindPopup('" + segname + "')\n\n")



if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--club", required=True,
        help="Club name")
    args = vars(ap.parse_args())
    club_arg = (args['club'])

    segmentMap(club_arg)

    map_instance = segmentMap(club_arg)
    map_data = map_instance.concat(club_arg)
