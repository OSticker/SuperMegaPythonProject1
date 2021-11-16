import random
import sys

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
def vhod(login, password):
    global users
    false_login_password = False
    if login in users:
        true_password = users[login].return_password()
        if password == true_password:
            return True  # открываем дальнейшее меню (логин и пароль верны)
        else:
            false_login_password = True
    else:
        false_login_password = True
    if false_login_password:
        return False  # вывод: "неверный логин или пароль"


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
    a = product.buying(kolvo)
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

    def return_products_list(self):
        return self.sp_productes

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


class MainWindow():
    def __init__(self):
        pass

    def show_authtorisation(self):
        new_user()
        self.w_authtorisation = Authtorisation()
        self.w_authtorisation.show()

    def close_authtorisation(self):
        self.w_authtorisation.close()

    def show_vivod_categoryes(self):
        for _ in range(6):
            new_category()
            for _ in range(2):
                category_list[-1].add_product(Product(input(), int(input())))
        self.w_vivod_categoryes = Vivod_categoryes()
        self.w_vivod_categoryes.show()


class Authtorisation(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project.ui', self)
        self.successfulAuth.hide()
        self.unsuccessfulAuth.hide()
        self.knopkaVoiti.clicked.connect(self.run)

    def run(self):
        login = self.login.text()
        password = self.password.text()
        pr = vhod(login, password)
        if pr:
            self.unsuccessfulAuth.hide()
            self.successfulAuth.show()
            ex.close_authtorisation()
            ex.show_vivod_categoryes()

        else:
            self.successfulAuth.hide()
            self.unsuccessfulAuth.show()


class Vivod_categoryes(QMainWindow):
    def __init__(self):
        self.categoryes_buttons = []
        button_x = 10
        button_y = 60
        button_height = 110
        button_width = 200
        super(Vivod_categoryes, self).__init__()
        uic.loadUi('test.ui', self)
        self.category_frame.setMinimumSize(0, 0)
        sch = 0
        for j in category_list:
            sch += 1
            if sch > 4:
                sch = 1
                button_x = 10
                button_y += 140
            button = QPushButton(self.category_frame)
            button.setGeometry(button_x, button_y, button_width, button_height)
            button.setText(j.return_name())
            button.clicked.connect(lambda checked, j=j: self.open_products_list(j))
            self.categoryes_buttons.append(button)
            button_x += 230

    def open_products_list(self, category):
        self.products_buttons = []
        button_x = 10
        button_y = 50
        button_width = 891
        button_height = 30
        for i in self.categoryes_buttons:
            i.hide()
        print(category.return_products_list())
        for j in category.return_products_list():
            button_y += 30
            button = QPushButton(self.category_frame)
            button.setGeometry(button_x, button_y, button_width, button_height)
            button.setText(j.return_name())
            button.clicked.connect(lambda checked, j=j: self.add_to_korzina(j))
            button.show()
            self.products_buttons.append(button)

    def add_to_korzina(self, product):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show_authtorisation()
    sys.exit(app.exec_())
