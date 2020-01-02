import sys
import doc_assist as doc

if __name__ == "__main__":
    data_filepath = sys.argv[2]
    output_folder = sys.argv[3]
    file_extension = doc.get_extension(data_filepath)

    if file_extension == "csv":
        doc.main_kvp_file(sys.argv[1], data_filepath, output_folder)
    elif file_extension == "json":
        doc.main_json_file(sys.argv[1], data_filepath, output_folder)
    elif file_extension == "xml":
        doc.main_xml_file(sys.argv[1], data_filepath, output_folder)

    sys.stdout.flush()
