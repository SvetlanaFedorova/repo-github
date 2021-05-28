import pickle
from socket import socket, AF_INET, SOCK_STREAM
import time
import sys
import argparse
import logging
import server_log_config
import select

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
        return {'response': 404, 'time': time.time(), 'error': f'Неизвестная команда {action}'}
    processing_the_action = dict_of_commands[action]  # находим в словаре
    return processing_the_action(**data)  # выполняем нужную ф-цию


authorized_users = []
chat_rooms = {}


def authenticate(**kwargs):  # авторизация на сервере
    user_name = kwargs['user']['account_name']
    response = {'response': 200, 'time': time.time(
    ), 'alert': f'Пользователь {user_name} успешно авторизован'}
    if user_name in authorized_users:
        response = {
            'response': 409,
            'time': time.time(),
            'alert': f'Уже имеется подключение с указанным логином {user_name}',
        }
        logger.error(response)
        return response
    authorized_users.append(user_name)
    logger.info(response)
    return response


def presence(**kwargs):  # присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online
    user_name = kwargs['user']['account_name']
    response = {'response': 404, 'time': time.time(
    ), 'error': f'Пользователь {user_name} отсутствует на сервере', }
    if user_name in authorized_users:
        response = {
            'response': 200,
            'time': time.time(),
            'alert': f'Хорошо, {user_name} приветствуется'
        }
        logger.info(response)
        return response
    logger.error(response)
    return response


def msg(**kwargs):  # простое сообщение пользователю или в чат
    from_user = kwargs['from']
    to_user = kwargs['to']
    message = kwargs['message']

    msg_user_to_user = {
        'from': from_user,
        'to': to_user,
        'message': message}

    msg_log_200 = {
        'response': 200,
        'time': time.time(),
        'alert': f'Сообщение от {from_user} успешно доставлено в чат {chat_rooms}'
    }

    if from_user not in authorized_users:
        response = {'response': 401, 'time': time.time(
        ), 'alert': f'Пользователь {from_user} не авторизован'}
        logger.info(response)
        return response

    if to_user[0] == '#':
        chat = to_user[1:]
        if chat not in chat_rooms:
            response = {'response': 404, 'time': time.time(
            ), 'error': f'Чат {chat} отсутствует на сервере'}
            logger.info(response)
            return response

        logger.info(msg_log_200)
        return msg_user_to_user

    if to_user not in authorized_users:
        response = {'response': 404, 'time': time.time(
        ), 'alert': f'Пользователь {to_user} не авторизован'}
        logger.info(response)
        return response

    logger.info(msg_log_200)
    return msg_user_to_user


def quit_my(**kwargs):  # отключение от сервера
    user_name = kwargs['user']['account_name']
    if user_name in authorized_users:
        return {'response': 200, 'time': time.time(), 'alert': f'Пользователь {user_name} отключился от сервера'}
    return {'response': 404, 'time': time.time(), 'error': f'Пользователь {user_name} не авторизован'}


def join(**kwargs):  # присоединиться к чату
    chat_name = kwargs['chat_name']
    user = kwargs['from']
    if user not in authorized_users:
        return {'response': 404, 'time': time.time(), 'error': f'Пользователь {user} не авторизован'}
    if chat_name in chat_rooms:
        if user not in chat_rooms[chat_name]:
            chat_rooms[chat_name].append(user)
            return {
                'response': 200,
                'time': time.time(),
                'alert': f'Пользователь {user} добавлен в {chat_name}',
            }
        return {
            'response': 409,
            'time': time.time(),
            'error': f'Пользователь {user}, уже присутствует в чате {chat_name},'
        }
    return {
        'response': 409,
        'time': time.time(),
        'error': f'Чат {chat_name} пока не создан'
    }


def leave(**kwargs):  # покинуть чат
    chat_name = kwargs['chat_name']
    user = kwargs['from']
    if user not in authorized_users:
        return {'response': 404, 'time': time.time(), 'error': f'Пользователь {user} не авторизован'}
    if chat_name in chat_rooms:
        if user in chat_rooms[chat_name]:
            chat_rooms[chat_name].remove(user)
            return {
                'response': 200,
                'time': time.time(),
                'alert': f'Пользователь {user} удален из {chat_name}',
            }
        return {
            'response': 409,
            'time': time.time(),
            'error': f'Пользователя {user}, нет в чате {chat_name} ',
        }
    return {
        'response': 409,
        'time': time.time(),
        'error': f'Чат {chat_name} пока не создан',
    }


def create(**kwargs):  # создание чата
    chat_name = kwargs['chat_name']
    user = kwargs['from']
    if user not in authorized_users:
        return {'response': 404, 'time': time.time(), 'error': f'Пользователь {user} не авторизован'}
    if chat_name in chat_rooms:
        return {
            'response': 409,
            'time': time.time(),
            'alert': f'Уже имеется чат с указанным названием {chat_name}',
        }
    chat_rooms[chat_name] = [user]  # создаем чат и список его участников
    return {'response': 200, 'time': time.time(), 'alert': f'Чат {chat_name} успешно создан'}


def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = sock.recv(1024)
            logger.info(
                f'Сообщение: {pickle.loads(data)} было отправлено {sock}')
            responses[sock] = data
        except:
            logger.error('Клиент отключился нет данных')
            all_clients.remove(sock)

    return responses


def write_responses(requests, w_clients, all_clients):
    """ Эхо-ответ сервера клиентам, от которых были запросы
    """

    for sock in w_clients:
        if sock in requests:
            try:
                resp = checking_data(requests[sock])
                for sock in w_clients:
                    sock.send(pickle.dumps(resp))
            except:  # Сокет недоступен, клиент отключился
                logger.error('Клиент отключился нет данных')
                sock.close()
                all_clients.remove(sock)


def mainloop():
    """ Основной цикл обработки запросов клиентов
    """
    parser = createParser()
    namespase = parser.parse_args(sys.argv[1:])
    clients = []

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((namespase.addr, int(namespase.port)))
    s.listen(5)
    s.settimeout(0.2)  # Таймаут для операций с сокетом
    while True:
        try:
            conn, addr = s.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            print("Получен запрос на соединение от %s" % str(addr))

            logger.info("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 10
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился

            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            if requests:
                # Выполним отправку ответов клиентам
                write_responses(requests, w, clients)


if __name__ == '__main__':
    try:
        print('Сервер запущен!')
        logger.warning('Сервер запущен!')
        mainloop()
    except Exception as e:
        logger.critical('Unhandled exception: ', e)
