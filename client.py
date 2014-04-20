# -*- coding: utf-8 -*-

import socket
import hashlib
import threading
import time
import itertools

global info_brut

stop=0
resultfound=0
data=''
hash=0
dict=[]
sock=0
info_brut=''
dict_brut=[]

hash_get=0
dict_get=0

letters='1234567890-=qwertyuiop[]asdfghjkl;zxcvbnm,./!$%^&*()_QWERTYUIOPP{}ASDFGHJKL:"ZXCVBNM<>?`'

class WaitForData(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.daemon = True
        def run(self):
            global sock
            global data
            global stop

            while True:
                data = sock.recv(1024*1024)
                DataParser(data)
                time.sleep(1)
                if stop==1:
                    break

def DataParser(data):
    global stop
    global hash_get
    global dict_get
    global hash
    global dict
    global info_brut

    data_correct=data.split('|')
    if (data_correct[0]=='Service:HASH'):
        hash=data_correct[1]
        hash_get=1
    if (data_correct[0]=='Service:DICT'):
        dict=data.split('|')
        dict_get=1
    if (data_correct[0]=='Service:INFO_BRUT'):
        info_brut=str(data_correct[1])
        dict_get=1
    if (data_correct[0]=='Service:STOP'):
        stop=1

# def BruteForce(charset, length):
#     return (''.join(candidate)
#         for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
#         for i in range(length, length + 1)))

#===============================================================================================================
# НАЧАЛО ПРОГРАММЫ
#===============================================================================================================

myip=raw_input('ip:')
port = input('port:')

mode=input('1.nostopping\n2.with stoppig\n')

sock = socket.socket()
sock.connect((myip, port))

t=WaitForData()
t.start()

print('connecting')

while True:
    print('getting data...')
    while True:
        if (dict_get*hash_get!=0):
            break

    print('took it')

    if dict!=[]:
        for element in dict:
            if (stop==0):
                temp_hash=hashlib.md5()
                temp_hash.update(element)
                if (temp_hash.hexdigest()==hash):
                    resultfound=1
                    stop=1
                    print('right word: '+element + '  his hash: '+temp_hash.hexdigest())
                    sock.send('Service:RESULTFOUND|'+element)
                    break
                else:
                    print('wrong word: '+element+' his hash: '+temp_hash.hexdigest())
            else:
                break
    else:
        for entry in itertools.product(letters,repeat = (int(info_brut[0:2])-1)):
            element=info_brut[3]+''.join(entry)
            if (stop==0):
                temp_hash=hashlib.md5()
                temp_hash.update(element)
                if (temp_hash.hexdigest()==hash):
                    resultfound=1
                    stop=1
                    print('right word: '+element + '  his hash: '+temp_hash.hexdigest())
                    sock.send('Service:RESULTFOUND|'+element)
                    break
                else:
                    print('wrong word: '+element+' his hash: '+temp_hash.hexdigest())
            else:
                break

    dict=[]
    if (stop==1):
        if (resultfound==1):
            print('u foung it bitch')
            break
        else:
            print('some user found it')
            break
    else:
        print('ending')
        print('sending result')
        sock.send('Service:RESULT|Not found')
        time.sleep(1)
        print('sent')

        if (mode==2):
            choice=input('1.eshe?\n2.hvatit=(')
            if (choice==2):
                break
        print('zapshena obrabotka sled. pakete)')
        dict_get=0
        hash_get=0
        sock.send('Service:NEED_DATA')
print('LOL')