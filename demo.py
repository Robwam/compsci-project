import sys
from PyQt5.QtWidgets import *


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.inputData = [] # Rows, each contains sub array for columns

        self.initUI()


    def initUI(self):
        add_event_button = QPushButton("Add event")
        add_event_button.clicked.connect(self.get_event_input)

        schedule_button = QPushButton("Schedule")

        # TODO wire this up to the schedule
        #schedule_button.clicked.connect(self.showDialog)

        #self.le = QLineEdit(self)
        #self.le.move(130, 22)

        self.event_name_textbox = QLineEdit(self)
        self.event_duration_textbox = QLineEdit(self)
        self.event_dependencies_textbox = QLineEdit(self)

        self.tableWidget = QTableWidget()
        self.tableWidget.move(100,100)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Duration', 'Dependencies'])

        self.updateTable()

        # Left virticle box
        labelsVbox = QVBoxLayout()
        inputsVbox = QVBoxLayout()
        labelsVbox.addWidget(QLabel("Name:"))
        inputsVbox.addWidget(self.event_name_textbox)
        labelsVbox.addWidget(QLabel("Duration:"))
        inputsVbox.addWidget(self.event_duration_textbox)
        labelsVbox.addWidget(QLabel("Dependencies:"))
        inputsVbox.addWidget(self.event_dependencies_textbox)

        leftVboxHbox = QHBoxLayout()
        leftVboxHbox.addLayout(labelsVbox)
        leftVboxHbox.addLayout(inputsVbox)


        leftVbox = QVBoxLayout()
        leftVbox.addLayout(leftVboxHbox)
        leftVbox.addWidget(add_event_button)
        leftVbox.addWidget(schedule_button)

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

    def get_event_input(self):
        event_name = self.event_name_textbox.text()
        self.event_name_textbox.setText('')

        event_duration = self.event_duration_textbox.text()
        self.event_duration_textbox.setText('')

        event_dependencies = self.event_dependencies_textbox.text()
        self.event_dependencies_textbox.setText('')

        self.inputData.append([event_name, event_duration, event_dependencies])

        # TODO add event to table
        self.updateTable()

    def updateTable(self):
        for r, row in enumerate(self.inputData):
            for c, col in enumerate(row):
                self.tableWidget.setItem(r,c, QTableWidgetItem(col))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
