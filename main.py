import requests, antiddos, adminparser as parser, datetime, sys, os
from admins import Admin, AdminDaemon as AD

def sortAdmins(admin):
    return admin.get_all()

def printStat(daemon):
    i = 1
    for admin in daemon.admins:
        print(f"[{i}] " + admin.nick+": ", admin.get_all())
        i += 1

def printDetailAdmin(admin : Admin):
    print(f"Администратор [{admin.nick}]")
    print("Всего наказаний за период:", admin.get_all())
    allbans = admin.bans["C"] + admin.bans["HC"] + admin.bans["R"] + admin.bans["HR"]
    print(f"Наказания по типам\n  B: {allbans}\n  W: {admin.warns}\n  J: {admin.jails}\n  N: {admin.namebans}")
    print(f"Баны по категориям")
    for category in admin.bans:
        print(f"  [{category}] : {admin.bans[category]}")
    print(f"Разбанов (лично админ разбанил):", admin.unbans)

############
SERVER = "rpg"
servers = {"rpg" : "rpg", "rp1" : "rp", "rp2": "rp2"}

mon = datetime.datetime.today().strftime("%m")

parse_n = 1000
if "-s" in sys.argv:
    SERVER = sys.argv[sys.argv.index("-s")+1]
if SERVER not in servers:
    print("Укажите корректно сервер: [rpg | rp1 | rp2]")
    input()
    exit(1)
SERVER = servers[SERVER]
if "-m" in sys.argv:
    mon = sys.argv[sys.argv.index("-m")+1]
if "-n" in sys.argv:
    parse_n = int(sys.argv[sys.argv.index("-n")+1])
############
print("server: ", SERVER, ", mounth: ", mon, ", parse_n: ", parse_n)
print("Starting...")

S = requests.Session()

resp = S.get("https://gta-trinity.ru/")
code = antiddos.get(resp.text)

cookies = dict(
    name='REACTLABSPROTECTION',
    value=code,
    path='/',
    domain='gta-trinity.ru',
    expires=2145916555,
    rest = {'hostOnly':True}
)
S.cookies.set(**cookies)

data = S.get(f"https://gta-trinity.ru/{SERVER}mon/bans.php").text

P = parser.Parser(data)
P.parse(parse_n)

daemon = AD()
tocount = 0
skipped = 0
for string in P.parsed_data:
    #Смотрим за указанный месяц
    if mon == string.date.strftime("%m"):
        daemon.add(string.admin, string.action, string.category)
        tocount += 1
    else:
        skipped += 1
daemon.admins.sort(key = sortAdmins, reverse=True)
exitflag = True
while exitflag:
    printStat(daemon)
    inp = input("\nВведите порядковый номер админа для подробной инфы, 'e' для выхода:\n")
    if inp == 'e':
        exitflag = False
        continue
    elif inp.isdigit():
        num = int(inp)
        if daemon.admins[num-1]:
            printDetailAdmin(daemon.admins[num-1])
            input()
        else:
            print("Админа под таким номером не найдено")
            input()
    else:
        print("Команда не распознана")
        input()
    os.system("cls")