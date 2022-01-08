import requests, sys, os, subprocess

url = sys.argv[0]
mainfile = sys.argv[1]
latest = requests.get(url)

os.remove(mainfile)
file = open(mainfile, "rb")
file.write(latest.content)
file.close()

subprocess.Popen([mainfile], close_fds=True)
exit(0)