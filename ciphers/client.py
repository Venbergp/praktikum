import socket


def pc_key_gen(g, p, Ksc):
    Kpc = str(g ** Ksc % p)
    return Kpc


def total_key_gen(Kps, Ksc, p):
    K = (Kps ** Ksc) % p
    return K


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
    sock.setblocking(1)
    sock.connect(('localhost', 9092))
    # Ksc = 101
    Ksc = int(input('Введите ваш сектретный ключ:'))
    data = sock.recv(1024).decode()
    data = data.split(' ')
    g = int(data[1])
    p = int(data[2])
    Kps = int(data[0])
    Kpc = pc_key_gen(g, p, Ksc)
    print("Ваш приватный ключ сгенерирован")
    sock.send(Kpc.encode())
    K = total_key_gen(Kps, Ksc, p)
    data = sock.recv(1024).decode()
    data = decript(data, K)
    print(data)
    while True:
        msg = input()
        if msg == 'ex':
            break
        else:
            msg = cript(msg, K)

            sock.send(msg.encode())
        try:
            data = sock.recv(1024).decode()
        except:
            print("Сервер остановил разговор")
            break
        data = decript(data, K)
        print(data)
    sock.close()


main()
