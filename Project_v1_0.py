import random
from PyQt5.QtWidgets import *
from PyQt5 import uic

category_list = []  # список со всеми категориями
users = {}  # словарь со всмеи пользователями вида "'логин':экземляр класса User, соответствующему этому логину"
korzina = {}  # словарь со всеми товарами, которые находятся в корзине вида "'экземпляр класса Product':кол-во товара находящеесе в корзине"


# CЛУЖЕБНЫЕ КЛАССЫ/ИСКЛЮЧЕНИЯ:

# исключение для фунции correct_ending_of_numerals_shtuki, возникает когда передается отрицательное число или вообще не число
class ZeroNumeral(Exception):
    pass


# СЛУЖЕБНЫЕ ФУНКЦИИ:

# генератор паролей
def password_generate():
    password = ''
    for i in range(random.randint(6, 8)):
        var = random.randint(0, 8)
        if 0 <= var <= 4:
            a = random.randint(65, 122)
            while 90 < a < 97:
                a = random.randint(65, 122)
            a = chr(a)
            if random.randint(0, 1) == 0:
                a = a.upper()
        elif 5 <= var <= 7:
            a = chr(random.randint(48, 57))
        else:
            if random.randint(0, 1) == 0:
                a = '?'
            else:
                a = '!'
        password += a
    return password


# возврат правильных окончаний слова "штука" в зависимости от числа
def correct_ending_of_numerals_shtuki(numeral):  # в аргумент numeral передается 'число штук'
    numeral = str(numeral)
    dlina = len(numeral)
    if not numeral.isdigit():
        raise ZeroNumeral('Функция correct_ending_of_numerals. Число меньше 0 или число отсутствует')
    elif (dlina > 1 and numeral[-2:] == '11') or numeral[-1] == '0' or 5 <= int(numeral[-1]) <= 6:
        return 'штук'
    elif numeral[-1] == '1':
        return 'штука'
    else:
        return 'штуки'


# АВТОРИЗАЦИЯ

# начальная страница входа в аккаунт пользователя
def vhod():
    global users
    false_login_password = False
    login = input()  # вводится в поле для ввода
    password = input()  # вводится в поле для ввода
    if login in users:
        true_password = users[login].return_password()
        if password == true_password:
            print('открываем дальнейшее меню')  # открываем дальнейшее меню
        else:
            false_login_password = True
    else:
        false_login_password = True
    if false_login_password:
        print('неверный логин или пароль')  # вывод: "неверный логин или пароль"


# создание нового пользователя
def new_user():
    login = input()  # вводится в поле для ввода
    password = input()  # вводится в поле для ввода
    prava_dostupa = input()  # выберается из преложенных вариантов
    user_class = User(login, password, prava_dostupa)
    users[login] = user_class


# добавление новой категории
def new_category():
    name = input()  # вводится в поле для ввода
    color = input()  # вводится в поле для ввода
    new_pr_category = Category(name, color)
    category_list.append(new_pr_category)


# создание нового продукта
def new_product(category):  # в аргумент "category" передается экземплчр класса категории (Category)
    name = input()  # вводится в поле для ввода
    kolvo = input()  # кол-во товара на складе, вводится в поле для ввода
    new_pr_product = Product(name, kolvo)
    category.add_product(new_pr_product)


# добавление товара в корзину
def adding_to_korzina(product,
                      kolvo=1):  # в аргумент product передается экземляр класс Product, в kolvo - колличество товара (по умолчанию = 1)
    a = product.buying_products(kolvo)
    if a:
        product_name = product.return_name()
        korzina[product] = kolvo
        # товар добавляется в корзину и отображается слева в блоке корзины (в списке корзины)
    else:
        ostatok_na_sklade = product.return_kolvo()
        if ostatok_na_sklade == 0:
            print('На складе не осталось такого товара')
        else:
            word_shtuk = correct_ending_of_numerals_shtuki(ostatok_na_sklade)  # слово "штук" с правильным окончанием
            print('Недостаточно товара на складе. на складе осталось:', ostatok_na_sklade, word_shtuk)


# удаление товара из корзины
def removing_from_korzina(product,
                          kolvo=1):  # в аргумент product передается экземляр класс Product, в kolvo - колличество товара (по умолчанию = 1):
    product.returning(kolvo)


# класс пользователя
class User:
    def __init__(self, login, password, prava_dostupa):
        self.login = login
        self.password = password
        self.prava_dostupa = prava_dostupa

    def return_password(self):
        return self.password

    def return_prava(self):
        return self.prava_dostupa


# класс категории
class Category:
    def __init__(self, name, color):
        self.sp_productes = []
        self.name = name
        self.color = color

    def return_color(self):
        return self.color

    def return_name(self):
        return self.name

    def add_product(self, product):
        self.sp_productes.append(product)


# класс продукта
class Product:
    def __init__(self, name, kolvo):
        self.name = name
        self.kolvo = kolvo

    def return_name(self):
        return self.name

    def return_kolvo(self):
        return self.kolvo

    def buying(self, kolvo=1):  # уменьшение кол-ва товара на складе при добавление товара в корзину
        if kolvo <= self.kolvo:
            self.kolvo -= kolvo
            return True  # если на кладе есть нужное для покупки кол-во товара - функция вернёт True
        else:
            return False  # если на складе нет нужного кол-ва товара для покупки - функция вернёт False

    def returning(self, kolvo=1):  # увеличение кол-ва товара на складе при удалении товара из корзины
        self.kolvo += kolvo


