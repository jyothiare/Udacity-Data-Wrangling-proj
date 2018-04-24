import xml.etree.cElementTree as ET 
2 import pprint 
3 
 
4 osm_file = open("austin_texas.osm", "r") 

def count_tags(filename):
"""  
8 		Parses through tags and adds tag to dictionary  
9 		after calling the add_tag function  
10  
11 		Args: 
12 			file: .osm file containing the OpenStreetMap data 
13  
14 		Returns: 
15 			tag_names: Dictionary containing tag type and count 
16 	""" 

    counts = defaultdict(int)
    for line in ET.iterparse(filename):
        current = line[1].tag
        counts[current] += 1
    return counts


def test():
    tags = count_tags('NYC.osm')
    pprint.pprint(tags)
    

    

test()