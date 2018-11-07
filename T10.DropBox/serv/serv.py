import os
import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import time
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2k'

index_list = []

def set_index():
    files = dbx.files_list_folder('').entries

    t = 0
    for i in files:
        i = i.name.split('_')
        if(i[0] == 'entrada'):
            t += 1
    
    print('SERV> Synchronizing with', t, 'clients')
    while(len(index_list) != t):
        index_list.append(0)

def send_(msg, m_id):
    for i in range(0, len(index_list)):
        if(i != m_id):
            md, res = dbx.files_download('/entrada_'+str(i)+'.txt')
            data = (res.content).decode(encoding="ascii", errors="ignore")
            data += msg

            f = open('temp', 'w')
            f.write(data)
            f.close()
            
            f = open('temp', 'rb')
            dbx.files_upload(f.read(), '/entrada_'+str(i)+'.txt', mode=WriteMode('overwrite'))
            print('SERV> CLI#'+str(m_id) + ' Sending msg to CLI#' + str(i))

def sync():
    set_index()
    for i in range(0, len(index_list)):
        md, res = dbx.files_download('/saida_'+str(i)+'.txt')
        data = (res.content).decode(encoding="ascii", errors="ignore")
        data = data.split('\n')

        msg = ''
        while(index_list[i] < len(data)-1):
            msg += data[index_list[i]] + '\n'
            index_list[i] += 1

        if(msg != ''):
            send_(msg, i)
        

def printMsg(msg):
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)
    print(msg)

if __name__ == '__main__':
    dbx = dropbox.Dropbox('4mC_DRyJKlYAAAAAAAABcIXFKiWcwtTjss1An0RpWFql0x7JKN05fTbUtzncI6pG')
    print('SVR> Estabelecendo conexão')
    dbx.users_get_current_account()
    printMsg('SVR> Estabelecendo conexão.')

    while(True):
        sync()