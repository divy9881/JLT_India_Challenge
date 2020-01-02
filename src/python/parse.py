import re
import json
from docx import Document


def main(template_file):
    try:
        document = Document(template_file)
        kvp = dict()
        for para in document.paragraphs:
            regex = r"(<<|«)([^><»«\n]*)(>>|»)"
            matches = re.finditer(regex, para.text, re.MULTILINE)
            for match in reversed(tuple(matches)):
                got = match.group(2)
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
    sys.stdout.flush()
