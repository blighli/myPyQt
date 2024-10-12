import sys
from warnings import catch_warnings

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QMenu, QHBoxLayout, QVBoxLayout, \
    QWidget, QLCDNumber, QLineEdit, QComboBox, QTextEdit, QSlider, QDial
from PyQt6.QtGui import QAction
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QIODevice, QByteArray, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        '''实列串口对象并设置初始化参数'''
        self.serialObject = QSerialPort()
        self.serialObject.setBaudRate(115200)
        self.serialObject.setStopBits(QSerialPort.StopBits.OneStop)
        self.serialObject.setDataBits(QSerialPort.DataBits.Data8)
        self.serialObject.setFlowControl(QSerialPort.FlowControl.NoFlowControl)
        self.serialObject.readyRead.connect(self.readData)


    def initUI(self):
        BUTTON_HEIGHT = 30

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #创建整体左右布局
        mainBox = QHBoxLayout()
        leftBox = QVBoxLayout()
        rightBox = QVBoxLayout()
        mainBox.addLayout(leftBox)
        mainBox.addLayout(rightBox)
        central_widget.setLayout(mainBox)

        #创建左侧垂直布局结构
        connBox = QHBoxLayout()
        self.msg_area = QTextEdit()
        sendBox = QHBoxLayout()
        leftBox.addLayout(connBox)
        leftBox.addWidget(self.msg_area)
        leftBox.addLayout(sendBox)

        #布局右侧窗格，创建拨号盘
        self.lcd = QLCDNumber()
        rightBox.addWidget(self.lcd)
        self.dial = QDial()
        rightBox.addWidget(self.dial)
        self.servoSlider = QSlider(Qt.Orientation.Horizontal)
        rightBox.addWidget(self.servoSlider)


        #创建连接按钮
        self.com_list = QComboBox()
        self.com_list.setFixedHeight(BUTTON_HEIGHT)
        portList = QSerialPortInfo.availablePorts()
        portList = sorted(portList, key=lambda x: eval(x.portName()[3:]))
        for i in portList:
            self.com_list.addItem(i.portName())
        connBox.addWidget(self.com_list)

        self.baud_list = QComboBox()
        self.baud_list.setFixedHeight(BUTTON_HEIGHT)
        self.baud_list.addItems(["9600", "19200", "38400", "115200", "230400", "460800", "921600"])
        self.baud_list.setCurrentIndex(3)
        connBox.addWidget(self.baud_list)

        self.conn_button = QPushButton("打开串口")
        self.conn_button.setFixedHeight(BUTTON_HEIGHT)
        connBox.addWidget(self.conn_button)
        self.conn_button.clicked.connect(self.on_conn_clicked)

        #设置消息显示控件
        self.msg_area.setStyleSheet("background-color: rgb(255, 255, 255);")


        #创建发送按钮
        self.msg_edit = QLineEdit()
        self.msg_edit.setFixedHeight(BUTTON_HEIGHT)
        sendBox.addWidget(self.msg_edit)
        self.send_button = QPushButton("发送")
        self.send_button.setFixedHeight(BUTTON_HEIGHT)
        sendBox.addWidget(self.send_button)
        self.send_button.clicked.connect(self.on_send_clicked)

        #设置拨号盘
        self.dial.setRange(0,180)
        self.dial.setPageStep(45)
        self.dial.setNotchTarget(10)
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.servoSlider.setValue)
        self.dial.valueChanged.connect(self.lcd.display)

        #设置滑条
        self.servoSlider.setFixedHeight(50)
        self.servoSlider.setMinimum(0)
        self.servoSlider.setMaximum(180)
        self.servoSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.servoSlider.setTickInterval(10)
        self.servoSlider.setPageStep(45)
        self.servoSlider.setSingleStep(10)
        self.servoSlider.setValue(90)
        self.servoSlider.valueChanged.connect(self.dial.setValue)
        self.servoSlider.valueChanged.connect(self.servoSliderChange)

        #设置主窗口属性
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle("串口调试程序")  # 设置窗口标题
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def sendData(self, data):
        if self.serialObject.isOpen():
            byteArray = QByteArray(data)
            self.serialObject.write(byteArray)

    def sendText(self, text):
        data = bytes(text, encoding='utf-8')
        self.sendData(data)

    def servoSliderChange(self):
        degree = self.servoSlider.value()
        self.sendText(str(degree))

    # 按钮点击事件的处理函数
    def on_conn_clicked(self):
        if self.serialObject.isOpen():
            self.serialObject.close()
            self.conn_button.setText("打开串口")
            self.com_list.setEnabled(True)
            self.baud_list.setEnabled(True)
            return
        comName = self.com_list.currentText()
        for i in QSerialPortInfo.availablePorts():
            if i.portName() == comName:  ## 查找串口
                self.serialObject.setPort(i)  ## 设置串口
                self.serialObject.setBaudRate(int(self.baud_list.currentText()))  ## 设置串口波特率
                if self.serialObject.open(QIODevice.OpenModeFlag.ReadWrite):
                    # 打开成功，改变按键提示字符串
                    self.conn_button.setText("关闭串口")
                    self.com_list.setEnabled(False)
                    self.baud_list.setEnabled(False)
                else:
                    # 打开失败，弹出提示警告
                    msg = QMessageBox(QMessageBox.Icon.Warning, "warning", "打开串口失败",
                                      QMessageBox.StandardButton.Ok)
                    msg.exec()
                break

    def on_send_clicked(self):
        self.sendText(self.msg_edit.text())

    def readData(self):
        try:
            data = self.serialObject.readAll()
            data = str(data.data(), encoding='utf-8')
            self.msg_area.append(data)
        except:
            self.msg_area.append("error\n")



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()





