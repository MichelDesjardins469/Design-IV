import json

f = open("values.json")

data = json.load(f)

print(data["Capteurs"]["Temperature"])

data["Capteurs"]["CO2"] = 1000

json_object = json.dumps(data, indent=len(data))

with open("values.json", "w") as outputfile:
    outputfile.write(json_object)
