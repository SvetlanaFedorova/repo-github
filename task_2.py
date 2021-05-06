''' 2.	Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. 
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
a.	Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), 
количество (quantity), цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись 
данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
b.	Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого 
параметра.'''

import json


def write_order_to_json(item, quantity, price, buyer, date):
    dict_to_json = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }
    with open('orders.json', 'w') as f_n:
        json.dump(dict_to_json, f_n, indent=4)


result = write_order_to_json('intel-5', 3, 100, 'tesla', '01.05.2021')
