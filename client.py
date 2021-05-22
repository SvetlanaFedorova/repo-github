import pickle
from socket import socket, AF_INET, SOCK_STREAM
import time
import sys
import argparse
import logging
import log.client_log_config

logger = logging.getLogger('client_log')


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default="7777")
    parser.add_argument("-a", "--addr", default="127.0.0.1")
    parser.error = myerror
    logger.info('parser created successfully')
    return parser


def myerror(message_str):
    print(f'Применен недопустимый аргумент {message_str}')


def create_message():
    logger.info('create message length started')
    action = input(
        'Введите команду (authenticate, presence, msg, quit, join, leave, create): ')
    account_name = input('Введите имя: ')
    password = input('Введите пароль: ')
    msg = {
        'action': action,
        'time': time.time(),
        'user': {'account_name': account_name, 'password': password}
    }
    logger.info('message creation completed successfully')
    return msg


def main():
    logger.info('main function started')
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    s = socket(AF_INET, SOCK_STREAM)
    logger.info('client socket created successfully')
    s.connect((namespace.addr, int(namespace.port)))
    n = 0
    while n < 3:
        n = n + 1
        msg = create_message()
        s.send(pickle.dumps(msg))
        data = s.recv(1024)
        print('Сообщение от сервера: ', pickle.loads(data))
        s.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical('Unhandled exception: ', e)
