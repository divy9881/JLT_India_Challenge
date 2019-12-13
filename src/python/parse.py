import os
import re
import json
from docx import Document


def main(template_file):
    try:
        document = Document(template_file)
        kvp = dict()
        for para in document.paragraphs:
            regex = r"<<([a-zA-Z0-9_+ -])*>>"
            matches = re.finditer(regex, para.text, re.MULTILINE)
            for m in reversed(tuple(matches)):
                got = m.string[m.start() + 2: m.end() - 2]
                if got in kvp.keys():
                    pass
                else:
                    if got[0] == "+":
                        got_ = got[1:]
                        keys = got_.split('+')
                        kvp[got] = keys[1]
                    else:
                        kvp[got] = got
        print(json.dumps(kvp))

    except Exception as e:
        print("")


if __name__ == '__main__':
    import sys

    # main(sys.argv[1])
    main(os.getcwd() + '\\files\\templates\\demo.docx')
    sys.stdout.flush()
