import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QMenu, QHBoxLayout, QVBoxLayout, \
    QWidget, QLCDNumber, QLineEdit, QComboBox
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        BUTTON_HEIGHT = 30

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #创建垂直布局结构
        connBox = QHBoxLayout()
        msg_area = QWidget()
        sendBox = QHBoxLayout()

        vbox = QVBoxLayout()
        vbox.addLayout(connBox)
        vbox.addWidget(msg_area)
        vbox.addLayout(sendBox)
        central_widget.setLayout(vbox)

        #创建连接按钮
        self.com_list = QComboBox()
        self.com_list.setFixedHeight(BUTTON_HEIGHT)
        self.com_list.addItem("COM1")
        self.com_list.addItem("COM2")
        self.com_list.addItem("COM3")
        connBox.addWidget(self.com_list)

        self.baud_list = QComboBox()
        self.baud_list.setFixedHeight(BUTTON_HEIGHT)
        self.baud_list.addItem("9600")
        self.baud_list.addItem("115200")
        connBox.addWidget(self.baud_list)

        conn_button = QPushButton("连接")
        conn_button.setFixedHeight(BUTTON_HEIGHT)
        connBox.addWidget(conn_button)
        conn_button.clicked.connect(self.on_conn_clicked)

        #设置消息显示控件
        msg_area.setStyleSheet("background-color: rgb(255, 255, 255);")


        #创建发送按钮
        msg_edit = QLineEdit()
        msg_edit.setFixedHeight(BUTTON_HEIGHT)
        sendBox.addWidget(msg_edit)
        send_button = QPushButton("发送")
        send_button.setFixedHeight(BUTTON_HEIGHT)
        sendBox.addWidget(send_button)
        send_button.clicked.connect(self.on_send_clicked)

        #设置主窗口属性
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("串口调试程序")  # 设置窗口标题
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 按钮点击事件的处理函数
    def on_conn_clicked(self):
        message_box = QMessageBox()
        message_box.setText("连接成功: %s - %s" % (self.com_list.currentText(), self.baud_list.currentText()))
        message_box.exec()

    def on_send_clicked(self):
        message_box = QMessageBox()
        message_box.setText("发送成功！")
        message_box.exec()



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()





