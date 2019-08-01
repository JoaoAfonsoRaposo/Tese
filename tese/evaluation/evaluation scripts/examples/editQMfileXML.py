import sys, getopt
import pdb
import xml.etree.ElementTree as ET

file = "../songs/annotations/ep_groundtruth/A-HA_-_Take_on_me.xml"

def editQMfileXML(inputFile):
    root = ET.parse(inputFile).getroot()
    last_seg = root.findall('segmentation/segment')[-1]
    end_time = float(last_seg.get('end_sec'))
    print(end_time)
    
editQMfileXML(file)
#if __name__ == "__main__":
 #   editQMfile(sys.argv[1], sys.argv[2])
