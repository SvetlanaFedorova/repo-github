import socket
import pickle
import unittest


def creat_connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8888))

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


new_connect = creat_connect()


class TestClient(unittest.TestCase):
    def test_get_authentication(self):
        self.assertFalse(creat_connect())


if __name__ == '__main__':
    unittest.main()
