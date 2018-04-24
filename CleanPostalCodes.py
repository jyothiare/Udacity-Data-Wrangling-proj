import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

def is_zip_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_zip(osmfile):
    osm_file = open(osmfile, "rb")
    prob_zip = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zip_code(tag):

                    if len(tag.attrib['v']) != 5:
                        if (tag.attrib['v'][0])=='N':
                            print ("Fixed Zip:   ", tag.attrib['v'], "=>", tag.attrib['v'][-5:])
                        else:
                            print ("Fixed Zip:   ", tag.attrib['v'], "=>", tag.attrib['v'][0:5])                        
                                              
                    elif tag.attrib['v'][0:2] != '96':
                        #print ("Fixed Zip:   ", tag.attrib['v'], "=>", tag.attrib['v'][0:5])
                        prob_zip.add(tag.attrib['v'])
                    elif len(tag.attrib['v']) == 5:
                        prob_zip.add(tag.attrib['v'])
    osm_file.close()
    return prob_zip

print ("Possible problematic zip codes:")



audit_zip('NYC.osm')
