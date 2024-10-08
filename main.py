import sys
from argparse import Action

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        newAct = QAction('New', self)
        fileMenu.addAction(newAct)
        newAct.triggered.connect(self.on_button_clicked)

        self.statusBar().showMessage('Ready')

        self.setGeometry(300, 300, 1200, 800)
        self.setWindowTitle("PyQt6 应用程序示例")  # 设置窗口标题
        # 创建按钮
        button = QPushButton("Click me!", self)
        button.setGeometry(300, 200, 200, 50)  # 设置按钮的位置和大小
        # 将按钮点击事件与处理函数关联
        button.clicked.connect(self.on_button_clicked)
        # 显示窗口
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 按钮点击事件的处理函数
    def on_button_clicked(self):
        message_box = QMessageBox()
        message_box.setText("Hello, PyQt6!")  # 创建一个消息框并显示消息
        message_box.exec()



def main():
    # 创建应用程序对象
    app = QApplication(sys.argv)
    # 创建主窗口
    window = MainWindow()
    # 运行应用程序的事件循环
    sys.exit(app.exec())

if __name__ == '__main__':
    main()





