def fix_street(elem):
    street_types = defaultdict(set)
    if elem.tag == "node" or elem.tag == "way":
        for tag in elem.iter("tag"):
            if is_street_name(tag):
                audit_street_type(street_types, tag.attrib['v'])
                for st_type, ways in street_types.items():
                    for name in ways:
                        for key,value in mapping.items():
                            n = street_type_re.search(name)
                            if n:
                                street_type = n.group()
                                if street_type not in expected:
                                    if street_type in mapping:
                                        better_name = name.replace(key,value)
                                        if better_name != name:
                                            #print ("Fixed Street:", tag.attrib['v'], "=>", better_name)
                                            tag.attrib['v'] = better_name
                                            return
    # Fix Zip Codes:

def fix_zip(elem):
    if elem.tag == "node" or elem.tag == "way":
        for tag in elem.iter("tag"):
            if is_zip_code(tag):
                if len(tag.attrib['v']) != 5:
                    if (tag.attrib['v'][0])=='N':
                        #print ("Fixed Zip:   ", tag.attrib['v'], "=>", tag.attrib['v'][-5:])
                        tag.attrib['v'] = tag.attrib['v'][-5:]
                    else:
                        #print ("Fixed Zip:   ", tag.attrib['v'], "=>", tag.attrib['v'][0:5])
                        tag.attrib['v'] = tag.attrib['v'][0:5]
                            
                            
def fix_element(elem):
    
    # Fix Street Names:

    # mapping provides a dictionary for updating potentially problematic street type names.
    # Dictionary contents were updated iteratively, based on the audit results
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
    fix_street(elem)
    fix_zip(elem)
   