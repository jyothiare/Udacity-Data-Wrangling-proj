import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

#OSMFILE = "NYC.osm"
OSMFILE = "sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
st_types = defaultdict(set)
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Bend", "Chase", "Circle", "Cove", "Crossing", "Hill",
            "Hollow", "Loop", "Park", "Pass", "Overlook", "Path", "Plaza", "Point", "Ridge", "Row",
            "Run", "Terrace", "Walk", "Way", "Trace", "View", "Vista","Concourse","South","North","East",
             "West","Mews","Broadway","Alley","street","avenue","Americas","Village","Bowery"]
             

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "st": "Street",
            "st.": "Street",
            "ST": "Street",
            "Ave": "Avenue",
            "ave": "Avenue",
            "Avene": "Avenue",
            "avene": "Avenue",
            "Aveneu": "Avenue",
             "steet": "Street",
            "Steet": "Street",            
            "Rd.": "Road",
            "W": "West",
            "N": "North",
            "S": "South",
            "E": "East"}


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "rb")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):
    after = []
    # Split name string to test each part of the name;
    # Replacements may come anywhere in the name.
    for part in name.split(" "):
        # Check each part of the name against the keys in the correction dict
        if part in mapping.keys():
            # If exists in dict, overwrite that part of the name with the dict value for it.
            part = mapping[part]
        # Assemble each corrected piece of the name back together.
        after.append(part)
    # Return all pieces of the name as a string joined by a space.
    return " ".join(after)
    

#     for w in mapping.keys():
#         if w in name:
#             if flag:
#                 continue
#             # Replace abbrev. name in string with full name value from the mapping dict.
#             name = name.replace(w, mapping[w], 1)
#             # If St., flag to not check again in this string looking for St since new 'Street' will contain St
#             # re.compile() might be better
#             if w == "St.":
#                 flag = True

    return name


def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    #pprint.pprint(dict(st_types))

    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_name(name, mapping)
            print (name, "=>", better_name)
           



test()