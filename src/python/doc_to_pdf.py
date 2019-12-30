import os
import convertapi
from doc_assist import get_extension
import mammoth

convertapi.api_secret = 'zjXpGuMeVAO171vl'


def converter(in_file, out_file):
    in_file = os.path.abspath(in_file)
    out_file = os.path.abspath(out_file)

    in_ext = get_extension(in_file)
    out_ext = get_extension(out_file)

    if in_ext == "docx":
        extensions = ["jpg", "pdf", "pdfa", "png", "tiff", "txt", "zip"]
        if out_ext in extensions:
            result = convertapi.convert(out_ext, {'File': in_file}, from_format=in_ext)
            print(result)
            result.file.save(out_file)
        elif out_ext == "html":
            with open(in_file, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html = result.value
                with open(out_file, "w+") as f:
                    f.write(html)
        else:
            print(False)
    else:
        print(False)


if __name__ == '__main__':
    converter(".\\files\\templates\\Template-output_2.docx", ".\\a.pdf")
