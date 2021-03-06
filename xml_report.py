
def get_xml(comments):
    xml_res = '<?xml version="1.0" encoding="utf-8"?><comments>'
    rec = '<Comment><id>%s</id><parent_id>%s</parent_id><user_id>%s</user_id><text>"%s"</text></Comment>'
    for row in comments:
        xml_res += rec % (row[0], row[1], row[2], row[3])
    xml_res += '</comments>'
    return xml_res
