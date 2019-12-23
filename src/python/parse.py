import os
import re
import json
from docx import Document


def main(template_file):
    try:
        document = Document(template_file)
        kvp = dict()
        for para in document.paragraphs:
            regex = [(r"«([a-zA-Z0-9_+ &.-])*»", 1), (r"<<([a-zA-Z0-9_+ &.-])*>>", 2)]
            for r in regex:
                matches = re.finditer(r[0], para.text, re.MULTILINE)
                for m in reversed(tuple(matches)):
                    got = m.string[m.start() + r[1]: m.end() - r[1]]
                    if got in kvp.keys():
                        pass
                    else:
                        if got[0] == "+":
                            got_ = got[1:]
                            keys = got_.split('+')
                            kvp[got] = keys[1]
                        else:
                            kvp[got] = got
        print(True)
        print(json.dumps(kvp))
    except Exception as e:
        print(False)
        print(repr(e))


if __name__ == '__main__':
    import sys

    main(sys.argv[1])
    # main(os.getcwd() + '\\files\\templates\\Template.docx')
    # main(os.getcwd() + '\\files\\templates\\demo.docx')
    sys.stdout.flush()
