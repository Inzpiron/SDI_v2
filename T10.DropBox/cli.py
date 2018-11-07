import os
import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import time
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2k'

def getId():
    files = dbx.files_list_folder('').entries

    t = 0
    for i in files:
        i = i.name.split('_')
        if(i[0] == 'entrada'):
            t += 1

    return t

def printMsg(msg):
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)
    print(msg)

def writer():
    f = open(arqSaida, 'rb')
    dbx.files_upload(f.read(), '/'+arqSaida, mode=WriteMode('overwrite'))
    f.close()

    while True:
        msg = input()
        printMsg(name + '> ' +msg)

        f = open(arqSaida, 'a')
        f.write(name+'#'+str(myId)+'> '+msg + '\n')
        f.close()

        f = open(arqSaida, 'rb')
        dbx.files_upload(f.read(), '/'+arqSaida, mode=WriteMode('overwrite'))
        f.close()

def reader():
    f = open(arqEntrada, 'rb')
    dbx.files_upload(f.read(), '/'+arqEntrada, mode=WriteMode('overwrite'))
    f.close()

    line_index = 0
    while True:
        time.sleep(1)
        md, res = dbx.files_download('/'+arqEntrada)
        data = (res.content).decode(encoding="ascii", errors="ignore")
        data = data.split('\n')

        while(line_index < len(data)-1):
            print(data[line_index])
            line_index += 1

if __name__ == '__main__':
    name = sys.argv[1]
    dbx = dropbox.Dropbox('4mC_DRyJKlYAAAAAAAABcIXFKiWcwtTjss1An0RpWFql0x7JKN05fTbUtzncI6pG')
    print('SVR> Estabelecendo conexão')
    dbx.users_get_current_account()
    printMsg('SVR> Estabelecendo conexão.')

    myId = getId()
    arqSaida = 'saida_'+str(myId) + '.txt'
    arqEntrada = 'entrada_'+str(myId) + '.txt'
    f = open(arqSaida, 'w+')
    f.close()
    f = open(arqEntrada, 'w+')
    f.close()

    newpid = os.fork()
    if(newpid == 0):
        reader()
    else:
        writer()
