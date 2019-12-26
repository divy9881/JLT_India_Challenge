import sys
import xmltodict

filePath = sys.argv[1]

csv_str = ""

with open(filePath) as f:
    key_values = xmltodict.parse(f.read())
    data_keys = list(key_values["data"]["data1"].keys())
    rows = len(key_values["data"].keys())
    csv_str = ",".join(data_keys)
    for i in range(rows):
        data_values = list(key_values["data"]["data"+str(i+1)].values())
        for i in range(len(data_values)):
            data_values[i] = "\"" + data_values[i] + "\""
        csv_str += "\n" + ",".join(data_values)

reversedString=''.join(reversed(filePath))
first_index = reversedString.index(".")
reversedString = "vsc" + reversedString[first_index:]
filePath = ''.join(reversed(reversedString))

f = open(filePath, "w+")
f.write(csv_str)
f.close()