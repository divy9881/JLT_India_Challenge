import sys
import xmltodict
import json
import csv
from doc_assist import get_extension
from csv_to_json import csv_to_json
from json_to_csv import json_to_csv
from xml_to_csv import xml_to_csv
from csv_to_xml import csv_to_xml

# def xml_to_csv(xml_content):
#     key_values = xmltodict.parse(xml_content)
#     data_keys = list(key_values["data"]["data1"].keys())
#     rows = len(key_values["data"].keys())
#     csv_str = ",".join(data_keys)
#     for i in range(rows):
#         data_values = list(key_values["data"]["data" + str(i + 1)].values())
#         for i in range(len(data_values)):
#             data_values[i] = "\"" + data_values[i] + "\""
#         csv_str += "\n" + ",".join(data_values)
#     return csv_str


# def json_to_csv(json_content):
#     data = json.loads(json_content)
#     first_data = data["data"][0]
#     rows = len(data["data"])
#     data_keys = list(first_data.keys())

#     csv_string = ",".join(data_keys)

#     for i in range(rows):
#         dict_values = list(data["data"][i].values())
#         for i in range(len(dict_values)):
#             dict_values[i] = "\"" + dict_values[i] + "\""
#         csv_string += "\n" + ",".join(dict_values)

#     return csv_string


# def csv_to_json(csv_content):
#     data = {}
#     csv_reader = csv.DictReader(csv_content.splitlines())
#     for rows in csv_reader:
#         data[rows['id']] = rows
#     return json.dumps(data, indent=4)


def json_to_xml(json_content):
    from json2xml import json2xml, readfromstring
    return json2xml.Json2xml(readfromstring(json_content)).to_xml()


def read_input(file_path) -> str:
    with open(file_path, "rt") as f:
        return f.read()


def write_output(file_path, data):
    with open(file_path, "w+") as f:
        f.write(data)


def main(input_file_path, output_file_path):
    input_extension = get_extension(input_file_path)
    output_extension = get_extension(output_file_path)
    if input_extension == "csv":
        if output_extension == "csv":
            write_output(output_file_path, read_input(input_file_path))
            print(True)
        elif output_extension == "json":
            # write_output(output_file_path, csv_to_json(read_input(input_file_path)))
            csv_to_json(input_file_path, output_file_path)
            print(True)
        elif output_extension == "xml":
            # from csv_to_xml import csv_file_to_xml
            # write_output(output_file_path, csv_file_to_xml(input_file_path))
            # write_output(output_file_path, json_to_xml(csv_to_json(read_input(input_file_path))))
            csv_to_xml(input_file_path, output_file_path)
            print(True)
        else:
            print(False)
            print("Invalid output file format")
    elif input_extension == "json":
        if output_extension == "csv":
            # write_output(output_file_path, json_to_csv(read_input(input_file_path)))
            json_to_csv(input_file_path, output_file_path)
            print(True)
        elif output_extension == "json":
            write_output(output_file_path, read_input(input_file_path))
            print(True)
        elif output_extension == "xml":
            write_output(output_file_path, json_to_xml(read_input(input_file_path)))
        else:
            print(False)
            print("Invalid output file format")
    elif input_extension == "xml":
        if output_extension == "csv":
            # write_output(output_file_path, xml_to_csv(read_input(input_file_path)))
            xml_to_csv(input_file_path, output_file_path)
            print(True)
        elif output_extension == "json":
            write_output(output_file_path, json.dumps(xmltodict.parse(read_input(input_file_path))))
            print(True)
        elif output_extension == "xml":
            write_output(output_file_path, read_input(input_file_path))
            print(True)
        else:
            print(False)
            print("Invalid output file format")
    else:
        print(False)
        print("Invalid input file format")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
    sys.stdout.flush()
