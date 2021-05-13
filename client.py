import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 7777))

msg = input('Хотите отключиться от сервера? y/n: ')

if msg != 'y':
    msg = {
        "action": "authenticate",
        "time": "<unix timestamp>",
        "user": {
                "account_name":  "C0deMaver1ck",
                "password":      "CorrectHorseBatteryStaple"
        }
    }

s.send(pickle.dumps(msg))
data = s.recv(1024)
print('Сообщение от сервера: ', pickle.loads(data))
s.close()
