import requests, sys, os

url = sys.argv[1]
mainfile = sys.argv[2]
latest = requests.get(url)

if os.path.isfile(mainfile):
    os.remove(mainfile)
file = open(mainfile, "wb")
file.write(latest.content)
file.close()

input("Успешное обновление. Можете запускать прогу")