import xml.etree.ElementTree as ET

root = ET.parse('Wise_Guys_-_Powerfrau.xml').getroot()
print(root)

for type_tag in root.findall('segmentation/segment'):
    start_sec = type_tag.get('start_sec')
    end_sec = type_tag.get('end_sec')
    print(start_sec)
    print(end_sec)
