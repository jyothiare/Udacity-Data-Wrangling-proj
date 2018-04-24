import xml.etree.cElementTree as ET 
import pprint 
import re 

lo = set()
lo_co = set()
pro_co = set()
oth = set()

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\, \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        k_value = element.attrib['k']
        if lower.search(k_value) is not None:
            keys['lower'] += 1
            lo.add(element.attrib['k'])
        elif lower_colon.search(k_value) is not None:
            keys['lower_colon'] += 1
            lo_co.add(element.attrib['k'])
        elif problemchars.search(k_value) is not None:
            keys["problemchars"] += 1
            pro_co.add(element.attrib['k'])
        else:
            keys['other'] += 1
            oth.add(element.attrib['k'])
        pass
        
    return keys

def write_data(data, filename):
    with open(filename, 'w') as f:
        for x in data:
            f.write(x + "\n")

def process_map1(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    
    keys = process_map1('NYC.osm')
    write_data(lo, 'lower.txt')
    write_data(lo_co, 'lower_colon.txt')
    write_data(pro_co, 'problem_chars.txt')
    write_data(oth, 'other.txt')
    pprint.pprint(keys)
    #assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


	
test()