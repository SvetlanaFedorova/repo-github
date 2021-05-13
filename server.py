import socket
import pickle
import unittest


def get_authentication(data):
    print(pickle.loads(data))
    response = {
        "response": 200,
        "alert": "Все OK!"
    }
    return response


def get_shutdown():
    print('Получен запрос на отключение')
    response = {
        "action": "quit"
    }
    return response


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8888))
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
            client.send(pickle.dumps(get_shutdown()))
            n += 1
        else:
            client.send(pickle.dumps(get_authentication(data)))
            n += 1


class TestServer(unittest.TestCase):
    def test_get_shutdown(self):
        self.assertTrue(get_shutdown())


if __name__ == '__main__':
    unittest.main()
