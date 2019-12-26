import os
import csv
from docx import Document
import sys
import re
import json
from docx.shared import Pt
import xmltodict
import pprint

count = 1


def get_extension(file_path: str):
    return file_path[file_path.rindex('.') + 1:]


def read_csv(template_file, csv_file):
    try:
        with open(csv_file, mode='r') as infile:
            reader = csv.reader(infile)
            line_count = 0
            for rows in reader:
                if line_count == 0:
                    fields = rows
                    line_count = line_count + 1
                else:
                    i = 0
                    kvp = dict()
                    for row in rows:
                        kvp[fields[i]] = row
                        i = i + 1
                    main(template_file, kvp)

    except OSError:
        print("Error File Not Found")
        exit()


def replacer(match: re.Match, kvp: dict, char: int = 2) -> (str, str):
    # text -> the whole line
    got = match.string[match.start() + char: match.end() - char]
    # got -> the matching text inside << >>
    if got[0] == "+":
        keys = got.split('+')
        text_header = keys[2].upper().strip()
        data = kvp.get(got)
        return text_header, data
    else:
        data = kvp.get(got)
        text_header = ""
        return text_header, data


def create_doc(template_file, key_values, output_name):

    try:
        document = Document(template_file)
        for para in document.paragraphs:
            regex = [(r"«([a-zA-Z0-9_+ &.])*»", 1), (r"<<([a-zA-Z0-9_+ &.-])*>>", 2)]
            for r in regex:
                matches = re.finditer(r[0], para.text, re.MULTILINE)
                for m in reversed(list(matches)):
                    header, data = replacer(m, key_values, char=r[1])

                    if header == "":
                        if data is not None:
                            style = document.styles['Normal']
                            font = style.font
                            font.name = 'Arial'
                            font.size = Pt(10)
                            para.styles = document.styles['Normal']
                            para.text = para.text[:m.start()] + str(data) + " " + para.text[m.end() + 1:]
                    else:
                        if data is not None:
                            style = document.styles['Normal']
                            font = style.font
                            font.name = 'Arial'
                            font.size = Pt(10)
                            para.styles = document.styles['Normal']
                            para.text = para.text[:m.start()] + str(data) + " " + para.text[m.end() + 1:]
                            header_paragraph = para.insert_paragraph_before(data)
                            font.size = Pt(15)
                            header_paragraph.styles = document.styles['Normal']
                            header_paragraph.text = header

        document.save(output_name)
    except Exception as e:
        return False, repr(e)
    return True, None


def main(template_file: str, key_values: dict):
    global count
    template_ext = get_extension(template_file)
    if template_ext == "docx":
        output_name = template_file[:template_file.rindex('.')] + '-output_' + str(count) + '.' + template_ext
        count = count + 1
        ok, error = create_doc(template_file, key_values, output_name)
        print(ok)
        if not ok:
            print(error)
        else:
            print(output_name)
    else:
        print(False)
        print("Improper Template file format")


def main_kvp_file(template_file: str, kvp_file: str):
    kvp_ext = get_extension(kvp_file)
    if kvp_ext == "csv":
        read_csv(template_file, kvp_file)
    else:
        print(False)
        print("Improper Key-Value Pair file format")


def main_json_str(template_file: str, json_str: str):
    try:
        json_str = json_str.replace("\n", "\\n")
        json_str = json_str.replace("\t", "\\t")
        key_values: dict = json.loads(json_str)
        main(template_file, key_values)
    except json.JSONDecodeError as e:
        print(False)
        print(repr(e))


def main_json_object(template_file: str, json_file: str):
    try:
        with open(json_file) as f:
            key_values = json.load(f)
            # json_str = json_str.replace("\n", "\\n")
            # json_str = json_str.replace("\t", "\\t")
            # key_values: dict = json.loads(json_str)
            for val in key_values["data"]:
                main(template_file, val)
    except json.JSONDecodeError as e:
        print(False)
        print(repr(e))


def main_xml_object(template_file: str, xml_file: str):
    with open(xml_file) as f:
        key_values = xmltodict.parse(f.read())
        for i, j in key_values.items():
            for k,m in j.items():
                kvp = dict()
                for n,q in m.items():
                    kvp[n] = q
                main(template_file, kvp)
                
