from PyQt5 import QtCore, QtWidgets, QtGui
import sys
from reg import Ui_MainWindow
from my_use import Ui_MainWindow_user
from my_token import Ui_MainWindow_token
from myProject import API

class Registration(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Registration, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.open_token_window)
        self.ui.pushButton_2.clicked.connect(self.open_user_window)

    def open_token_window(self):
        nickname = self.ui.lineEdit.text()
        self.token_window = TokenWindow(nickname)
        self.token_window.show()

    def open_user_window(self):
        nickname = self.ui.lineEdit.text()
        self.user_window = UserWindow(nickname)
        self.user_window.show()

class TokenWindow(QtWidgets.QMainWindow):
    def __init__(self, nickname, parent=None):
        super(TokenWindow, self).__init__(parent)
        self.ui = Ui_MainWindow_token()
        self.ui.setupUi(self)
        self.api = API(str(nickname))
        
            
        self.api.user_token(self)
            
        self.update_nicknameToken()
        self.update_balance()  
        self.update_cost()

        self.ui.pushButton.clicked.connect(self.approve)
        self.ui.pushButton_5.clicked.connect(self.create_token)
        self.ui.pushButton_6.clicked.connect(self.change_token)
            
            
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_balance)
        self.timer.timeout.connect(self.update_nicknameToken)
        self.timer.timeout.connect(self.update_cost)
        self.timer.timeout.connect(self.update_steck)
        self.timer.start(5000)  
        
    def create_token(self):
        cost = self.ui.lineEdit.text()
        count = self.ui.lineEdit_2.text()
        name = self.ui.lineEdit_3.text()
        short_name = self.ui.lineEdit_4.text()
        self.api.create_token(int(cost), int(count), name, short_name)
        
    def approve(self):
        self.api.approve_cell()
        
    def change_token(self):
        new_cost = self.ui.lineEdit_5.text()
        new_count = self.ui.lineEdit_6.text()
        new_short_name = self.ui.lineEdit_7.text()
        self.api.change_token(int(new_cost), int(new_count), new_short_name)
        
    def update_balance(self):
        info_token_result = self.api.info_token()
        
        if info_token_result is not None:
            balance = info_token_result.get('count', 'N/A')
        else:
            balance = 'N/A'
        
        self.ui.label_6.setText(f"Balance: {balance}")
        
    def update_nicknameToken(self):
        info_token_result = self.api.info_token()
        
        if info_token_result is not None:
            name = info_token_result.get('name', 'N/A')
            short_name = info_token_result.get('shortName', 'N/A')
        else:
            name = 'none'
            short_name = 'none'
        
        self.ui.label_5.setText(f"Token: {name} {short_name}")
        
    def update_cost(self):
        info_token_result = self.api.info_token()
        
        if info_token_result is not None:
            cost = info_token_result.get('cost', 'N/A')
        else:
            cost = 'none'
        self.ui.label.setText(f"Cost: {cost}")
        
    def update_steck(self):
        steck_result = self.api.steck_info()
        if steck_result is not None:
            
            token_balance = steck_result.get('tokenBalance', [])
            self.ui.tableWidget.setRowCount(0)
            
            for token in token_balance:
                user_name = token.get('userAddress', 'N/A')
                queque_value = token.get('QuequeValue', 'N/A')
                product = token.get('product', 'N/A')
                
                row_position = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row_position)
                
                self.ui.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(user_name)))
                self.ui.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(queque_value)))
                self.ui.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(product)))
            

class UserWindow(QtWidgets.QMainWindow):
    def __init__(self, nickname, parent=None):
        super(UserWindow, self).__init__(parent)
        self.ui = Ui_MainWindow_user()
        self.ui.setupUi(self)
        self.api = API(str(nickname))
        
        self.api.user_user()      

        self.ui.label_4.setText("Address " + nickname)
        self.update_balance()
            
        self.ui.pushButton.clicked.connect(self.add_money)
        self.ui.pushButton_2.clicked.connect(self.hide_address)
        self.ui.pushButton_8.clicked.connect(self.cell_token)
        self.ui.pushButton_9.clicked.connect(self.buy_token)
        self.ui.pushButton_7.clicked.connect(self.add_token)
            
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_balance)
        self.timer.timeout.connect(self.update_table_of_tokens)
        self.timer.start(10000)  
        
    def update_balance(self):
        balance = self.api.get_balance_token()
        if balance is not None:
            self.ui.label_3.setText(f"Balance: {balance} Dollar")
        else:
            self.ui.label_3.setText("Balance: 0 Doll")
            
    def add_money(self):
        money_add = self.ui.lineEdit.text()
        self.api.add_money(int(money_add))
        
    def hide_address(self):
        address = self.ui.lineEdit_2.text()
        self.api.hide_token(API(address).account)   
        
    def buy_token(self):
        token = self.ui.lineEdit_11.text()
        count = self.ui.lineEdit_12.text()
        self.api.buy_token(API(token).account, int(count))
         
    def cell_token(self):
        token = self.ui.lineEdit_10.text()
        count = self.ui.lineEdit_9.text()
        self.api.sell_token(API(token).account, int(count))
        
    def add_token(self):
        token = self.ui.lineEdit_8.text()
        self.api.add_token(API(token).account)
        
    def update_table_of_tokens(self):
        result_table = self.api.get_current_balance_token()
        if result_table is not None:
            token_balance = result_table.get('tokenBalance', [])
            balances = result_table.get('balances', 'N/A') 
            self.ui.tableWidget_4.setRowCount(0)
            
            for i, balance in enumerate(token_balance):
                name = balance.get('name', 'N/A')
                short_name = balance.get('shortName', 'N/A')
                cost = balance.get('cost', 'N/A')

                if isinstance(balances, int):
                    bal = balances
                else:
                    bal = balances[i] if i < len(balances) else 'N/A'
                
                row_position = self.ui.tableWidget_4.rowCount()
                self.ui.tableWidget_4.insertRow(row_position)
                
                self.ui.tableWidget_4.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(name)))
                self.ui.tableWidget_4.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(short_name)))
                self.ui.tableWidget_4.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(cost)))
                self.ui.tableWidget_4.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(bal)))
            

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Registration()
    myapp.show()
    sys.exit(app.exec())