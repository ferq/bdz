__author__ = 'ferq'

# -*- coding: utf-8 -*-
from Tkinter import *
import socket
import sys
import time
import threading
import itertools

myhash=0
resultfound=0
#filename='real_dict.txt'
filename='test_dict.txt'
IP1=0
ipadr=0
port=0
conn=0
addr=0
clients=[]
sock=0
client_connect=0
client_disconnect=0
scetchik_of_users=1

client_interval={}
Wait_Client=0

sdict=''
dict=[]
dict_status={}
dict_client={}
dict_sent=False

dict_brut=[]
dict_brut_status={}
dict_brut_client={}

dict_conn_addr={}

letters='1234567890-=qwertyuiop[]asdfghjkl;zxcvbnm,./!$%^&*()_QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?`'
stroka=''
the_end=0

i=4
while i<=16:
    for elem in letters:
        if i>=10:
            stroka=str(i)+'_'+elem
        else:
            stroka='0'+str(i)+'_'+elem
        dict_brut.append(stroka)
    i+=1
for elem in dict_brut:
    dict_brut_status[elem]=0
    dict_brut_client[elem]=0

def BruteLALALA(charset, length):
    return (''.join(candidate)
        for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
        for i in range(1, length + 1)))

def Master_Of_Settings():
    global myhash
    global entry_Hash
    global text_Process
    global filename
    global button_Start
    global button_Stop
    global button_Add_dict
    global button_Add_IP_users

    myhash = entry_Hash.get()
    if (len(myhash))!=32:
        text_Process.set('wrong hash')
        return 0

    global ipadr
    global port
    global sock
    try:
        ipadr = entry_IP.get()
        port = entry_Port.get()
        sock = socket.socket()
        sock.bind((ipadr, int(port)))
        sock.close()
    except Exception as e:
        print(e)
        text_Process.set('wrong address')
        return 0
    ReadDictionary()
    Online()
    Wait_Client = ThreadWait()
    Wait_Result = ThreadWaitResult()
    Wait_Client.start()
    Wait_Result.start()
    text_Process.set('server was created')
    button_Start.place(x=-1000,y=-1000)
    button_Add_dict.place(x=-1000,y=-1000)
    button_Add_IP_users.place(x=-1000,y=-1000)
    button_Stop.place(x=0,y=0)

def Online():
    global sock

    sock = socket.socket()
    sock.bind((ipadr, int(port)))
    sock.listen(1)

def WaitForClient():
    global conn
    global addr
    global clients
    global sock
    global client_connect
    global scetchik_of_users

    conn, addr = sock.accept()
    clients.append(conn)
    dict_conn_addr[conn]=scetchik_of_users
    scetchik_of_users=scetchik_of_users+1
    text_Process.set('connected:'+str(addr))
    client_connect=1

def ReadDictionary():
    global dict
    global dict_status
    global dict_done
    global sdict
    dict_done=0

    if (filename!='0'):
        f = open(filename, 'r')
        sdict = sdict + f.read()
        dict = sdict.split('|')
        f.close()

    dict+=list(BruteLALALA(letters,3))
    for element in dict:
        dict_status[element]=0
        dict_client[element]=0
    dict_done=1

def ClientDisconnect(client):
        global clients
        global dict
        global dict_status
        global dict_client

        try:
            clients.remove(client)
        except:
            pass
        userid=dict_conn_addr[client]
        text_Process.set('something disconnect')

        for element in dict:
            if (dict_client[element]==userid):
                dict_status[element]=0
                dict_client[element]=0
        for element in dict_brut:
            if (dict_brut_client[element]==userid):
                dict_brut_status[element]=0
                dict_client[element]=0
                break

def On_Client_Connected(conn):
    global client_connect
    global  dict_sent
    client_connect=0
    try:
        conn.send('Service:HASH|'+myhash)
        time.sleep(1)
    except:
        ClientDisconnect(conn)
    dict_current_client=''
    i=0
    userid=dict_conn_addr[conn]
    while (i<10000):
        try:
            if dict_sent==False:
                for element in dict:
                    if (dict_status[element]==0):
                        dict_current_client+=element+'|'
                        dict_status[element]=1
                        dict_client[element]=userid
                        i=i+1
                        if element==dict[-1]:
                            dict_sent=True
                        if (i==10000) or element==dict[-1]:
                            try:
                                conn.send('Service:DICT|'+dict_current_client)
                            except:
                                ClientDisconnect(conn)
                            break
                if dict_sent==True:
                    break
            if dict_sent==True:
                for element in dict_brut:
                    if (dict_brut_status[element]==0):
                        dict_brut_status[element]=1
                        dict_brut_client[element]=userid
                        try:
                            time.sleep(1)
                            conn.send('Service:INFO_BRUT|'+element)
                            i=10000
                            break
                        except:
                            ClientDisconnect(conn)
                            i=10000
                            break
        except:
            pass

