import requests, antiddos, datetime, sys, os, subprocess
from adminparser import Parser
from sets import SETS
from admins import Admin, AdminDaemon as AD

__version = 0.3

def sortAdmins(admin):
    return admin.get_all()

def printStat(daemon):
    i = 1
    total = 0
    for admin in daemon.admins:
        print(f"[{i}] " + admin.nick+": ", admin.get_all())
        total += admin.get_all()
        i += 1
    print(f"===================\nВсего наказаний: {total}")

def printDetailAdmin(admin : Admin):
    print(f"Администратор [{admin.nick}]")
    print("Всего наказаний за период:", admin.get_all())
    allbans = admin.bans["C"] + admin.bans["HC"] + admin.bans["R"] + admin.bans["HR"]
    print(f"Наказания по типам\n  B: {allbans}\n  W: {admin.warns}\n  J: {admin.jails}\n  N: {admin.namebans}")
    print(f"Баны по категориям")
    for category in admin.bans:
        print(f"  [{category}] : {admin.bans[category]}")
    print(f"Разбанов (лично админ разбанил):", admin.unbans)

##########################
# CHECKING UPDATES
##########################
update_info = requests.get(SETS['update_url']).json()
if float(update_info["v"]) > __version:
    print("==========!!!!!!!!!!!!!!==========")
    print(f"Доступно обновление!\nТекущая версия: {__version}\nНовая версия: {update_info['v']}.\nНововведения:")
    print(update_info["comment"])
    answ = input("\nОбновить сейчас? (y/n): ")
    if answ.lower() in ["y", "д"]:
        subprocess.Popen(["updater.exe", update_info["url"], __file__], close_fds=True)
        exit(0)

##########################
# GETTING ARGS
##########################
SERVER = SETS['server']
servers = {"rpg" : "rpg", "rp1" : "rp", "rp2": "rp2"}
mon = datetime.datetime.today().strftime("%m")
parse_n = SETS['parse']

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

print("server: ", SERVER, ", mounth: ", mon, ", parse_n: ", parse_n)
print("Получение и обработка информации...")

S = requests.Session()

resp = S.get("https://gta-trinity.com/")
code = antiddos.get(resp.text)

cookies = dict(
    name='REACTLABSPROTECTION',
    value=code,
    path='/',
    domain='gta-trinity.com',
    expires=2145916555,
    rest = {'hostOnly':True}
)
S.cookies.set(**cookies)

data = S.get(f"https://gta-trinity.com/{SERVER}mon/bans.php").text

P = Parser(data)
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
    inp = input("\nВведите порядковый номер админа для подробной инфы, 'q' для выхода:\n")
    if inp == 'q':
        exitflag = False
        continue
    elif inp.isdigit():
        num = int(inp)
        if daemon.admins[num-1]:
            os.system("cls")
            printDetailAdmin(daemon.admins[num-1])
        else:
            print("Ошибка: Админа под таким номером не найдено")
    else:
        print("Ошибка: Команда не распознана")
    input()
    os.system("cls")