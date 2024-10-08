import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

def main():
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 创建主窗口
    window = QMainWindow()
    window.setGeometry(300, 300, 400, 300)
    window.setWindowTitle("PyQt6 应用程序示例")  # 设置窗口标题

    # 创建按钮
    button = QPushButton("Click me!", window)
    button.setGeometry(50, 50, 100, 30)  # 设置按钮的位置和大小

    # 将按钮点击事件与处理函数关联
    button.clicked.connect(on_button_clicked)

    # 显示窗口
    window.show()

    # 运行应用程序的事件循环
    sys.exit(app.exec())

# 按钮点击事件的处理函数
def on_button_clicked():
    message_box = QMessageBox()
    message_box.setText("Hello, PyQt6!")  # 创建一个消息框并显示消息
    message_box.exec()

if __name__ == '__main__':
    main()




