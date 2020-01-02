import pandas as pd
import sys
import json

# filePath = sys.argv[1]
def csv_to_json(filePath, outputFilePath):

    data = pd.read_csv(filePath)

    fields = list(data)

    rows = len(data[fields[0]])
    cols = len(fields)

    dict_object = {}
    dict_object["data"] = []

    for i in range(rows):
        samp_dict = {}
        for j in range(cols):
            samp_dict[fields[j]] = data[fields[j]][i]
        dict_object["data"].append(samp_dict)

    json_object = json.dumps(dict_object,sort_keys=True, indent=4)

    # reversedString=''.join(reversed(filePath))
    # first_index = reversedString.index(".")
    # reversedString = "nosj" + reversedString[first_index:]
    # filePath = ''.join(reversed(reversedString))

    f = open(outputFilePath, "w+")
    f.write(json_object)
    f.close()