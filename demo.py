import sys
from PyQt5.QtWidgets import *


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.inputData = ["Yo Yo"]

        self.initUI()


    def initUI(self):
        okButton = QPushButton("OK")
        okButton.clicked.connect(self.showDialog)

        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.showDialog)

        #self.le = QLineEdit(self)
        #self.le.move(130, 22)

        self.tableWidget = QTableWidget()
        self.tableWidget.move(100,100)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(2)

        self.updateTable()

        # Right virticle box
        leftVbox = QVBoxLayout()
        leftVbox.addWidget(okButton)
        leftVbox.addWidget(cancelButton)

        # Right virticle box
        rightVbox = QVBoxLayout()
        rightVbox.addWidget(self.tableWidget)

        hbox = QHBoxLayout()
        hbox.addLayout(leftVbox)
        hbox.addLayout(rightVbox)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

        if ok:
            self.inputData.append(str(text))
            self.updateTable()
            #self.le.setText(str(text))

    def updateTable(self):
        for i, data in enumerate(self.inputData):
            self.tableWidget.setItem(i,0, QTableWidgetItem(data))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
