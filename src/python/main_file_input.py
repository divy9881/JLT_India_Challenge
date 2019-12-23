import sys
import doc_assist as doc

if __name__ == "__main__":
    data_filepath = sys.argv[2]
    file_extension = data_filepath[-4:]
    
    if file_extension == ".csv":
        doc.main_kvp_file(sys.argv[1], data_filepath)
    elif file_extension == "json":
        doc.main_json_object(sys.argv[1], data_filepath)
    elif file_extension == ".xml":
        doc.main_xml_object(sys.argv[1], data_filepath)

    sys.stdout.flush()