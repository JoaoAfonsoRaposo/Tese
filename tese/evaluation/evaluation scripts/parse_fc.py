#parse files for fc
import xml.etree.ElementTree as ET

def parse_segmentino_file(inputFile):
    inFile = open(inputFile, "r")
    segs = {}
    for line in inFile.readlines():
        line = line.split(",")
        line[3] = line[3].replace('\n', '')
        seg = segs.get(line[3]) 
        start_time = float(line[0])
        end_time = float(float(line[0]) + float(line[1]))
        if seg == None:
            segs[line[3]] = []
        segs[line[3]].append([start_time, end_time])
    return segs

def parse_qm_segmenter_file(inputFile):
    inFile = open(inputFile, "r")
    segs = {}
    while(True):
        line1 = inFile.readline()
        pos = inFile.tell()
        line2 = inFile.readline()
        if not line2:
            break
        inFile.seek(pos)
        line1 = line1.split(",")
        line2 = line2.split(",")
        start_time = float(line1[0])
        end_time = float(line2[0])
        seg = segs.get(line1[1])
        if seg == None:
            segs[line1[1]] = []
        segs[line1[1]].append([start_time, end_time])
        if len(line2) == 4:
            start_time = float(line2[0])
            end_time = float(line2[3])
            seg = segs.get(line2[1]) 
            if seg == None:
                segs[line2[1]] = []
            segs[line2[1]].append([start_time, end_time])
    return segs

def parse_gt_file(inputFile):
    inFile = open(inputFile, "r")
    segs = {}
    for line in inFile.readlines():
        line = line.split("\t")
        del(line[2])
        seg = segs.get(line[2]) 
        start_time = float(line[0])
        end_time = float(line[1])
        if seg == None:
            segs[line[2]] = []
        segs[line[2]].append([start_time, end_time])
    return segs

def parse_gt_xml_file(inputFile):
    root = ET.parse(inputFile).getroot()
    segs = {}
    for type_tag in root.findall('segmentation/segment'):
        seg = segs.get(type_tag.get('label'))
        start_time = float(type_tag.get('start_sec'))
        end_time = float(type_tag.get('end_sec'))
        if seg == None:
            segs[type_tag.get('label')] = []
        segs[type_tag.get('label')].append([start_time, end_time])
    return segs    
    
def getSegs(inputFile, algorithm='gt'):
    if algorithm == 'gt':
        return parse_gt_file(inputFile)
    elif algorithm == 'gt_xml':
        return parse_gt_xml_file(inputFile)
    elif algorithm == 'segmentino':
        return parse_segmentino_file(inputFile)
    elif algorithm == 'qm_segmenter':
        return parse_qm_segmenter_file(inputFile)
    else:
        print("there is no such", algorithm, "algorithm")
        return 0
    
