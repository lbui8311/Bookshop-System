from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import QAbstractTableModel, Qt
import pandas as pd


# D:\App\Qt\Tools\QtDesignStudio\qt5_design_studio_reduced_version\bin

class DataFrameTableModel(QAbstractTableModel):

    def __init__(self, df, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.df = df

    def rowCount(self, parent=None):
        return self.df.shape[0]

    def columnCount(self, parent=None):
        return self.df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.df.iloc[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.df.columns[col]
        return None


class LoginGUI(QMainWindow):
    def __init__(self):
        super(LoginGUI, self).__init__()
        uic.loadUi('login_GUi_main.ui', self)
        self.df_books_users = pd.read_excel('Books_Users.xlsx', sheet_name='Users')
        self.setFixedHeight(185)
        self.setFixedWidth(350)
        self.setWindowTitle('Login!')
        self.log_button.clicked.connect(self.log_info)
        self.signup_button.clicked.connect(self.sign_up)
        self.show_signup_UI = 0
        self.show_book_list_UI = 0
        self.show()

    def log_info(self):
        for username in self.df_books_users.username:
            if self.log_username.text() == username:
                print(username)
                for password in self.df_books_users.password:
                    if self.log_password.text() == password:
                        print(password)
                        log_verify = QMessageBox()
                        log_verify.setWindowTitle('Information')
                        log_verify.setText('Login Successfully')
                        log_verify.setIcon(QMessageBox.Information)  # Warning, Critical, Information, Question
                        log_verify.setStandardButtons(QMessageBox.Ok)
                        response = log_verify.exec()
                        if response == QMessageBox.Ok:  # If User chooses Ok, continue below, else close the window
                            self.show_book_list_UI = BookGUI(username)
                            self.close()
                        break
                    else:
                        log_verify = QMessageBox()
                        log_verify.setWindowTitle('Warning')
                        log_verify.setText('Incorrect or Password ')
                        log_verify.setIcon(QMessageBox.Warning)  # Warning, Critical, Information, Question
                        log_verify.setStandardButtons(QMessageBox.Ok)
                        res = log_verify.exec()
                        break

    def sign_up(self):
        choice7 = QMessageBox()
        choice7.setWindowTitle('SignUp!')
        choice7.setText('Are you sure that you want to create an account?')
        choice7.setIcon(QMessageBox.Information)
        choice7.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        option7 = choice7.exec()
        if option7 == QMessageBox.Yes:
            self.show_signup_UI = SignUpGUI(self)
            self.close()


class SignUpGUI(QMainWindow):
    def __init__(self, parent):
        super(SignUpGUI, self).__init__()
        uic.loadUi('signup_GUI.ui', self)
        self.parent = parent
        self.show_Login_UI = 0
        self.df_users = 0
        self.setFixedHeight(165)
        self.setFixedWidth(240)
        self.setWindowTitle('New User!')
        self.add_user_button.clicked.connect(self.adding_user)
        self.show()

    def adding_user(self):
        signup_username = self.log_username.text()
        signup_password = self.log_password.text()
        if signup_username == '':
            pass
        elif signup_password == '':
            pass
        else:
            self.df_users = pd.read_excel('Books_Users.xlsx', sheet_name='Users')
            self.df_users.loc[len(self.df_users.index)] = [self.df_users.id.max() + 1, signup_username, signup_password]
            self.df_users.to_excel('Books_Users.xlsx', sheet_name='Users', index=False)
            signup_successful = QMessageBox()
            signup_successful.setWindowTitle('Information')
            signup_successful.setText('SignUp Successfully')
            signup_successful.setIcon(QMessageBox.Information)  # Warning, Critical, Information, Question
            signup_successful.setStandardButtons(QMessageBox.Ok)
            signup = signup_successful.exec()
            self.close()
            self.show_Login_UI = LoginGUI()
        pass


class AddNewUser(QMainWindow):
    def __init__(self, parent):
        super(AddNewUser, self).__init__()
        uic.loadUi('signup_GUI.ui', self)
        self.parent = parent
        self.df_users = 0
        self.setFixedHeight(165)
        self.setFixedWidth(240)
        self.setWindowTitle('New User!')
        self.add_user_button.clicked.connect(self.adding_user)
        self.show()

    def adding_user(self):
        new_username = self.log_username.text()
        new_password = self.log_password.text()
        if new_username == '':
            pass
        elif new_password == '':
            pass
        else:
            self.df_users = pd.read_excel('Books_Users.xlsx', sheet_name='Users')
            self.df_users.loc[len(self.df_users.index)] = [self.df_users.id.max() + 1, new_username, new_password]
            self.df_users.to_excel('Books_Users.xlsx', sheet_name='Users', index=False)
            self.parent.load_users()
            self.close()
        pass


class BookGUI(QMainWindow):
    def __init__(self, username):
        super(BookGUI, self).__init__()
        uic.loadUi('book_GUI.ui', self)
        self.name_label.setText('Hi, ' + username)
        self.df_books = 0
        self.df_books_order = 0
        self.df_orders = 0
        self.show_add_book_UI = 0
        self.show_update_book_UI = 0
        self.setFixedHeight(410)
        self.setFixedWidth(1040)
        self.setWindowTitle('Books List!')
        self.row_length = 3
        self.load_books_data()
        self.load_books_order()
        if username == 'Luan': # Admin
            self.users_control_button.clicked.connect(self.users_control)
        self.show_users_control_UI = 0
        self.signout_button.clicked.connect(self.users_login)
        self.show_users_login_UI = 0
        self.order_submit_button.clicked.connect(self.order_submit)
        self.show_order_submit_UI = 0
        self.order_update_button.clicked.connect(self.order_update)
        self.show_order_update_UI = 0
        self.order_delete_button.clicked.connect(self.order_delete)
        self.search_by_book.textChanged.connect(self.load_books_data)
        self.search_by_order.textChanged.connect(self.load_books_order)
        self.show()

    def load_books_data(self):
        while self.layout_books.count():
            self.layout_books.itemAt(0).widget().setParent(None)
        self.df_books = pd.read_excel('Books_Records.xlsx', sheet_name='Books')
        searchBook = self.search_by_book.text()
        self.df_books = self.df_books[(self.df_books.book.str.contains(searchBook)
                                       | self.df_books.author.str.contains(searchBook))].reset_index(drop=True)
        row_index = -1
        for i in range(len(self.df_books)):
            column_index = i % self.row_length  # Setting column limit to display
            if column_index == 0:
                row_index += 1  # Increment to new row when column limit is reached

            book = QLabel()
            book.setPixmap(QPixmap(str(self.df_books.photo_path[i])))
            book.setScaledContents(True)
            book.setFixedWidth(150)
            book.setFixedHeight(150)
            book.mousePressEvent = lambda e, id=self.df_books.id[i]: self.show_book(id)
            self.layout_books.addWidget(book, row_index, column_index)

    def load_books_order(self):
        self.df_books_order = pd.read_excel('Books_Orders.xlsx', sheet_name='Orders')
        searchOrder = self.search_by_order.text()
        self.df_books_order = self.df_books_order[(self.df_books_order.customer.str.contains(searchOrder))].reset_index(
            drop=True)
        # self.df_books_order = self.df_books_order.loc[:, self.df_books_order.columns != 'photo_path']
        books_data_model = DataFrameTableModel(self.df_books_order)
        self.tbl_orders.setModel(books_data_model)

    def show_book(self, id):
        book_options = QMessageBox()
        book_options.setWindowTitle('Please choose an option!')
        book_options.setText('Do you want to add a new book, update or delete?')
        book_options.setIcon(QMessageBox.Information)
        book_options.setStandardButtons(QMessageBox.Cancel)
        add_option = book_options.addButton('Add', QMessageBox.YesRole)
        update_option = book_options.addButton('Update', QMessageBox.YesRole)
        delete_option = book_options.addButton('Delete', QMessageBox.YesRole)
        # add_option.clicked.connect(self.add_book)
        # update_option.clicked.connect(self.update_book)
        # delete_option.clicked.connect(self.delete_book)
        book_response = book_options.exec()
        if book_options.clickedButton() == add_option:
            choice1 = QMessageBox()
            choice1.setWindowTitle('Add Book!')
            choice1.setText('Are you sure that you want to add a book?')
            choice1.setIcon(QMessageBox.Information)
            choice1.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            option1 = choice1.exec()
            if option1 == QMessageBox.Yes:
                self.show_add_book_UI = AddBookGUI(id, self)
        if book_options.clickedButton() == update_option:
            choice2 = QMessageBox()
            choice2.setWindowTitle('Update Book!')
            choice2.setText('Are you sure that you want to update this book?')
            choice2.setIcon(QMessageBox.Information)
            choice2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            option2 = choice2.exec()
            if option2 == QMessageBox.Yes:
                self.show_update_book_UI = UpdateBookGUI(id, self)
        if book_options.clickedButton() == delete_option:
            delete_final = QMessageBox()
            delete_final.setWindowTitle('Delete!')
            delete_final.setText('Are you sure that you want to delete this book?')
            delete_final.setIcon(QMessageBox.Information)
            delete_final.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            del_response = delete_final.exec()
            if del_response == QMessageBox.Yes:
                self.df_books = self.df_books[self.df_books.id != id]
                self.df_books.to_excel('Books_Records.xlsx', sheet_name='Books', index=False)
                self.load_books_data()
        pass

    def users_control(self):
        self.show_users_control_UI = UsersControlGUI()
        pass

    def users_login(self):
        self.show_users_login_UI = LoginGUI()
        self.close()
        pass

    def order_submit(self):
        choice5 = QMessageBox()
        choice5.setWindowTitle('Add Order!')
        choice5.setText('Are you sure that you want to add an order?')
        choice5.setIcon(QMessageBox.Information)
        choice5.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        option5 = choice5.exec()
        if option5 == QMessageBox.Yes:
            self.show_order_submit_UI = AddOrderGUI(self)
        pass

    def order_update(self):
        choice6 = QMessageBox()
        choice6.setWindowTitle('Update Order!')
        choice6.setText('Are you sure that you want to update this order?')
        choice6.setIcon(QMessageBox.Information)
        choice6.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        option6 = choice6.exec()
        if option6 == QMessageBox.Yes:
            indexes = self.tbl_orders.selectedIndexes()
            if indexes:
                print(indexes[0].row())
                id = indexes[0].row()
                self.show_order_update_UI = UpdateOrderGUI(id, self)
        pass

    def order_delete(self):
        indexes = self.tbl_orders.selectedIndexes()
        if indexes:
            if len(indexes) > 0:
                dialog = QMessageBox()
                dialog.setWindowTitle('Delete!')
                dialog.setText('Are you sure you want to delete this order?')
                dialog.setIcon(QMessageBox.Warning)
                dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                choice = dialog.exec()
                if choice == QMessageBox.Ok:
                    selected_row = indexes[0].row()
                    self.df_orders = pd.read_excel('Books_Orders.xlsx', sheet_name='Orders')
                    self.df_orders = self.df_orders.drop(selected_row)
                    self.df_orders.to_excel('Books_Orders.xlsx', sheet_name='Orders', index=False)
                    self.load_books_order()
        pass


class AddOrderGUI(QMainWindow):
    def __init__(self, parent):
        super(AddOrderGUI, self).__init__()
        uic.loadUi('add_order_GUI.ui', self)
        self.setWindowTitle('Add Order!')
        self.setFixedHeight(150)
        self.setFixedWidth(270)
        self.df_orders = 0
        self.parent = parent
        self.add_order_button.clicked.connect(self.order_submitting)
        self.show()

    def order_submitting(self):
        new_name = self.customer_name.text()
        new_date = self.date_order.text()
        new_price = self.total_price.text()
        if new_name == '':
            pass
        elif new_date == '':
            pass
        elif new_price == '':
            pass
        else:
            self.df_orders = pd.read_excel('Books_Orders.xlsx', sheet_name='Orders')
            self.df_orders.loc[len(self.df_orders.index)] = [self.df_orders.id.max() + 1, self.df_orders.id.max() + 1,
                                                             new_name, new_date, new_price]
            self.df_orders.to_excel('Books_Orders.xlsx', sheet_name='Orders', index=False)
            self.parent.load_books_order()
            self.close()
        pass


class UpdateOrderGUI(QMainWindow):
    def __init__(self, id, parent):
        super(UpdateOrderGUI, self).__init__()
        uic.loadUi('update_order_GUI.ui', self)
        self.setWindowTitle('Update Order!')
        self.setFixedWidth(270)
        self.setFixedHeight(165)
        self.parent = parent
        self.id = id
        self.df_orders = pd.read_excel('Books_Orders.xlsx', sheet_name='Orders')
        self.order = self.df_orders.loc[self.df_orders.id == self.id + 1].reset_index()
        self.customer_name.setText(str(self.order.customer[0]))
        self.date_order.setText(str(self.order.date[0]))
        self.price.setText(str(self.order.total_price[0]))
        self.update_order_button.clicked.connect(self.updating_order)
        self.show()

    def updating_order(self):
        same_name = self.customer_name.text()
        same_date = self.date_order.text()
        same_price = self.price.text()
        if same_name == '':
            pass
        elif same_date == '':
            pass
        elif same_price == '':
            pass
        else:
            self.df_orders = pd.read_excel('Books_Orders.xlsx', sheet_name='Orders')
            self.df_orders.loc[self.df_orders.id == self.order.id[0]] = [self.order.id[0],
                                                                         self.order.id[0],
                                                                         same_name, same_date, same_price]
            self.df_orders.to_excel('Books_Orders.xlsx', sheet_name='Orders', index=False)
            self.parent.load_books_order()
            self.close()


class AddBookGUI(QMainWindow):
    def __init__(self, id, parent):
        super(AddBookGUI, self).__init__()
        uic.loadUi('add_book_GUI.ui', self)
        self.setFixedHeight(370)
        self.setFixedWidth(270)
        self.setWindowTitle('Add Book to List')
        self.browse_photo.clicked.connect(self.browse_book_photo)
        self.add_book.clicked.connect(self.add_book_entry)
        self.photo_path = 0
        self.id = id
        self.parent = parent
        self.show()

    def browse_book_photo(self):
        file = QFileDialog.getOpenFileName(self, 'Chose an image', '', 'PNG Files (*.png)')  # Set the file type
        if file[0]:  # If a file/image is chosen, continue below
            self.photo_path = file[0]  # Set the new photo_path to the new chosen file/image
            self.photo_label.setPixmap(QPixmap(self.photo_path))  # Set the new file/image based on the new photo_path.
        pass

    def add_book_entry(self):
        book = self.book_name.text()
        author = self.author_name.text()
        copies = self.num_copies.text()
        book_price = self.price.text()
        if book == '':
            pass
        elif author == '':
            pass
        elif copies == '':
            pass
        elif book_price == '':
            pass
        elif self.photo_path == 0:
            pass
        else:
            self.df_books = pd.read_excel('Books_Records.xlsx', sheet_name='Books')
            self.df_books.loc[len(self.df_books.index)] = [self.df_books.id.max() + 1, book, author, copies, book_price,
                                                           self.photo_path]
            self.df_books.to_excel('Books_Records.xlsx', sheet_name='Books', index=False)
            self.parent.load_books_data()
            self.close()


class UpdateBookGUI(QMainWindow):
    def __init__(self, id, parent):
        super(UpdateBookGUI, self).__init__()
        uic.loadUi('update_book_GUI.ui', self)
        self.setFixedHeight(370)
        self.setFixedWidth(270)
        self.setWindowTitle('Update Book to List')
        self.df_books = pd.read_excel('Books_Records.xlsx', sheet_name='Books')
        self.book = self.df_books.loc[self.df_books.id == id].reset_index()  # Set the default profile from click image
        self.book_name.setText(str(self.book.book[0]))
        self.author_name.setText(str(self.book.author[0]))
        self.num_copies.setText(str(self.book.number[0]))
        self.price.setText(str(self.book.price[0]))
        self.photo_label.setPixmap(
            QPixmap(str(self.book.photo_path[0])))  # Set the default image based on clicked image
        self.browse_photo.clicked.connect(self.browse_book_photo)
        self.update_book.clicked.connect(self.update_book_entry)
        self.photo_path = self.book.photo_path[0]  # # Set the default image
        self.id = id
        self.parent = parent
        # print(self.book.Book[0])
        self.show()

    def browse_book_photo(self):
        file = QFileDialog.getOpenFileName(self, 'Chose an image', '', 'PNG Files (*.png)')  # Set the file type
        if file[0]:  # If a file/image is chosen, continue below
            self.photo_path = file[0]  # Set the new photo_path to the new chosen file/image
            self.photo_label.setPixmap(QPixmap(self.photo_path))  # Set the new file/image based on the new photo_path.
        pass

    def update_book_entry(self):
        book = self.book_name.text()
        author = self.author_name.text()
        copies = self.num_copies.text()
        book_price = self.price.text()
        if book == '':
            pass
        elif author == '':
            pass
        elif copies == '':
            pass
        elif book_price == '':
            pass
        elif self.photo_path == 0:
            pass
        else:
            df_books = pd.read_excel('Books_Records.xlsx', sheet_name='Books')
            df_books.loc[self.df_books.id == self.book.id[0]] = [self.book.id[0], book, author, copies, book_price,
                                                                 self.photo_path]
            df_books.to_excel('Books_Records.xlsx', sheet_name='Books', index=False)
            self.parent.load_books_data()
            self.close()
        pass


class UsersUpdateGUI(QMainWindow):
    def __init__(self, id, parent):
        super(UsersUpdateGUI, self).__init__()
        uic.loadUi("update_user_GUI.ui", self)
        self.setWindowTitle("Update User!")
        self.setFixedHeight(145)
        self.setFixedWidth(240)
        self.parent = parent
        self.id = id
        print(self.id)
        self.df_users = pd.read_excel('Books_Users.xlsx', sheet_name='Users')
        self.user = self.df_users.loc[self.df_users.id == self.id + 1].reset_index()
        self.log_username_2.setText(str(self.user.username[0]))
        self.log_password_2.setText(str(self.user.password[0]))
        self.update_user_button.clicked.connect(self.updating_user)
        self.show()

    def updating_user(self):
        same_username = self.log_username_2.text()
        same_password = self.log_password_2.text()
        if same_username == '':
            pass
        elif same_password == '':
            pass
        else:
            self.df_users = pd.read_excel('Books_Users.xlsx', sheet_name='Users')
            self.df_users.loc[self.df_users.id == self.user.id[0]] = [self.user.id[0], same_username, same_password]
            self.df_users.to_excel('Books_Users.xlsx', sheet_name='Users', index=False)
            self.parent.load_users()
            self.close()
        pass


class UsersControlGUI(QMainWindow):
    def __init__(self):
        super(UsersControlGUI, self).__init__()
        uic.loadUi("UsersControl_GUI.ui", self)
        self.df_users = 0
        self.df_sales = 0
        self.load_users()
        self.load_sales()
        self.setFixedWidth(350)
        self.setFixedHeight(370)
        self.setWindowTitle("Users Control & Sales")
        self.add_user.clicked.connect(self.adding_user)
        self.update_user.clicked.connect(self.updating_user)
        self.delete_user.clicked.connect(self.deleting_user)
        self.show_update_UI = 0
        self.show_signup_UI = 0
        self.search_by_user.textChanged.connect(self.load_users)
        self.search_by_sales.textChanged.connect(self.load_sales)
        self.show()

    def load_users(self):
        self.df_users = pd.read_excel('Books_Users.xlsx', sheet_name='Users')
        searchUser = self.search_by_user.text()
        self.df_users = self.df_users[(self.df_users.username.str.contains(searchUser))].reset_index(drop=True)
        users_data_model = DataFrameTableModel(self.df_users)
        self.tbl_users.setModel(users_data_model)
        pass

    def load_sales(self):
        self.df_sales = pd.read_excel('Books_OrderItems.xlsx', sheet_name='OrderItems')
        searchSales = self.search_by_sales.text()
        self.df_sales = self.df_sales[(self.df_sales.book_id.str.contains(searchSales))].reset_index(drop=True)
        sales_data_model = DataFrameTableModel(self.df_sales)
        self.tbl_sales.setModel(sales_data_model)
        pass

    def adding_user(self):
        choice3 = QMessageBox()
        choice3.setWindowTitle('Add User!')
        choice3.setText('Are you sure that you want to add a user?')
        choice3.setIcon(QMessageBox.Information)
        choice3.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        option3 = choice3.exec()
        if option3 == QMessageBox.Yes:
            self.show_signup_UI = AddNewUser(self)
            self.load_users()
        pass

    def updating_user(self):
        choice4 = QMessageBox()
        choice4.setWindowTitle('Update User!')
        choice4.setText('Are you sure that you want to update this user?')
        choice4.setIcon(QMessageBox.Information)
        choice4.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        option4 = choice4.exec()
        if option4 == QMessageBox.Yes:
            indexes = self.tbl_users.selectedIndexes()
            if indexes:
                print(indexes[0].row())
                id = indexes[0].row()
                self.show_update_UI = UsersUpdateGUI(id, self)
                self.load_users()
        pass

    def deleting_user(self):
        indexes = self.tbl_users.selectedIndexes()
        if indexes:
            if len(indexes) > 0:
                dialog = QMessageBox()
                dialog.setWindowTitle('Delete!')
                dialog.setText('Are you sure you want to delete this user?')
                dialog.setIcon(QMessageBox.Warning)
                dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                choice = dialog.exec()
                if choice == QMessageBox.Ok:
                    selected_row = indexes[0].row()
                    self.df_users = self.df_users.drop(selected_row)
                    self.df_users.to_excel('Books_Users.xlsx', sheet_name='Users', index=False)
                    self.load_users()
        pass


app = QApplication([])
window = LoginGUI()
app.exec()
