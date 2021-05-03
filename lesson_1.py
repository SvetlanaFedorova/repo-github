# 1.	Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
# проверить тип и содержание соответствующих переменных. Затем с помощью онлайн-конвертера
# преобразовать строковые представление в формат Unicode и также проверить тип и содержимое
# переменных.


import locale
import subprocess

print('Задание 1')

variable_1, variable_2, variable_3 = 'разработка', 'сокет', 'декоратор'
print(variable_1, variable_2, variable_3)
print(type(variable_1), type(variable_2), type(variable_3))

variable_1_b, variable_2_b, variable_3_b = variable_1.encode(
    'utf-8'), variable_2.encode('utf-8'), variable_3.encode('utf-8')
print(variable_1_b, variable_2_b, variable_3_b)
print(type(variable_1_b), type(variable_2_b), type(variable_3_b))


# 2.	Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования
# в последовательность кодов (не используя методы encode и decode) и определить тип, содержимое
# и длину соответствующих переменных.

print('Задание 2')

var = ['class', 'function', 'method']
for i in var:
    i = bytes(i, 'utf-8')
    print(type(i), i, len(i))

# 3.	Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать
# в байтовом типе.

print('Задание 3')

var = ['attribute', 'класс', 'функция', 'type']
for i in var:
    b = i.encode('utf-8')
    print(b, type(b))

# 4.	Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
# строкового представления в байтовое и выполнить обратное преобразование
# (используя методы encode и decode).

print('Задание 4')

var = ['разработка', 'администрирование', 'protocol', 'standard']
for i in var:
    b = i.encode('utf-8')
    print(b, type(b))
    s = b.decode('utf-8')
    print(s, type(s))

# 5.	Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
# байтовового в строковый тип на кириллице.

print('Задание 5')

args_y = ['ping', 'yandex.ru']
args_y_ping = subprocess.Popen(args_y, stdout=subprocess.PIPE)
for line in args_y_ping.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'))

args_yt = ['ping', 'youtube.com']
args_yt_ping = subprocess.Popen(args_yt, stdout=subprocess.PIPE)
for line in args_yt_ping.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'))

# 6.Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате
# Unicode и вывести его содержимое.

print('Задание 6')

def_coding = locale.getpreferredencoding()
print(def_coding)

f_n = open("test_file.txt", "w")
content = ['сетевое программирование\n', 'сокет\n', 'декоратор\n']
f_n.writelines(content)
f_n.close()
print(f_n)

with open('test_file.txt', encoding='cp1251') as f_n:
    for el_str in f_n:
        print(el_str)
