from os import write
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


def authenticate():
    """ Авторизация клиента
    """
    account_name = input('Введите Ваше имя: ')
    password = input('Введите пароль: ')
    action = 'authenticate'
    create_msg = {
        'action': action,
        'time': time.time(),
        'user': {'account_name': account_name, 'password': password},
    }
    return create_msg


def presence(user, action):
    create_msg = {
        'action': action,
        'time': time.time(),
        'user': user,
    }
    logger.info('the client sent a presence request to the server')
    return create_msg


def create_message(user, action):
    """ Создание сообщения в чат/клиенту
    """
    logger.info('create message length started')
    to = input('Ведите имя получателя: ')
    message = input('Введите сообщение: ')

    create_msg = {
        'action': action,
        'time': time.time(),
        'from': user,
        'to': to,
        'message': message,
    }

    return create_msg


def quit_server(user, action):
    """ Запрос на отключение от сервера
    """
    create_msg = {
        'action': action,
        'time': time.time(),
        'user': user,
    }
    return create_msg


def join(user, action, chat_name):
    """ Запрос на присоединение к чату
    """
    create_msg = {
        'action': action,
        'time': time.time(),
        'from': user,
        'chat_name': chat_name}  # доделать чат
    return create_msg


def message_from_server(create_msg, s):
    """ Отправка сообщения серверу/получение ответа
    """
    s.send(pickle.dumps(create_msg))
    data = s.recv(1024)
    logger.info('Сообщение от сервера: ', pickle.loads(data))
    print('Сообщение от сервера: ', pickle.loads(data))


def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    with socket(AF_INET, SOCK_STREAM) as s:  # Создать сокет TCP
        logger.info('client socket created successfully')
        s.connect((namespace.addr, int(namespace.port)))

        status_auth = False
        while True:
            if status_auth == False:
                print('Для начала пройдите авторизацию')
                create_msg = authenticate()
                status_auth = True
                user = create_msg['user']['account_name']
                message_from_server(create_msg, s)

            if status_auth == True:
                action = input(
                    'Введите команду (presence, msg, quit, join, leave, create): ')

                if action == 'msg':
                    create_msg = create_message(user, action)
                    message_from_server(create_msg, s)

                if action == 'quit':
                    create_msg = quit_server(user, action)
                    message_from_server(create_msg, s)

                if action == 'join':
                    create_msg = join(user, action, chat_name='#')
                    message_from_server(create_msg, s)
                    # пока общий чат

                if action == 'presence':
                    create_msg = presence(user, action)
                    message_from_server(create_msg, s)


if __name__ == '__main__':
    try:
        print('Клиент запущен!')
        logger.warning('Клиент запущен!')
        main()
    except Exception as e:
        logger.critical('Unhandled exception: ', e)
