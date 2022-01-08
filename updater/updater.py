import requests, sys, os, subprocess

url = sys.argv[1]
mainfile = sys.argv[2]
latest = requests.get(url)

if os.path.isfile(mainfile):
    os.remove(mainfile)
file = open(mainfile, "wb")
file.write(latest.content)
file.close()

subprocess.Popen([mainfile], close_fds=True)
exit(0)