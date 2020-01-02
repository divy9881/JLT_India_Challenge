import json
import xmltodict
from csv_to_xml import *

def json_to_xml(filePath, outputFilePath):
    f = open(filePath, "r")

    data = json.load(f)
    f.close()

    first_data = data["data"][0]
    rows = len(data["data"])
    data_keys = list(first_data.keys())

    csv_string = ",".join(data_keys)

    for i in range(rows):
        dict_values = list(data["data"][i].values())
        for i in range(len(dict_values)):
            dict_values[i] = "\"" + dict_values[i] + "\""
        csv_string += "\n" + ",".join(dict_values)

    # reversedString=''.join(reversed(filePath))
    # first_index = reversedString.index(".")
    # reversedString = "vsc" + reversedString[first_index:]
    # filePath = ''.join(reversed(reversedString))

    # f = open(outputFilePath, "w+")
    # f.write(csv_string)
    # f.close()
    data = read_csv(filePath)
    fields = get_fields(data[0])
    tags = create_tags(fields)
    count = 1
    xml_string = "<data>" + "\n"
    for row in data[1:]:
        xml_string = xml_string + "<data" + str(count) + ">" + "\n"
        xml_string = xml_string + convert_row(row, tags)
        xml_string = xml_string + "</data" + str(count) + ">" + "\n"
        count = count + 1
    xml_string = xml_string + "</data>"
    # filePath = get_xml_filepath(filePath)
    f = open(outputFilePath,"w+")
    f.write(xml_string)
    f.close() 