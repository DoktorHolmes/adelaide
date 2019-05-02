import json
with open("Nick_Vent.txt", "rb") as fin:
    content = json.loads(fin)
with open("nickJson.txt", "wb") as fout:
    json.dumps(content, fout, indent=1)
