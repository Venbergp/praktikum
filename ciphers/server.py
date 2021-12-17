import socket
import csv, os

file = os.path.join(os.getcwd(), 'keys.csv')
with open(os.path.join(os.getcwd(), 'servkeys.csv'), 'r') as f:
    i = 0
    for line in csv.reader(f):
        if i == 0:
            p = int(''.join(line))
        elif i == 1:
            g = int(''.join(line))
        elif i == 2:
            a = int(''.join(line))
        i += 1


def ps_key_gen(conn, p, g):
    with open(os.path.join(os.getcwd(), 'servkeys.csv'), 'r') as f:
        i = 0
        for line in csv.reader(f):
            if i == 3:
                Kps = int(''.join(line))
            i += 1
    msg = str(Kps) + ' ' + str(g) + ' ' + str(p)
    conn.send(msg.encode())
    return Kps


def total_key_gen(Kpc):
    global p, g, a
    K = (int(Kpc) ** a) % p
    return K


def check_ksc(Kpc):
    global file
    with open(file, 'r') as f:
        know = False
        for line in csv.reader(f):
            if Kpc in line:
                know = True
                return True
        if know == False:
            return False


def cript(msg, k):
    msgl = list(msg)
    for i in range(len(msgl)):
        msgl[i] = chr(ord(msgl[i]) + k)
    msg = ''.join(msgl)
    return msg


def decript(msg, k):
    msgl = list(msg)
    for i in range(len(msgl)):
        msgl[i] = chr(ord(msgl[i]) - k)
    msg = ''.join(msgl)
    return msg


def main():
    sock = socket.socket()
    sock.bind(('', 9092))
    sock.listen(0)
    while True:
        conn, addr = sock.accept()
        print(addr)
        ps_key_gen(conn, p, g)
        Kpc = conn.recv(1024).decode()
        print("Client's public key recieved")
        if check_ksc(Kpc) == True:
            print("Клиент найден")
            pass
        else:
            print("Клиент не известен")
            conn.close()
            continue
        print("Ключ сгенерирован")
        K = total_key_gen(Kpc)
        conn.send(cript("Welcome!", K).encode())
        while True:
            try:
                data = conn.recv(1024).decode()
            except:
                break
            data = decript(data, K)
            print(data)
            msg = "Ваше сообщение получено: " + data
            msg = cript(msg, K)
            conn.send(msg.encode())
        conn.close()


main()
