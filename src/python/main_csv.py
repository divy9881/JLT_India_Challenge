import sys
import doc_assist as doc

if __name__ == "__main__":
    doc.main_kvp_file(sys.argv[1], sys.argv[2])
    sys.stdout.flush()