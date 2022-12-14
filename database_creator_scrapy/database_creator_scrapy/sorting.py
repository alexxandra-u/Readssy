import json

with open('../items.json') as json_file:
    data = [json.load(json_file)]
    data = sorted(data, key=lambda x: x["rating"])
    print(data)
