import sys
import json

filePath = sys.argv[1]

f = open(filePath, "r")

data = json.load(f)
f.close()

first_data = data["data"][0]
rows = len(data["data"])
data_keys = list(first_data.keys())

csv_string = ",".join(data_keys)

for i in range(rows):
    dict_values = list(data["data"][i].values())
    for i in range(len(dict_values)):
        dict_values[i] = "\"" + dict_values[i] + "\""
    csv_string += "\n" + ",".join(dict_values)

reversedString=''.join(reversed(filePath))
first_index = reversedString.index(".")
reversedString = "vsc" + reversedString[first_index:]
filePath = ''.join(reversed(reversedString))

f = open(filePath, "w+")
f.write(csv_string)
f.close()