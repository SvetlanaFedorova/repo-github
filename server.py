import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 7777))
s.listen(5)
n = 0
while n < 3:
    try:
        client, addr = s.accept()
    except KeyboardInterrupt:
        s.close()
        break
    else:
        data = client.recv(1024)
        if pickle.loads(data) == 'y':
            print(f'Получен запрос на отключение {client}')
            response = {
                "action": "quit"
            }
            client.send(pickle.dumps(response))
            n += 1
        else:
            print(pickle.loads(data))
            response = {
                "response": 200,
                "alert": "Все OK!"
            }
            client.send(pickle.dumps(response))
            n += 1
