import os, json

DIR = "sets/"
SETS = {
    "update_url" : "https://raw.githubusercontent.com/pap1k/adminstat-dist/master/version.json",
    "parse": 1000,
    "server": "rpg"
}
if not os.path.isdir(DIR):
    os.makedirs(DIR)

if os.path.isfile(DIR+"settings.json"):
    txt = open(DIR+"settings.json", "r", encoding="utf-8").read()
    js = json.loads(txt)
    mod = False
    for field in SETS:
        if field not in js:
            mod = True
            js[field] = SETS[field]
    SETS = js
    if mod: open(DIR+"settings.json", "w", encoding="utf-8").write(json.dumps(SETS))
else:
    open(DIR+"settings.json", "w", encoding="utf-8").write(json.dumps(SETS))
