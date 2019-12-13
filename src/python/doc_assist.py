import os
import csv
from docx import Document
import re
from typing import Union


def get_extension(filepath: str):
    return filepath[filepath.rindex('.') + 1:]


def read_csv(csv_file) -> (bool, Union[dict, str]):
    try:
        with open(csv_file, mode='r') as infile:
            reader = csv.reader(infile)
            kvp = {rows[0].strip().lower(): rows[1].strip() for rows in reader}
        return True, kvp
    except OSError:
        return False, 'File Not Found'


def replacer(text: str, match: re.Match, kvp: dict, char:int=2):
    # text -> the whole line
    got = match.string[match.start() + char: match.end() - char]
    # got -> the matching text inside << >>
    if got[0] == "+":
        keys = got.split('+')
        text_header = keys[2].upper().strip()
        data = kvp.get(got.strip().lower())
        if data is not None:
            text = text[:match.start()] + text_header + "\n" + data + " " + text[match.end() + 1:]
    else:
        data = kvp.get(got.strip().lower())
        if data is not None:
            text = text[:match.start()] + data + " " + text[match.end() + 1:]
    return text


def create_doc(template_file, key_values, output_name):
    try:
        document = Document(template_file)

        for para in document.paragraphs:
            matches = re.finditer(r"<<([a-zA-Z0-9_+ -])*>>", para.text, re.MULTILINE)
            for m in reversed(list(matches)):
                para.text = replacer(para.text, m, key_values, char=2)
            matches = re.finditer(r"«([a-zA-Z0-9_+ -])*»", para.text, re.MULTILINE)
            for m in reversed(list(matches)):
                para.text = replacer(para.text, m, key_values, char=1)

        document.save(output_name)
    except Exception as e:
        return False, repr(e)
    return True, None


def main(template_file: str, kvp_file: str):
    kvp_ext = get_extension(kvp_file)
    if kvp_ext == "csv":
        template_ext = get_extension(template_file)
        if template_ext == "docx":
            output_name = template_file[:template_file.rindex('.')] + '-output' + '.' + template_ext
            ok, key_values = read_csv(kvp_file)
            if not ok:
                print(key_values)
            else:
                ok, error = create_doc(template_file, key_values, output_name)
                print(ok)
                if not ok:
                    print(error)
        else:
            print(False)
            print("Improper Template file format")
    else:
        print(False)
        print("Improper Key-Value Pair file format")


if __name__ == '__main__':
    import sys

    # main(sys.argv[1], sys.argv[2])
    main(os.getcwd() + '\\files\\templates\\Template.docx', os.getcwd() + '\\files\\kvp\\demo.csv')
    sys.stdout.flush()