def Result_from_client(client):
    global dict_status
    global dict_client

    userid=dict_conn_addr[conn]
    while True:
        try:
            for element in dict:
                if (dict_client[element]==userid):
                    dict_status[element]=2
                    dict_client[element]=0
            for element in dict_brut:
                if (dict_brut_client[element]==userid):
                    dict_brut_status[element]=2
                    dict_brut_client[element]=0
            break
        except:
            pass

def Result_Found(result):
    global the_end
    text_Process.set('Result was found = '+result)
    for client in clients:
        try:
            client.send('Service:STOP')
        except:
            pass
    the_end=1

class ThreadWait(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.daemon = True
        def run(self):
            while True:
                if (resultfound==1):
                    exit()
                WaitForClient()
                if (client_connect==1):
                    global conn
                    On_Client_Connected(conn)

class ThreadWaitResult(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.daemon = True

        def run(self):
            data=''
            global resultfound
            while True:
                for client in clients:
                    try:
                        data=client.recv(1024)
                    except:
                        k=0
                        ClientDisconnect(client)
                    data_correct=data.split('|')
                    if (data_correct[0]=='Service:RESULTFOUND'):
                        resultfound=1
                        Result_Found(data_correct[1])
                        break
                    if (data_correct[0]=='Service:RESULT'):
                        Result_from_client(client)
                    if (data_correct[0]=='Service:NEED_DATA'):
                        On_Client_Connected(client)

def create_server(event):
    global Wait_Client

    Master_Of_Settings()

def stop_brut(event):
    pass

def add_ip(event):
    pass

def add_dict(event):
    global sdict
    try:
        f = open(entry_Add_dict.get(), 'r')
        sdict = f.read()
        f.close()
        text_Process.set('slovar loaded')
        button_Add_dict.place(x=-1000,y=-1000)
    except:
        text_Process.set('neverniy adress')

IP1 = socket.gethostbyname(socket.gethostname())

root=Tk()

root.title('Brutim :O')
root.geometry('550x400+300+200')
root.resizable(False, False)

label_Welcome = Label(text="Privetiki. Vvedi hash, IP i port. Recomendyem: "+IP1)
label_Welcome.place(x=130, y=35)

entry_IP = Entry()
entry_IP.insert(0, "vvedi zdes' IP")
entry_IP.place(x=170, y=70)

entry_Port = Entry()
entry_Port.place(x=170, y=100)
entry_Port.insert(0, "vvedi zdes' Port")

entry_Hash = Entry()
entry_Hash.place(x=170, y=130)
entry_Hash.insert(0, "vvedi zdes' hash")

entry_Add_IP_users = Entry()
entry_Add_IP_users.place(x=150, y=275)
entry_Add_IP_users.insert(0, "Add IP user")

entry_Add_dict = Entry()
entry_Add_dict.place(x=150, y=200)
entry_Add_dict.insert(0, "Way to DICT")

button_Start = Button(root, bg="orange",text="START!",width=15,height=4)
button_Start.place(x=0,y=70)
button_Start.bind('<Button-1>', create_server)

button_Stop = Button(root, bg="red", text="STOP IT!", width=15,height=4)
button_Stop.place(x=-1000,y=-1000)
button_Stop.bind('<Button-1>', stop_brut)

button_Add_dict = Button(root, bg="grey", text="Add Dict", width=15,height=4)
button_Add_dict.place(x=0, y=180)
button_Add_dict.bind('<Button-1>', add_dict)

button_Add_IP_users = Button(root, bg="grey", text="Add User", width=15,height=4)
button_Add_IP_users.place(x=0,y=250)
button_Add_IP_users.bind('<Button-1>', add_ip)

text_Process=StringVar()
label_Process = Label(textvariable=text_Process)
label_Process.place(x=350, y=120)

root.mainloop()