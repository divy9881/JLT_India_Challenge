import os
import csv
from docx import Document
import re
from typing import Union
import json


def get_extension(file_path: str):
    return file_path[file_path.rindex('.') + 1:]


def read_csv(csv_file) -> (bool, Union[dict, str]):
    try:
        with open(csv_file, mode='r') as infile:
            reader = csv.reader(infile)
            kvp = {rows[0]: rows[1] for rows in reader}
        return True, kvp
    except OSError:
        return False, 'File Not Found'


def replacer(text: str, match: re.Match, kvp: dict, char: int = 2):
    # text -> the whole line
    got = match.string[match.start() + char: match.end() - char]
    # got -> the matching text inside << >>
    if got[0] == "+":
        keys = got.split('+')
        text_header = keys[2].upper().strip()
        data = kvp.get(got)
        if data is not None:
            text = text[:match.start()] + text_header + "\n" + data + " " + text[match.end() + 1:]
    else:
        data = kvp.get(got)
        if data is not None:
            text = text[:match.start()] + data + " " + text[match.end() + 1:]
    return text


def create_doc(template_file, key_values, output_name):
    try:
        document = Document(template_file)

        for para in document.paragraphs:
            regex = [(r"«([a-zA-Z0-9_+ -])*»", 1), (r"<<([a-zA-Z0-9_+ -])*>>", 2)]
            for r in regex:
                matches = re.finditer(r[0], para.text, re.MULTILINE)
                for m in reversed(list(matches)):
                    para.text = replacer(para.text, m, key_values, char=r[1])

        document.save(output_name)
    except Exception as e:
        return False, repr(e)
    return True, None


def main(template_file: str, key_values: dict):
    template_ext = get_extension(template_file)
    if template_ext == "docx":
        output_name = template_file[:template_file.rindex('.')] + '-output' + '.' + template_ext
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
        ok, key_values = read_csv(kvp_file)
        if ok:
            main(template_file, key_values)
        else:
            print(False)
            print(key_values)
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


if __name__ == '__main__':
    import sys

    main(sys.argv[1], sys.argv[2])
    # main_json_str(os.getcwd() + '\\files\\templates\\demo.docx',
    #               '{"JMF_CLIENTNAME": "Motor Vehicle", "jmf_DateCreated": "2011-2012", "+DECINTRO+ Introduction - Declaration": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus convallis dapibus ex at dapibus. Ut bibendum rutrum commodo. Etiam ut arcu eget felis venenatis congue at et libero. Praesent at quam dignissim, bibendum sapien in, convallis eros. Sed cursus justo vitae nisl ultrices, a vehicula elit vestibulum. Morbi accumsan suscipit facilisis. Nam at tempor est. Vestibulum magna metus, finibus sed lectus vel, feugiat laoreet mi. Sed dignissim sem turpis, a egestas dolor vehicula ut. Pellentesque pharetra et nisl in fermentum. Proin cursus egestas purus, sed bibendum arcu sagittis at. Suspendisse potenti. Nunc venenatis velit sem, ut bibendum lectus malesuada a. Nunc libero velit, placerat id vestibulum a, condimentum id lacus. Pellentesque vehicula viverra bibendum. Praesent congue ipsum sit amet mauris mollis finibus.\n\nProin non gravida nisl, sit amet varius diam. Phasellus dictum magna et metus fringilla scelerisque. Cras porta fermentum velit quis accumsan. Nam luctus mauris faucibus, rhoncus dolor non, efficitur eros. Donec quis ligula a risus semper euismod nec id augue. In maximus dictum lacus. Vivamus sapien lorem, maximus in ipsum ut, fermentum pulvinar sem. Phasellus ut ornare dolor. Nullam a sapien enim.\n\nPellentesque interdum tortor quis ipsum sollicitudin congue et ac dui. Nam feugiat nisl libero, a rhoncus metus pharetra sed. Vestibulum varius, nunc sit amet malesuada molestie, quam dolor rhoncus leo, posuere faucibus nunc eros eget leo. Vivamus nec est eu mauris aliquam semper a eget metus. In ut tortor sem. Quisque quis massa at orci tincidunt bibendum. Pellentesque at rhoncus metus, non venenatis libero. Donec dapibus, metus vitae eleifend blandit, risus lorem vulputate arcu, sodales varius risus mi ut sapien. Phasellus quis turpis et dolor sodales imperdiet. Vivamus ac mauris rutrum odio efficitur varius in placerat nisi. Ut placerat tortor quam, non tincidunt lorem auctor at.\n\nMorbi consectetur urna justo, et ornare quam ornare eu. Suspendisse nec sem sit amet turpis tincidunt ornare ac in urna. Etiam eget tellus convallis, maximus tellus eget, imperdiet magna. In cursus augue viverra tortor euismod malesuada. Donec at massa non mi posuere aliquam. Sed a tincidunt massa. Fusce dui enim, egestas at enim et, elementum lacinia augue. Maecenas quis imperdiet leo, in laoreet nibh. Aliquam sit amet nunc in massa mollis sagittis quis varius ex.\n\nNunc in lobortis ex. Morbi et nisi nibh. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Quisque bibendum felis a semper malesuada. Aliquam tristique justo vitae tincidunt faucibus. Suspendisse neque felis, luctus non urna sed, hendrerit iaculis nulla. Vestibulum consequat magna mattis sapien molestie venenatis. Etiam ex metus, auctor sit amet volutpat ac, eleifend vel odio. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos."}')
    # main_kvp_file(os.getcwd() + '\\files\\templates\\Template.docx', os.getcwd() + '\\files\\kvp\\demo.csv')
    sys.stdout.flush()