# if __name__ == '__main__':

    # main_json_str(sys.argv[1], sys.argv[2])   
    # main_json_str(os.getcwd() + '\\files\\templates\\demo.docx',
    #               '{"JMF_CLIENTNAME": "Motor Vehicle", "jmf_DateCreated": "2011-2012", "+DECINTRO+ Introduction - Declaration": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus convallis dapibus ex at dapibus. Ut bibendum rutrum commodo. Etiam ut arcu eget felis venenatis congue at et libero. Praesent at quam dignissim, bibendum sapien in, convallis eros. Sed cursus justo vitae nisl ultrices, a vehicula elit vestibulum. Morbi accumsan suscipit facilisis. Nam at tempor est. Vestibulum magna metus, finibus sed lectus vel, feugiat laoreet mi. Sed dignissim sem turpis, a egestas dolor vehicula ut. Pellentesque pharetra et nisl in fermentum. Proin cursus egestas purus, sed bibendum arcu sagittis at. Suspendisse potenti. Nunc venenatis velit sem, ut bibendum lectus malesuada a. Nunc libero velit, placerat id vestibulum a, condimentum id lacus. Pellentesque vehicula viverra bibendum. Praesent congue ipsum sit amet mauris mollis finibus.\n\nProin non gravida nisl, sit amet varius diam. Phasellus dictum magna et metus fringilla scelerisque. Cras porta fermentum velit quis accumsan. Nam luctus mauris faucibus, rhoncus dolor non, efficitur eros. Donec quis ligula a risus semper euismod nec id augue. In maximus dictum lacus. Vivamus sapien lorem, maximus in ipsum ut, fermentum pulvinar sem. Phasellus ut ornare dolor. Nullam a sapien enim.\n\nPellentesque interdum tortor quis ipsum sollicitudin congue et ac dui. Nam feugiat nisl libero, a rhoncus metus pharetra sed. Vestibulum varius, nunc sit amet malesuada molestie, quam dolor rhoncus leo, posuere faucibus nunc eros eget leo. Vivamus nec est eu mauris aliquam semper a eget metus. In ut tortor sem. Quisque quis massa at orci tincidunt bibendum. Pellentesque at rhoncus metus, non venenatis libero. Donec dapibus, metus vitae eleifend blandit, risus lorem vulputate arcu, sodales varius risus mi ut sapien. Phasellus quis turpis et dolor sodales imperdiet. Vivamus ac mauris rutrum odio efficitur varius in placerat nisi. Ut placerat tortor quam, non tincidunt lorem auctor at.\n\nMorbi consectetur urna justo, et ornare quam ornare eu. Suspendisse nec sem sit amet turpis tincidunt ornare ac in urna. Etiam eget tellus convallis, maximus tellus eget, imperdiet magna. In cursus augue viverra tortor euismod malesuada. Donec at massa non mi posuere aliquam. Sed a tincidunt massa. Fusce dui enim, egestas at enim et, elementum lacinia augue. Maecenas quis imperdiet leo, in laoreet nibh. Aliquam sit amet nunc in massa mollis sagittis quis varius ex.\n\nNunc in lobortis ex. Morbi et nisi nibh. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Quisque bibendum felis a semper malesuada. Aliquam tristique justo vitae tincidunt faucibus. Suspendisse neque felis, luctus non urna sed, hendrerit iaculis nulla. Vestibulum consequat magna mattis sapien molestie venenatis. Etiam ex metus, auctor sit amet volutpat ac, eleifend vel odio. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos."}')
    
    # main_kvp_file(os.getcwd() + '\\files\\templates\\Template.docx', os.getcwd() + '\\files\\kvp\\demo2.csv')

    # main_kvp_file(sys.argv[1], sys.argv[2])
# main_kvp_file(os.getcwd() + '\\files\\templates\\demo.docx', os.getcwd() + '\\files\\kvp\\demo2.csv')
# sys.stdout.flush()

    # main_kvp_file(os.getcwd() + '\\files\\templates\\Template.docx', os.getcwd() + '\\files\\kvp\\demo2.csv')

