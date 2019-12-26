import csv 
import os
import sys

def read_csv(csv_file):
    try:
        with open(csv_file, mode='r') as infile:
            reader = csv.reader(infile)
            data = []
            for row in reader: 
                data.append(row)
            
            return data

    except OSError:
        print("Error File Not Found")
        exit()

def create_tags(fields):
    tags = ""
    length = len(fields)
    for field in fields[:-1]:
        tags = tags + "<" + field + ">%s</" + field + ">" + "\n"
    tags = tags + "<" + fields[length-1] + ">%s</" + fields[length-1] + ">"
    return tags

def convert_row(row, tags):
    data = tuple()
    for entry in row:
        data = data + (entry,)
    test = """""" + tags + """"""
    return test % data

def get_fields(row):
    fields = []
    for entry in row:
        if(entry[0] == "+"):
            entry_ = entry[1:].split("+")
            fields.append(entry_[1].strip())
        else :
            fields.append(entry.strip())
    return fields

def get_xml_filepath(file_path: str):
    xml_path = file_path[:file_path.rindex('.') + 1]
    xml_path = xml_path + "xml"
    return xml_path

if __name__ == '__main__':
    filePath = sys.argv[1]
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
    filePath = get_xml_filepath(filePath)
    f = open(filePath,"w+")
    f.write(xml_string)
    f.close()