#parse files for br
import xml.etree.ElementTree as ET

def parse_segmentino_file(inputFile):
    inFile = open(inputFile, "r")
    bounds = []
    for line in inFile.readlines():
        line = line.split(",")
        boundary = float(float(line[0]) + float(line[1]))
        bounds.append(boundary)
    return bounds

def parse_qm_segmenter_file(inputFile):
    inFile = open(inputFile, "r")
    bounds = []
    for line in inFile.readlines():
        line = line.split(",")
        boundary = float(line[0])
        bounds.append(boundary)
    return bounds

def parse_gt_file(inputFile):
    inFile = open(inputFile, "r")
    bounds = []
    for line in inFile.readlines():
        line = line.split("\t")
        boundary = float(line[1])
        bounds.append(boundary)
    return bounds

def parse_gt_xml_file(inputFile):
    root = ET.parse(inputFile).getroot()
    bounds = []
    for type_tag in root.findall('segmentation/segment'):
        boundary = float(type_tag.get('end_sec'))
        bounds.append(boundary)
    return bounds[1:-1]

def getBounds(inputFile, algorithm='gt'):
    if algorithm == 'gt':
        return parse_gt_file(inputFile)
    elif algorithm == 'gt_xml':
        return parse_gt_xml_file(inputFile)
    elif algorithm == 'segmentino':
        return parse_segmentino_file(inputFile)
    elif algorithm == 'qm_segmenter':
        return parse_segmentino_file(inputFile)
    else:
        print("there is no such", algorithm, "algorithm")
        return 0
