import csv
import re


''' 1.	Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных
данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV.
Для этого:
a.	Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие
и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь
значения параметров «Изготовитель системы»,  «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка — например,
os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции создать главный список для
хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета в виде списка:
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов также
оформить в виде списка и поместить в файл main_data(также для каждого файла)
b.	Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать
получение данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий
CSV-файл
c.	Проверить работу программы через вызов функции write_to_csv().'''


def get_data(file_name):
    os_code_list = []
    os_name_list = []
    os_prod_list = []
    os_type_list = []

    with open(file_name) as f_n:
        for el_str in f_n:
            rezult = re.match(r'Изготовитель системы:', el_str)
            if rezult:
                my_str = re.findall(r':\w+', el_str).group(0)
                os_prod_list.append(my_str)

            rezult = re.match(r'Название ОС:', el_str)
            if rezult:
                my_str = re.findall(r':\w+', el_str).group(0)
                os_name_list.append(my_str)

            rezult = re.match(r'Код продукта:', el_str)
            if rezult:
                my_str = re.findall(r':\w+', el_str).group(0)
                os_code_list.append(my_str)

            rezult = re.match(r'Тип системы:', el_str)
            if rezult:
                my_str = re.findall(r':\w+', el_str).group(0)
                os_type_list.append(my_str)

    main_data = ['Изготовитель системы',
                 'Название ОС', 'Код продукта', 'Тип системы']

    main_list_items = [main_data, os_prod_list,
                       os_name_list, os_code_list, os_type_list]

    return main_list_items


def write_to_csv():
    with open('main_data.csv', 'w', newline='') as f_n:
        fieldnames = ['info_1.txt', 'info_2.txt', 'info_3.txt']
        for file_name in fieldnames:
            data = get_data(file_name)
            f_n_writer = csv.DictWriter(f_n, fieldnames=fieldnames)
            f_n_writer.writerow({file_name: data})

    with open('main_data.csv') as f_n:
        print(f_n.read())


result_fun = write_to_csv()
