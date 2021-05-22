import pickle
from socket import socket, AF_INET, SOCK_STREAM
import time
import sys
import argparse
import logging
import log.server_log_config


logger = logging.getLogger('server_log')


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default="7777")
    parser.add_argument("-a", "--addr", default="127.0.0.1")
    parser.error = myerror
    logger.info('parser created successfully')
    return parser


def myerror(message_str):
    print(f'Применен недопустимый аргумент {message_str}')


def checking_data(message_str):
    logger.info('checking message length started')
    if len(message_str) > 640:
        logger.error('error checking message length')
        return {
            'response': 400,
            'time': time.time(),
            'error': "Длина сообщения больше 640 символов"
        }
    dict_of_commands = {
        'authenticate': authenticate,
        'presence': presence,
        'msg': msg,
        'quit': quit_my,
        'join': join,
        'leave': leave,
        'create': create,
    }
    data = pickle.loads(message_str)
    action = data['action']
    if action not in dict_of_commands:
        logger.error('error checking the client_s command')
        return {'response': 404, 'time': time.time(), 'error': f'Неизвестная команда {action}'}
    processing_the_action = dict_of_commands[action]  # находим в словаре
    logger.info('data verification completed successfully')
    return processing_the_action(**data)  # выполняем нужную ф-цию


authorized_users = []
chat_rooms = {}


def authenticate(**kwargs):  # авторизация на сервере
    logger.info('user authentication check started')
    user_name = kwargs['user']['account_name']
    if user_name in authorized_users:
        logging.warning(
            'authentication check failed. Someone is already connected with the given user name')
        return {
            'response': 409,
            'time': time.time(),
            'alert': f'Уже имеется подключение с указанным логином {user_name}',
        }
    authorized_users.append(user_name)
    logger.info('authentication check completed successfully')
    return {'response': 200, 'time': time.time(), 'alert': f'Пользователь {user_name} успешно авторизован'}


def presence(**kwargs):  # присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online
    logger.info('presence check started')
    user_name = kwargs['user']['account_name']
    if user_name in authorized_users:
        logger.info('presence check was successful')
        return {
            'response': 200,
            'time': time.time(),
            'alert': f'Хорошо, {user_name} приветствуется'
        }
    logger.error('presence check failed')
    return {'response': 404, 'time': time.time(), 'error': f'Пользователь {user_name} отсутствует на сервере', }


def msg(**kwargs):  # простое сообщение пользователю или в чат
    logger.info('start sending message')
    from_user = kwargs['from']
    to_user = kwargs['to']
    if from_user not in authorized_users:
        logger.error('presence check failed')
        return {'response': 401, 'time': time.time(), 'alert': f'Пользователь {from_user}не авторизован'}

    if to_user[0] == '#':
        chat = to_user[1:]
        if chat not in chat_rooms:
            logger.error('chat check ended with an error')
            return {'response': 404, 'time': time.time(), 'error': f'Чат {chat} отсутствует на сервере'}

        logger.info('chat verification was successful, message delivered')
        return {
            'response': 200,
            'time': time.time(),
            'alert': f'Сообщение от {from_user} успешно доставлено в чат {chat_rooms}'
        }

    if to_user not in authorized_users:
        logger.error('presence check failed')
        {'response': 404, 'time': time.time(
        ), 'alert': f'Пользователь {to_user} не авторизован'}

    logger.info('chat verification was successful, message delivered')
    return {'response': 200, 'time': time.time(), 'alert': f'Сообщение от {from_user} к {to_user} доставлено'}


def quit_my(**kwargs):  # отключение от сервера
    logger.info('the disconnect from the server function has been initiated')
    user_name = kwargs['user']['account_name']
    if user_name in authorized_users:
        logger.info(
            'the user was successfully disconnected from the server on request')
        authorized_users.remove(user_name)
        return {'response': 200, 'time': time.time(), 'alert': f'Пользователь {user_name} отключился от сервера'}
    logger.error('presence check failed')
    return {'response': 404, 'time': time.time(), 'error': f'Пользователь {user_name} не авторизован'}


def join(**kwargs):  # присоединиться к чату
    logger.info('received a request to join the chat')
    chat_name = kwargs['chat_name']
    user = kwargs['from']
    if user not in authorized_users:
        logger.error('presence check failed')
        return {'response': 404, 'time': time.time(), 'error': f'Пользователь {user} не авторизован'}
    if chat_name in chat_rooms:
        if user not in chat_rooms[chat_name]:
            logger.info('the user was successfully added to the chat')
            chat_rooms[chat_name].append(user)
            return {
                'response': 200,
                'time': time.time(),
                'alert': f'Пользователь {user} добавлен в {chat_name}',
            }
        logging.warning(
            'error adding user to chat. Someone is already connected with the given user name')
        return {
            'response': 409,
            'time': time.time(),
            'error': f'Пользователь {user}, уже присутствует в чате {chat_name},'
        }
    logging.error('error adding user to chat. The chat has not been created')
    return {
        'response': 409,
        'time': time.time(),
        'error': f'Чат {chat_name} пока не создан'
    }


def leave(**kwargs):  # покинуть чат
    logging('a request to leave the chat was received')
    chat_name = kwargs['chat_name']
    user = kwargs['from']
    if user not in authorized_users:
        logger.error('presence check failed')
        return {'response': 404, 'time': time.time(), 'error': f'Пользователь {user} не авторизован'}
    if chat_name in chat_rooms:
        if user in chat_rooms[chat_name]:
            logger.info('the user was successfully removed from the chat')
            chat_rooms[chat_name].remove(user)
            return {
                'response': 200,
                'time': time.time(),
                'alert': f'Пользователь {user} удален из {chat_name}',
            }
        logger.error(
            'the request to delete from the chat was completed with an error. User is not in chat')
        return {
            'response': 409,
            'time': time.time(),
            'error': f'Пользователя {user}, нет в чате {chat_name} ',
        }
    logging.error('error adding user to chat. The chat has not been created')
    return {
        'response': 409,
        'time': time.time(),
        'error': f'Чат {chat_name} пока не создан',
    }


def create(**kwargs):  # создание чата
    logger.info('a request to create a chat was received')
    chat_name = kwargs['chat_name']
    user = kwargs['from']
    if user not in authorized_users:
        logger.error('presence check failed')
        return {'response': 404, 'time': time.time(), 'error': f'Пользователь {user} не авторизован'}
    if chat_name in chat_rooms:
        logger.error(
            'request to start a chat completed with an error. The chat has already been created')
        return {
            'response': 409,
            'time': time.time(),
            'alert': f'Уже имеется чат с указанным названием {chat_name}',
        }
    logger.info('chat request completed successfully. Chat created')
    chat_rooms[chat_name] = [user]  # создаем чат и список его участников
    return {'response': 200, 'time': time.time(), 'alert': f'Чат {chat_name} успешно создан'}


def main():
    logger.info('main function started')
    parser = createParser()
    namespase = parser.parse_args(sys.argv[1:])

    s = socket(AF_INET, SOCK_STREAM)
    logger.info('server socket created successfully')
    s.bind((namespase.addr, int(namespase.port)))
    s.listen(5)
    logger.debug('Старт приложения')

    n = 0
    while n < 3:
        n = n + 1
        client, addr = s.accept()
        message_str = client.recv(1024)
        print('Сообщение: ', pickle.loads(message_str),
              ', было отправлено клиентом ')
        response = checking_data(message_str)
        client.send(pickle.dumps(response))
        client.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical('Unhandled exception: ', e)
